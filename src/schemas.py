"""
Strict Input Validation Schemas.
Reference: Spec/001-Spec-Security-guide.md (INP-01, AC-03, API-03)
Enforces boundary schemas, rejects unknown fields (mass assignment prevention), and limits lengths.
"""

from typing import List
from pydantic import BaseModel, Field, ConfigDict

class TaskCreateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Rejects unknown fields (AC-03)

    title: str = Field(..., min_length=1, max_length=80, description="Brief task summary")
    specReference: str = Field(..., min_length=1, max_length=200, description="Reference link or anchor in docs/SPEC.md")
    invariants: List[str] = Field(..., min_length=1, max_length=20, description="Non-negotiable invariants (docs/CONSTITUTION.md)")

class PatchVerifySchema(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Rejects unknown fields (AC-03)

    patch: str = Field(..., min_length=1, max_length=50000, description="Unified git diff patch")
    targetFile: str = Field(..., min_length=1, max_length=255, description="Target file path under workspace")
    runTests: bool = Field(default=True, description="Whether to trigger automated test verification")
