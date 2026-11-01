# Slash Command Workflow: /code-testing
Description: Runs deterministic automated test suites, negative security verifications, and regression tests.

## Trigger
- User invokes `/code-testing` or asks to run tests.

## Execution
Refer to the primary skill definition:
- [code-testing SKILL.md](../skills/code-testing/SKILL.md)

1. Verify `.venv` and set test environment variables (`$env:ENVIRONMENT = "testing"`).
2. Execute primary pytest runner: `.venv\Scripts\python.exe -m pytest -v`.
3. If targeted, run `tests/test_auth.py`, `tests/test_security.py`, or `tests/test_services.py`.
4. Ensure 100% pass rate with zero regression errors.

