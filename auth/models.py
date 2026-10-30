"""
Domain Models and Enums for the Authentication & Authorization Subsystem.
Reference: Spec/001-Spec-Security-guide.md (AUTH-01 through AUTH-06, AC-01 through AC-04)
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
import uuid

class UserRole(str, Enum):
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    QA = "qa"
    ADMIN = "admin"
    GUEST = "guest"

@dataclass
class AuthUser:
    """Authenticated user context attached to verified requests."""
    user_id: str
    role: str
    token: str
    email: Optional[str] = None
    session_id: Optional[str] = None

@dataclass
class UserRecord:
    """Internal user account record."""
    id: str
    email: str
    password_hash: str
    role: UserRole = UserRole.DEVELOPER
    is_active: bool = True
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    mfa_backup_codes: List[str] = field(default_factory=list)
    failed_login_attempts: int = 0
    locked_until: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class TokenPair:
    """Access and Refresh token bundle."""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in_seconds: int = 900  # 15 minutes default

@dataclass
class Session:
    """Server-side active user session (AUTH-05)."""
    session_id: str
    user_id: str
    created_at: float
    last_active_at: float
    expires_at: float
    client_ip: str
    user_agent: str
    is_revoked: bool = False

@dataclass
class AuthResult:
    """Result object for authentication and registration actions."""
    success: bool
    user: Optional[AuthUser] = None
    tokens: Optional[TokenPair] = None
    error: Optional[str] = None
    requires_mfa: bool = False
    mfa_ticket: Optional[str] = None
