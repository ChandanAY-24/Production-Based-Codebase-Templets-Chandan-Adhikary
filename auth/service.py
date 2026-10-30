"""
Central Authentication and Authorization Service.
Reference: Spec/001-Spec-Security-guide.md (AUTH-01 through AUTH-06, AC-01 through AC-04)
Orchestrates user management, credential validation, token rotation, sessions, and RBAC.
"""

from datetime import datetime, timezone
import hmac
import time
from typing import Optional, Dict, List, Any
import uuid

from auth.models import (
    UserRole,
    UserRecord,
    AuthUser,
    TokenPair,
    AuthResult,
    Session
)
from auth.passwords import (
    hash_password,
    verify_password,
    verify_dummy_password,
    validate_password_strength
)
from auth.tokens import TokenManager
from auth.session import SessionStore
from auth.mfa import verify_totp_code, verify_and_consume_backup_code

# Standard backward-compatible development tokens
SYSTEM_TOKENS: Dict[str, Dict[str, str]] = {
    "sdd-dev-token-architect-2026": {"user_id": "u_admin_01", "role": "architect", "email": "admin@agentic.sdd"},
    "sdd-dev-token-developer-2026": {"user_id": "u_dev_01", "role": "developer", "email": "dev@agentic.sdd"}
}

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 900  # 15 minutes


