"""
Application Configuration and Environment Validation.
Reference: Spec/001-Spec-Security-guide.md (SEC-02)
Enforces safe environment defaults, type checks, and startup validation.
"""

import os
from typing import List
from pydantic import BaseModel, Field

class AppConfig(BaseModel):
    environment: str = Field(default="development")
    port: int = Field(default=8000, ge=1024, le=65535)
    allowed_origins: List[str] = Field(default_factory=lambda: [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ])
    max_request_body_bytes: int = Field(default=1_048_576, ge=1024, le=10_485_760)  # Default 1MB, max 10MB
    rate_limit_requests_per_minute: int = Field(default=60, ge=1, le=1000)
    api_tokens: List[str] = Field(default_factory=lambda: [
        # Default development tokens (in production, loaded strictly from environment)
        "sdd-dev-token-architect-2026",
        "sdd-dev-token-developer-2026"
    ])
    log_level: str = Field(default="INFO")

def load_config() -> AppConfig:
    """Load and validate configuration from environment variables."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    port = int(os.getenv("PORT", "8000"))
    origins_env = os.getenv("ALLOWED_ORIGINS")
    allowed_origins = [o.strip() for o in origins_env.split(",") if o.strip()] if origins_env else [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    tokens_env = os.getenv("API_TOKENS")
    if tokens_env:
        tokens = [t.strip() for t in tokens_env.split(",") if t.strip()]
    elif env == "production":
        raise ValueError("[SECURITY] API_TOKENS must be explicitly defined in production (SEC-02)")
    else:
        tokens = ["sdd-dev-token-architect-2026", "sdd-dev-token-developer-2026"]

    return AppConfig(
        environment=env,
        port=port,
        allowed_origins=allowed_origins,
        api_tokens=tokens,
        log_level=os.getenv("LOG_LEVEL", "INFO")
    )
