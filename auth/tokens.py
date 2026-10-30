"""
Cryptographic Token Management & Single-Use Rotation Engine.
Reference: Spec/001-Spec-Security-guide.md (AUTH-05, CRYPTO-05)
Provides HMAC-SHA256 signed access tokens and rotating refresh tokens with replay protection.
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Optional, Dict, Any, Tuple
from auth.models import TokenPair

# Default signing key (can be overridden via AUTH_SIGNING_SECRET env var)
DEFAULT_SECRET = os.getenv("AUTH_SIGNING_SECRET", "sdd-agentic-secure-token-secret-2026-key")


class TokenManager:
    """Manages access token signing and single-use refresh token rotation."""

    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = (secret_key or DEFAULT_SECRET).encode("utf-8")
        # In-memory storage for refresh tokens: {refresh_token: {"user_id": str, "family_id": str, "expires_at": float, "is_spent": bool}}
        self._refresh_registry: Dict[str, Dict[str, Any]] = {}

    def _b64encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    def _b64decode(self, s: str) -> bytes:
        padding = 4 - (len(s) % 4)
        if padding != 4:
            s += "=" * padding
        return base64.urlsafe_b64decode(s.encode("utf-8"))

    def create_access_token(
        self,
        user_id: str,
        role: str,
        ttl_seconds: int = 900,  # 15 minutes
        session_id: Optional[str] = None,
        extra_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a compact, signed JWT-compatible token: header.payload.signature
        Enforces fixed HS256 algorithm and mandatory exp claim (AUTH-05).
        """
        now = int(time.time())
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": user_id,
            "role": role,
            "iat": now,
            "exp": now + ttl_seconds,
            "jti": secrets.token_hex(12),
            "sid": session_id or secrets.token_hex(8)
        }
        if extra_claims:
            payload.update(extra_claims)

        header_b64 = self._b64encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        payload_b64 = self._b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")

        signature = hmac.new(self.secret_key, signing_input, hashlib.sha256).digest()
        signature_b64 = self._b64encode(signature)

        return f"{header_b64}.{payload_b64}.{signature_b64}"

    def verify_access_token(self, token_str: str) -> Optional[Dict[str, Any]]:
        """
        Verify access token signature and expiration with timing-safe comparison (CRYPTO-05).
        Rejects alg:none, malformed tokens, and expired tokens.
        """
        if not token_str or not isinstance(token_str, str):
            return None

        clean_token = token_str.strip()
        if clean_token.startswith("Bearer "):
            clean_token = clean_token[7:].strip()

        parts = clean_token.split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts

        try:
            # Verify signature first
            signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
            expected_sig = hmac.new(self.secret_key, signing_input, hashlib.sha256).digest()
            actual_sig = self._b64decode(signature_b64)

            if not hmac.compare_digest(expected_sig, actual_sig):
                return None

            # Verify header
            header = json.loads(self._b64decode(header_b64).decode("utf-8"))
            if header.get("alg") != "HS256":
                return None

            # Verify payload & expiry
            payload = json.loads(self._b64decode(payload_b64).decode("utf-8"))
            now = int(time.time())
            if payload.get("exp", 0) <= now:
                return None  # Expired

            return payload
        except Exception:
            return None

    def create_refresh_token(
        self,
        user_id: str,
        role: str,
        family_id: Optional[str] = None,
        ttl_seconds: int = 604800  # 7 days
    ) -> str:
        """
        Generate a cryptographically secure random refresh token (AUTH-05).
        """
        token = f"rt_{secrets.token_urlsafe(32)}"
        now = time.time()
        self._refresh_registry[token] = {
            "user_id": user_id,
            "role": role,
            "family_id": family_id or f"fam_{secrets.token_hex(8)}",
            "expires_at": now + ttl_seconds,
            "is_spent": False
        }
        return token

    def issue_token_pair(self, user_id: str, role: str, session_id: Optional[str] = None) -> TokenPair:
        """Issue access token + refresh token bundle."""
        family_id = f"fam_{secrets.token_hex(8)}"
        access_token = self.create_access_token(user_id=user_id, role=role, session_id=session_id)
        refresh_token = self.create_refresh_token(user_id=user_id, role=role, family_id=family_id)
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in_seconds=900
        )

    def rotate_refresh_token(self, old_refresh_token: str) -> Optional[TokenPair]:
        """
        Rotate refresh token (AUTH-05 Single-Use Rotation).
        If an already spent refresh token is presented, revoke the entire token family (Replay Defense).
        """
        record = self._refresh_registry.get(old_refresh_token)
        if not record:
            return None

        family_id = record["family_id"]

        # Replay attack detection: if token is already spent, invalidate all tokens in this family
        if record["is_spent"]:
            self.revoke_family(family_id)
            return None

        # Check expiration
        now = time.time()
        if record["expires_at"] <= now:
            del self._refresh_registry[old_refresh_token]
            return None

        # Mark current token as spent
        record["is_spent"] = True

        # Issue new pair within same family
        user_id = record["user_id"]
        role = record["role"]
        new_access = self.create_access_token(user_id=user_id, role=role)
        new_refresh = self.create_refresh_token(user_id=user_id, role=role, family_id=family_id)

        return TokenPair(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="Bearer",
            expires_in_seconds=900
        )

    def revoke_family(self, family_id: str) -> int:
        """Revoke all refresh tokens belonging to a family."""
        to_delete = [t for t, rec in self._refresh_registry.items() if rec.get("family_id") == family_id]
        for t in to_delete:
            del self._refresh_registry[t]
        return len(to_delete)

    def revoke_token(self, refresh_token: str) -> bool:
        """Revoke a single refresh token."""
        if refresh_token in self._refresh_registry:
            del self._refresh_registry[refresh_token]
            return True
        return False
