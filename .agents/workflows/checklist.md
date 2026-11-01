# Slash Command Workflow: /checklist
Description: Generates and audits production release readiness checklists and quality sign-offs.

## Trigger
- User invokes `/checklist` before a release, PR merge, or deployment.

## Execution
Refer to the primary skill definition:
- [checklist SKILL.md](../skills/checklist/SKILL.md)

1. Review the 17-point production checklist across Specification, Simplicity, Security, Testing, and Runtime.
2. Verify all checklist criteria against automated test and audit evidence.
3. Emit sign-off decision (RELEASE READY or RELEASE BLOCKED).

