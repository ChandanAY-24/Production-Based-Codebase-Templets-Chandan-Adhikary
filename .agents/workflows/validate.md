# Slash Command Workflow: /validate
Description: Executes end-to-end production validation across environment, linting, AST security, and deterministic tests.

## Trigger
- User invokes `/validate` or requests a full repository health check prior to commit, merge, or deployment.

## Execution
Refer to the primary skill definition:
- [validate SKILL.md](../skills/validate/SKILL.md)

1. Launch validator harness:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/validator.py
   ```
2. If any phase fails, inspect the structured error output, consult `Error-Tracker.xlsx`, and apply surgical remediations.
3. Once all 5 phases pass, the codebase is verified production-ready.

