# Task Checklist Continuous Synchronization Rule

> **Standard:** `Task-Checklist.xlsx`, `docs/TASKS.md`, `.agents/scripts/task-checklist.py`  
> **Mandate:** Real-time synchronization & complete date-time traceability

To ensure `Task-Checklist.xlsx` is always up to date across all agent interactions, all AI agents and engineers modifying tasks, executing quality gates, or cutting releases MUST adhere to this rule.

---

## 1. Real-Time Synchronization Invariant
Whenever a task transition occurs (e.g. from `PENDING` $\rightarrow$ `IN_PROGRESS` $\rightarrow$ `REVIEW` $\rightarrow$ `VERIFIED`):
1. Update `docs/TASKS.md` with the new status and acceptance criteria.
2. Immediately run the synchronization engine:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/task-checklist.py sync
   ```
3. Or update the specific checklist item via CLI:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/task-checklist.py update --id <TASK-ID-or-TC-ID> --status <VERIFIED|IN_PROGRESS|BLOCKED> --notes "<Verification notes>"
   ```
   This automatically updates `Last Updated Date-Time` with the current timestamp (`YYYY-MM-DD HH:MM:SS`).

---

## 2. Pre-Release Sign-Off
Before merging a pull request or tagging a release:
1. Run `.venv\Scripts\python.exe .agents/scripts/task-checklist.py stats`.
2. Ensure zero `BLOCKED` items exist.
3. Verify all associated release criteria (`TC-015`, `TC-016`) are marked `VERIFIED`.

