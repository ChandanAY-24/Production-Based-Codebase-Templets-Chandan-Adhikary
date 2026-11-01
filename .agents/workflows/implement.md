# Slash Command Workflow: /implement
Description: Executes surgical, deterministic code implementation using Super-TDD (Red-Green-Refactor).

## Trigger
- User invokes `/implement` or asks to build a task/feature.

## Execution
Refer to the primary skill definition:
- [implement SKILL.md](../skills/implement/SKILL.md)

1. Verify task assignment in `docs/TASKS.md`.
2. Write deterministic failing test (RED) in `tests/`.
3. Implement surgical minimal code (GREEN) adhering to <= 40 lines per function.
4. Refactor, remove dead logic, and enforce diff <= 150 lines.
5. Verify AST safety with `hooks/commit-guardian.py --ast-only`.

