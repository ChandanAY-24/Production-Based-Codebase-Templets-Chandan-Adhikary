# Slash Command Workflow: /code-review
Description: Executes the Five Quality Gates and AST consensus code review.

## Trigger
- User invokes `/code-review` on a PR, commit, or workspace diff.

## Execution
Refer to the primary skill definition:
- [code-review SKILL.md](../skills/code-review/SKILL.md)

1. Verify Gate 1: Task traceability in `docs/TASKS.md` & diff <= 150 lines.
2. Verify Gate 2: Static analysis pass via flake8 / syntax checks.
3. Verify Gate 3: AST scan and secret leak prevention via `hooks/commit-guardian.py`.
4. Verify Gate 4: 100% test pass rate with `.venv\Scripts\python.exe -m pytest`.
5. Verify Gate 5: Emit structured verdict (APPROVE / REQUEST_CHANGES / BLOCK).