class AuthService:
    """Production-grade Authentication & Authorization Service."""

    def __init__(self, token_secret: Optional[str] = None):
        self.tokens = TokenManager(secret_key=token_secret)
        self.sessions = SessionStore()
        # In-memory user store indexed by user_id and email
        self._users: Dict[str, UserRecord] = {}
        self._email_index: Dict[str, str] = {}
        # Password reset token registry: {token: {"user_id": str, "expires_at": float}}
        self._reset_tokens: Dict[str, Dict[str, Any]] = {}
        self._preload_baseline_users()

    def _preload_baseline_users(self):
        """Preload baseline users from database seeds for seamless development and testing."""
        admin = UserRecord(
            id="u_admin_01",
            email="admin@agentic.sdd",
            password_hash=hash_password("Admin@Agentic2026!"),
            role=UserRole.ARCHITECT
        )
        self._users[admin.id] = admin
        self._email_index[admin.email.lower()] = admin.id

        dev = UserRecord(
            id="u_dev_01",
            email="dev@agentic.sdd",
            password_hash=hash_password("Developer@Agentic2026!"),
            role=UserRole.DEVELOPER
        )
        self._users[dev.id] = dev
        self._email_index[dev.email.lower()] = dev.id

    def register(self, email: str, password: str, role: UserRole = UserRole.DEVELOPER) -> AuthResult:
        """Register a new user with strict password complexity bounds (AUTH-01, AUTH-02)."""
        clean_email = email.strip().lower()
        if clean_email in self._email_index:
            return AuthResult(success=False, error="An account with this email already exists")

        is_valid, reason = validate_password_strength(password)
        if not is_valid:
            return AuthResult(success=False, error=f"Weak password: {reason}")

        user_id = f"u_{uuid.uuid4().hex[:12]}"
        record = UserRecord(
            id=user_id,
            email=clean_email,
            password_hash=hash_password(password),
            role=role
        )
        self._users[user_id] = record
        self._email_index[clean_email] = user_id

        user_context = AuthUser(user_id=user_id, role=role.value, token="", email=clean_email)
        return AuthResult(success=True, user=user_context)

    def login(
        self,
        email: str,
        password: str,
        client_ip: str = "127.0.0.1",
        user_agent: str = "unknown"
    ) -> AuthResult:
        """
        Authenticate user with constant-time password check and lockout defense (AUTH-01, AUTH-06).
        Uses generic error messages to eliminate user enumeration side-channels.
        """
        now = time.time()
        clean_email = email.strip().lower()
        user_id = self._email_index.get(clean_email)
        user = self._users.get(user_id) if user_id else None

        if not user or not user.is_active:
            # Execute dummy verification to maintain constant-time response (timing attack mitigation)
            verify_dummy_password(password)
            return AuthResult(success=False, error="Invalid email or password")

        # Check account lockout (AUTH-06)
        if user.locked_until:
            lock_time = float(user.locked_until)
            if now < lock_time:
                remaining = int(lock_time - now)
                return AuthResult(success=False, error=f"Account temporarily locked. Try again in {remaining}s")
            else:
                user.locked_until = None
                user.failed_login_attempts = 0

        # Verify password
        if not verify_password(password, user.password_hash):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                user.locked_until = str(now + LOCKOUT_DURATION_SECONDS)
                return AuthResult(success=False, error="Too many failed attempts. Account locked for 15 minutes")
            return AuthResult(success=False, error="Invalid email or password")

        # Password verified! Check MFA requirement (AUTH-04)
        if user.mfa_enabled:
            mfa_ticket = self.tokens.create_access_token(
                user_id=user.id,
                role="mfa_pending",
                ttl_seconds=300
            )
            return AuthResult(success=True, requires_mfa=True, mfa_ticket=mfa_ticket)

        # Successful login: reset failed attempts counter
        user.failed_login_attempts = 0
        user.locked_until = None

        # Create session and issue tokens (AUTH-05)
        session = self.sessions.create_session(user_id=user.id, client_ip=client_ip, user_agent=user_agent)
        token_pair = self.tokens.issue_token_pair(user_id=user.id, role=user.role.value, session_id=session.session_id)

        auth_user = AuthUser(
            user_id=user.id,
            role=user.role.value,
            token=token_pair.access_token,
            email=user.email,
            session_id=session.session_id
        )
        return AuthResult(success=True, user=auth_user, tokens=token_pair)

    def verify_mfa_login(self, mfa_ticket: str, mfa_code: str, client_ip: str = "127.0.0.1") -> AuthResult:
        """Complete 2FA login verification using TOTP or single-use backup code (AUTH-04)."""
        payload = self.tokens.verify_access_token(mfa_ticket)
        if not payload or payload.get("role") != "mfa_pending":
            return AuthResult(success=False, error="Invalid or expired MFA ticket")

        user_id = payload.get("sub")
        user = self._users.get(user_id)
        if not user or not user.mfa_enabled or not user.mfa_secret:
            return AuthResult(success=False, error="MFA not properly configured")

        # Try TOTP verification
        verified = verify_totp_code(user.mfa_secret, mfa_code)

        # Fallback to backup recovery code
        if not verified and user.mfa_backup_codes:
            backup_ok, remaining = verify_and_consume_backup_code(mfa_code, user.mfa_backup_codes)
            if backup_ok:
                verified = True
                user.mfa_backup_codes = remaining

        if not verified:
            return AuthResult(success=False, error="Invalid authentication code")

        # Session and token creation
        session = self.sessions.create_session(user_id=user.id, client_ip=client_ip)
        token_pair = self.tokens.issue_token_pair(user_id=user.id, role=user.role.value, session_id=session.session_id)
        auth_user = AuthUser(
            user_id=user.id,
            role=user.role.value,
            token=token_pair.access_token,
            email=user.email,
            session_id=session.session_id
        )
        return AuthResult(success=True, user=auth_user, tokens=token_pair)

    def verify_token(self, token: Optional[str]) -> Optional[AuthUser]:
        """
        Verify request token.
        Supports both JWT-signed access tokens and legacy development tokens with timing-safe comparison (CRYPTO-05).
        """
        if not token or not isinstance(token, str):
            return None

        clean_token = token.strip()
        if clean_token.startswith("Bearer "):
            clean_token = clean_token[7:].strip()

        # 1. Check backward-compatible SYSTEM_TOKENS (timing-safe comparison)
        for known_token, info in SYSTEM_TOKENS.items():
            if hmac.compare_digest(clean_token.encode("utf-8"), known_token.encode("utf-8")):
                return AuthUser(
                    user_id=info["user_id"],
                    role=info["role"],
                    token=clean_token,
                    email=info.get("email")
                )

        # 2. Check signed JWT access token (AUTH-05)
        claims = self.tokens.verify_access_token(clean_token)
        if claims:
            # Check session validity if session id is present
            sid = claims.get("sid")
            if sid and not self.sessions.get_session(sid):
                return None  # Session expired or revoked

            return AuthUser(
                user_id=claims.get("sub", ""),
                role=claims.get("role", "developer"),
                token=clean_token,
                session_id=sid
            )

        return None

    def refresh_token(self, refresh_token: str) -> Optional[TokenPair]:
        """Rotate refresh token with single-use replay protection (AUTH-05)."""
        return self.tokens.rotate_refresh_token(refresh_token)

    def logout(self, session_id: Optional[str], refresh_token: Optional[str] = None) -> bool:
        """Invalidate session and associated refresh token (AUTH-05)."""
        sess_ok = False
        if session_id:
            sess_ok = self.sessions.revoke_session(session_id)
        if refresh_token:
            self.tokens.revoke_token(refresh_token)
        return sess_ok

    def require_role(self, user: Optional[AuthUser], allowed_roles: List[str]) -> bool:
        """Enforce role-based access control; deny by default (AC-01)."""
        if not user:
            return False
        return user.role in allowed_roles


# Global singleton instance for system-wide auth resolution
default_auth_service = AuthService()

