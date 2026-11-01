# Slash Command Workflow: /tasks
Description: Manages active tasks, lifecycle transitions, priority tracking, and subtask breakdowns.

## Trigger
- User invokes `/tasks`, `/tasks list`, `/tasks add`, or updates task progress.

## Execution
Refer to the primary skill definition:
- [tasks SKILL.md](../skills/tasks/SKILL.md)

1. Read and synchronize with `docs/TASKS.md` and `Task-Checklist.xlsx`.
2. Inspect or update task status (`PENDING` -> `IN_PROGRESS` -> `IN_REVIEW` -> `DONE`).
3. Synchronize `Task-Checklist.xlsx` with `.venv\Scripts\python.exe .agents/scripts/task-checklist.py sync`.
4. Ensure task scope adherence and link to formal specifications.

