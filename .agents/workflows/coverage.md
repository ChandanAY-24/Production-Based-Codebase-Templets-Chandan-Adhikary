# Slash Command Workflow: /coverage
Description: Audits test coverage across domain logic, auth, and backend modules.

## Trigger
- User invokes `/coverage` or requests code coverage analysis.

## Execution
Refer to the primary skill definition:
- [coverage SKILL.md](../skills/coverage/SKILL.md)

1. Run `.venv\Scripts\python.exe -m pytest --cov=src --cov=auth --cov=backend --cov-report=term-missing`.
2. Compare coverage against minimum thresholds (85% domain, 95% auth/crypto).
3. Report untested lines and error handling branches.

