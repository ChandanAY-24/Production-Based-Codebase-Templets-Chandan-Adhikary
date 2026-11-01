# Slash Command Workflow: /code-runner
Description: Starts the application locally, runs smoke health checks, and verifies security headers before deployment.

## Trigger
- User invokes `/code-runner` or asks to run the codebase, start local backend/frontend, or perform smoke checks.

## Execution
Refer to the primary skill definition:
- [code-runner SKILL.md](../skills/code-runner/SKILL.md)

1. Run automated pre-deployment smoke check:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/smoke-runner.py
   ```
2. For live interactive server:
   ```powershell
   $env:PYTHONPATH="."; .venv\Scripts\python.exe backend/main.py
   ```
3. Verify `GET /api/v1/health` and security headers (`X-Content-Type-Options: nosniff`).
4. Optionally serve `frontend/index.html` on port 3000.

