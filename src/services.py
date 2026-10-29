"""
Task Management and Verification Service.
Reference: docs/SPEC.md
"""

from typing import Dict, List, Optional
from src.models import AgentTask, TaskStatus

class TaskService:
    def __init__(self):
        self._tasks: Dict[str, AgentTask] = {}

    def create_task(self, title: str, spec_ref: str, invariants: List[str]) -> AgentTask:
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        if not invariants:
            raise ValueError("At least one invariant is required (docs/CONSTITUTION.md)")

        task = AgentTask(
            title=title.strip(),
            spec_reference=spec_ref,
            invariants=invariants
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[AgentTask]:
        return self._tasks.get(task_id)

    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[AgentTask]:
        if status:
            return [t for t in self._tasks.values() if t.status == status]
        return list(self._tasks.values())
