# Slash Command Workflow: /plan
Description: Executes Recursive Epistemic Action (REA) and Spec-Driven Development (SDD) planning.

## Trigger
- User invokes `/plan` or requests feature decomposition.

## Execution
Refer to the primary skill definition:
- [plan SKILL.md](../skills/plan/SKILL.md)

1. Review `docs/SPEC.md`, `specs/`, and `docs/CONSTITUTION.md`.
2. Extract uncertainties and trigger `/clarify` if any domain rule is ambiguous.
3. Formulate atomic milestones with P0-P3 task decomposition in `docs/TASKS.md`.
4. Establish Super-TDD failing test contracts prior to code generation.

