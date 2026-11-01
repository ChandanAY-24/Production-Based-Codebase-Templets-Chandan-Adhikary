# Slash Command Workflow: /run
Description: Starts the application locally, runs smoke health checks, and verifies security headers before deployment.

## Trigger
- User invokes `/run` or asks to run the project locally / smoke check before deployment.

## Execution
Refer to the primary skill definition:
- [run SKILL.md](../skills/run/SKILL.md)

1. Run automated pre-deployment smoke check: `.venv\Scripts\python.exe .agents/scripts/smoke-runner.py`.
2. For live interactive server: run `$env:PYTHONPATH="."; .venv\Scripts\python.exe backend/main.py`.
3. Verify `GET /api/v1/health` and security headers (`X-Content-Type-Options: nosniff`).
4. Optionally serve `frontend/index.html` on port 3000.

