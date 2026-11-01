# Slash Command Workflow: /git-log
Description: Inspects git history, branches, file changelogs, and verifies Conventional Commit compliance.

## Trigger
- User invokes `/git-log` or asks to review git history, verify commit compliance, or trace file evolution.

## Execution
Refer to the primary skill definition:
- [git-log SKILL.md](../skills/git-log/SKILL.md)

1. For interactive history check:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/git-log-auditor.py --limit 10
   ```
2. For branch graph visualization:
   ```powershell
   git log --graph --oneline --decorate -n 15
   ```
3. For single file audit:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/git-log-auditor.py --file <path>
   ```

