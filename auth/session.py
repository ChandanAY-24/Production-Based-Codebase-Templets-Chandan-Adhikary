"""
Server-Side Session Store & Lifecycle Management.
Reference: Spec/001-Spec-Security-guide.md (AUTH-05, AUTH-06)
Provides thread-safe session storage, idle/absolute expiration, and user session revocation.
"""

import secrets
import threading
import time
from typing import Optional, List, Dict
from auth.models import Session


class SessionStore:
    """Thread-safe in-memory session manager with idle and absolute expiration."""

    def __init__(self, idle_timeout_seconds: int = 1800, absolute_timeout_seconds: int = 86400):
        self.idle_timeout_seconds = idle_timeout_seconds        # Default: 30 minutes idle
        self.absolute_timeout_seconds = absolute_timeout_seconds  # Default: 24 hours absolute
        self._sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()

    def create_session(self, user_id: str, client_ip: str = "127.0.0.1", user_agent: str = "unknown") -> Session:
        """Create and register a new authenticated session (AUTH-05)."""
        now = time.time()
        session_id = f"sess_{secrets.token_urlsafe(32)}"
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            last_active_at=now,
            expires_at=now + self.absolute_timeout_seconds,
            client_ip=client_ip,
            user_agent=user_agent,
            is_revoked=False
        )
        with self._lock:
            self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Validate and touch active session.
        Enforces idle timeout and absolute timeout (AUTH-05).
        """
        now = time.time()
        with self._lock:
            session = self._sessions.get(session_id)
            if not session or session.is_revoked:
                return None

            # Absolute timeout check
            if now > session.expires_at:
                del self._sessions[session_id]
                return None

            # Idle timeout check
            if (now - session.last_active_at) > self.idle_timeout_seconds:
                del self._sessions[session_id]
                return None

            # Update last active timestamp
            session.last_active_at = now
            return session

    def revoke_session(self, session_id: str) -> bool:
        """Explicitly revoke a single session on logout (AUTH-05)."""
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id].is_revoked = True
                del self._sessions[session_id]
                return True
            return False

    def revoke_all_for_user(self, user_id: str) -> int:
        """Revoke all sessions for a user upon password reset or security event (AUTH-03, AUTH-06)."""
        revoked_count = 0
        with self._lock:
            to_remove = []
            for sid, s in self._sessions.items():
                if s.user_id == user_id:
                    s.is_revoked = True
                    to_remove.append(sid)
            for sid in to_remove:
                del self._sessions[sid]
                revoked_count += 1
        return revoked_count

    def list_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """List active sessions for user transparency and audit (AUTH-06)."""
        now = time.time()
        active = []
        with self._lock:
            for s in self._sessions.values():
                if s.user_id == user_id and not s.is_revoked and now <= s.expires_at:
                    active.append({
                        "sessionId": s.session_id,
                        "clientIp": s.client_ip,
                        "userAgent": s.user_agent,
                        "createdAt": s.created_at,
                        "lastActiveAt": s.last_active_at
                    })
        return active
