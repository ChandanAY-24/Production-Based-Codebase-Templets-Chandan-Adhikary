# SKILLS: Procedural Agent Task Workflows
> Directory: `skills/`
> Standard: Markdown-executable agent guidelines

---

## Skill Catalog & Trigger Index

| Skill File | Core Objective | Standard Reference | Typical Invocation Trigger |
|---|---|---|---|
| [`skills/grill-me.md`](file:///skills/grill-me.md) | Pre-implementation edge-case extraction interview | `[1. grill-me]` | Ambiguous spec, new feature request, `/grill-me` |
| [`skills/super-tdd.md`](file:///skills/super-tdd.md) | Red-Green-Refactor test cycle enforcement | `[2. superpowers]` | Bug fix, new function, API handler |
| [`skills/multi-model-review.md`](file:///skills/multi-model-review.md) | Consensus verification across external LLMs | `[5. claude-octopus]` | PR readiness, critical contract changes, `/octo:review` |
| [`skills/diff-patcher.md`](file:///skills/diff-patcher.md) | Exact unified diff formatting & validation | `[7. ponytail]` | Applying surgical code patches |
| [`skills/ui-polish.md`](file:///skills/ui-polish.md) | Micro-interactions, spacing, typography | `[12. impeccable / 16. emilkowalski]` | Frontend components, dialogs, button states |
| [`skills/db-migrate.md`](file:///skills/db-migrate.md) | Migration generation, execution & rollback | Database Ops | Schema evolution, new tables, column changes |
| [`skills/api-test-runner.md`](file:///skills/api-test-runner.md) | Headless E2E / integration test execution | `[11. playwright]` | Pre-merge verification, API contract validation |
| [`skills/ast-security-scan.md`](file:///skills/ast-security-scan.md) | Pre-commit security analysis & OWASP check | `[15. strix]` | Pre-commit check, dependency update |

---

## Operational Execution Standard
1. Read the corresponding `skills/<skill-name>.md` file prior to executing the task.
2. Adhere strictly to the required Inputs, Steps, Invariants, and Outputs.
3. Record progress and anomalies in `docs/ERROR-HANDLING-TRACKER.md`.
