# Slash Command Workflow: /code-testing
Description: Runs deterministic automated test suites, negative security verifications, and regression tests.

> **Order Invariant:** When automated workflows trigger, `code-testing` executes FIRST, followed by `code-review`.

## Execution Structure
Refer to the primary skill definition:
- [code-testing SKILL.md](../skills/code-testing/SKILL.md)

1. **test-writer Phase:**
   - Verify negative security tests and boundary tests exist in `tests/test_*.py`.
2. **test-runner Phase:**
   - Execute Pytest suite:
     ```powershell
     $env:PYTHONPATH="."; $env:ENVIRONMENT="testing"; .venv\Scripts\python.exe -m pytest -v
     ```
   - Enforce 100% pass rate. If any test fails, STOP and do not proceed to code-review.
