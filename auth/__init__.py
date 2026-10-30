"""
Authentication and Authorization Subsystem Package.
Reference: Spec/001-Spec-Security-guide.md (AUTH-01 through AUTH-06, AC-01 through AC-04)
Provides production-grade credentials, tokens, sessions, MFA, and RBAC controls.
"""

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
    validate_password_strength
)
from auth.tokens import TokenManager
from auth.session import SessionStore
from auth.mfa import (
    generate_totp_secret,
    generate_totp_code,
    verify_totp_code,
    generate_backup_codes,
    verify_and_consume_backup_code
)
from auth.service import (
    AuthService,
    SYSTEM_TOKENS
)

# Global default singleton service instance
default_auth_service = AuthService()

# Convenience functional exports
def verify_token(token):
    return default_auth_service.verify_token(token)

def require_role(user, allowed_roles):
    return default_auth_service.require_role(user, allowed_roles)

__all__ = [
    "UserRole",
    "UserRecord",
    "AuthUser",
    "TokenPair",
    "AuthResult",
    "Session",
    "hash_password",
    "verify_password",
    "validate_password_strength",
    "TokenManager",
    "SessionStore",
    "generate_totp_secret",
    "generate_totp_code",
    "verify_totp_code",
    "generate_backup_codes",
    "verify_and_consume_backup_code",
    "AuthService",
    "SYSTEM_TOKENS",
    "default_auth_service",
    "verify_token",
    "require_role"
]
