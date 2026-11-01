# Slash Command Workflow: /code-review
Description: Executes the Five Quality Gates with Security Review and Code Quality Review.

> **Order Invariant:** Automated triggers execute `code-testing` FIRST. Only after tests pass does `code-review` run.

## Trigger
- User invokes `/code-review` on a PR, commit, or uncommitted workspace diff.

## Execution
Refer to the primary skill definition:
- [code-review SKILL.md](../skills/code-review/SKILL.md)

1. **Verify Prerequisite:** Ensure all tests from `/code-testing` are 100% green.
2. **Execute Security Review:** Run AST scan & secret checks via `python hooks/commit-guardian.py --ast-only`.
3. **Execute Code Quality Review:** Run Flake8 static analysis and Karpathy simplicity audits.
4. **Emit Five Quality Gates Verdict:** Output structured `[APPROVE | REQUEST_CHANGES | BLOCK]` report.
