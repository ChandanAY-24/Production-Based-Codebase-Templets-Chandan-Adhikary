"""
Structured Security Audit Logger.
Reference: Spec/001-Spec-Security-guide.md (LOG-01, LOG-02)
Logs security-relevant events in structured JSON format with zero secret leakage.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# Configure standard logger
audit_logger = logging.getLogger("sdd.security.audit")
if not audit_logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[AUDIT] %(message)s"))
    audit_logger.addHandler(handler)
    audit_logger.setLevel(logging.INFO)

# High-risk fields to redact automatically (LOG-02)
REDACT_KEYS = {"password", "token", "authorization", "secret", "api_key", "cookie", "access_token"}

def sanitize_metadata(data: Dict[str, Any]) -> Dict[str, Any]:
    """Scrub sensitive credentials from logging metadata."""
    sanitized = {}
    for k, v in data.items():
        if any(sensitive in k.lower() for sensitive in REDACT_KEYS):
            sanitized[k] = "[REDACTED]"
        elif isinstance(v, dict):
            sanitized[k] = sanitize_metadata(v)
        else:
            sanitized[k] = v
    return sanitized

def log_security_event(
    action: str,
    status: str,
    client_ip: str,
    user_id: Optional[str] = None,
    resource: Optional[str] = None,
    request_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """
    Emit structured audit log entry for security and compliance monitoring (LOG-01).
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "status": status,
        "clientIp": client_ip,
        "userId": user_id or "anonymous",
        "resource": resource or "",
        "requestId": request_id or "",
        "details": sanitize_metadata(details or {})
    }
    audit_logger.info(json.dumps(entry))
