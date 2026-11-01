# Slash Command Workflow: /checklist
Description: Generates and audits production release readiness checklists and quality sign-offs.

## Trigger
- User invokes `/checklist` before a release, PR merge, or deployment.

## Execution
Refer to the primary skill definition:
- [checklist SKILL.md](../skills/checklist/SKILL.md)

1. Check current readiness status:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/task-checklist.py stats
   ```
2. Review the production checklist across Specification, Simplicity, Security, Testing, and Runtime.
3. Verify all checklist criteria against automated test and audit evidence.
4. Synchronize sign-off status to `Task-Checklist.xlsx`:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/task-checklist.py sync
   ```
5. Emit sign-off decision (RELEASE READY or RELEASE BLOCKED).

