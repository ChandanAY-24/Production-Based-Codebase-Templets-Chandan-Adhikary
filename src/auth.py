"""
Authentication and Access Control Bridge.
Reference: Spec/001-Spec-Security-guide.md (AUTH-01, AUTH-05, AC-01, AC-02, AC-04, CRYPTO-05)
Provides constant-time token comparison, role-based authorization, and user context
backed by the core Auth/ subsystem.
"""

from typing import Optional, Dict, List
from auth.models import AuthUser
from auth.service import default_auth_service, SYSTEM_TOKENS


def verify_token(token: Optional[str]) -> Optional[AuthUser]:
    """
    Verify bearer token using timing-safe comparison (CRYPTO-05 / AUTH-05).
    Delegates to Auth.service.default_auth_service.
    """
    return default_auth_service.verify_token(token)


def require_role(user: Optional[AuthUser], allowed_roles: List[str]) -> bool:
    """
    Check if the authenticated user possesses an authorized role (AC-01).
    Denies by default if user is None.
    """
    return default_auth_service.require_role(user, allowed_roles)


__all__ = ["AuthUser", "SYSTEM_TOKENS", "verify_token", "require_role"]
