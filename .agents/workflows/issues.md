# Slash Command Workflow: /issues (Alias: /issus)
Description: Generates, triages, and formats actionable tracking issues from tasks or bug traces.

## Trigger
- User invokes `/issues` or `/issus` to synthesize tasks into structured issues or file bug reports.

## Execution
Refer to the primary skill definition:
- [issues SKILL.md](../skills/issues/SKILL.md)

1. Extract task from `docs/TASKS.md` or bug trace from `docs/ERROR-HANDLING-TRACKER.md`.
2. Format issue using the production issue template (Context, Invariants, Reproduction, Definition of Done).
3. Optionally dispatch via GitHub CLI (`gh issue create`).

