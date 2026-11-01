# Slash Command Workflow: /run (Deprecated Alias -> /code-runner)
Description: Legacy alias redirecting to `/code-runner` for local application execution and smoke verification.

> **Notice:** `/run` is now superseded by `/code-runner`. Please invoke `/code-runner` directly.

## Execution
Refer to the primary `/code-runner` workflow and skill definition:
- [code-runner Workflow](code-runner.md)
- [code-runner SKILL.md](../skills/code-runner/SKILL.md)

1. Launch smoke checks or local server via `/code-runner`:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/smoke-runner.py
   ```
