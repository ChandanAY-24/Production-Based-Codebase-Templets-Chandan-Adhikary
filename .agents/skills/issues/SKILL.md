---
name: issues
description: "Generates, triages, and formats actionable tracking issues from tasks (docs/TASKS.md) or bug reproduction traces (docs/ERROR-HANDLING-TRACKER.md). Supports /issues and /issus."
---

# `/issues` — Issue Tracker, Task-to-Issue Generator & Bug Triage

> **Aliases:** `/issues`, `/issus`  
> **Sources:** `docs/TASKS.md`, `docs/ERROR-HANDLING-TRACKER.md`, `specs/`

Use this slash command to convert pending tasks or newly discovered bugs into standard, production-ready issue specifications for GitHub, GitLab, or local issue tracking.

---

## Issue Types & Taxonomy
- **`[Feature]`**: Spec-driven new capabilities or domain models.
- **`[Bug]`**: Broken invariant, regression, or failing test trace.
- **`[Security]`**: Vulnerability, rate limit breach, auth bypass, or AST finding.
- **`[Refactor]`**: Surgical code reduction, function line limit enforcement ($\le 40$ lines).

---

## Production Issue Template
When generating an issue, format it as follows:

```markdown
## Title: [TYPE] Concise description of the issue

### 1. Context & Spec Reference
- **Specification:** `specs/<id>.md` or `docs/SPEC.md#L...`
- **Related Task ID:** `TASK-XXX` (from `docs/TASKS.md`)
- **Severity / Priority:** P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)

### 2. Problem Statement / User Story
Clear, low-token description of the expected vs actual behavior or user journey.

### 3. Domain Invariants & Constraints
- `INV-001`: Zero unbounded mutations.
- `INV-004`: Diff size must remain <= 150 lines.
- Security constraints (e.g. rate limit, input schema validation, auth role).

### 4. Reproduction Steps (For Bugs)
```python
# Minimal deterministic reproduction script or failing test case
python -m pytest tests/test_security.py -k "test_unauthorized_access"
```

### 5. Definition of Done (DoD) Checklist
- [ ] Failing test authored in `tests/` verifying the contract (RED)
- [ ] Surgical implementation under 40 lines per function (GREEN)
- [ ] 100% test suite passing with zero regressions
- [ ] AST security scan and Commit Guardian verified (`hooks/commit-guardian.py`)
- [ ] Documentation updated in `docs/` and task marked `DONE`
```

---

## GitHub CLI Integration (Optional)
To export directly to GitHub issues via GitHub CLI (`gh`):
```bash
gh issue create \
  --title "[Security] Enforce sliding window rate limit on /api/v1/tasks" \
  --body-file issue.md \
  --label "security,P1-high"
```

