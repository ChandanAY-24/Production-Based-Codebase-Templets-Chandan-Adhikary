"""
Domain models for Agentic Tasks and Patch Verification.
Reference: docs/SPEC.md
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
import uuid

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    GRILLING = "GRILLING"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"

@dataclass
class AgentTask:
    title: str
    spec_reference: str
    invariants: List[str]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: str = "TDD-Engineer"
    execution_plan: List[str] = field(default_factory=list)
    user_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def advance_status(self, next_status: TaskStatus) -> None:
        """Validate state transition."""
        valid_transitions = {
            TaskStatus.PENDING: [TaskStatus.GRILLING, TaskStatus.IN_PROGRESS],
            TaskStatus.GRILLING: [TaskStatus.IN_PROGRESS, TaskStatus.FAILED],
            TaskStatus.IN_PROGRESS: [TaskStatus.REVIEW, TaskStatus.FAILED],
            TaskStatus.REVIEW: [TaskStatus.VERIFIED, TaskStatus.IN_PROGRESS, TaskStatus.FAILED],
            TaskStatus.VERIFIED: [],
            TaskStatus.FAILED: [TaskStatus.PENDING]
        }
        if next_status not in valid_transitions[self.status]:
            raise ValueError(f"Invalid transition from {self.status} to {next_status}")
        self.status = next_status
        self.updated_at = datetime.now(timezone.utc).isoformat()
