"""
Task Management and Verification Service.
Reference: docs/SPEC.md
"""

from typing import Dict, List, Optional
from src.models import AgentTask, TaskStatus

class TaskService:
    def __init__(self):
        self._tasks: Dict[str, AgentTask] = {}

    def create_task(self, title: str, spec_ref: str, invariants: List[str], user_id: Optional[str] = None) -> AgentTask:
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        if not invariants:
            raise ValueError("At least one invariant is required (docs/CONSTITUTION.md)")

        task = AgentTask(
            title=title.strip(),
            spec_reference=spec_ref,
            invariants=invariants,
            user_id=user_id
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[AgentTask]:
        return self._tasks.get(task_id)

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        user_id: Optional[str] = None,
        limit: int = 100
    ) -> List[AgentTask]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if user_id:
            tasks = [t for t in tasks if t.user_id == user_id]
        return tasks[:max(1, min(limit, 100))]
