# Slash Command Workflow: /clarify
Description: Executes the Grill-Me pre-implementation protocol to resolve ambiguities and probe invariants.

## Trigger
- User invokes `/clarify` or input requirement contains ambiguity / underspecified rules.

## Execution
Refer to the primary skill definition:
- [clarify SKILL.md](../skills/clarify/SKILL.md)

1. Formulate 2-4 targeted multiple-choice questions focusing on edge cases and invariants.
2. Halt implementation until user feedback is provided.
3. Record confirmed invariants in `docs/SPEC.md` and feature contracts.

