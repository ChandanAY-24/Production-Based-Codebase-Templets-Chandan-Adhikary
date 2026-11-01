---
name: tasks
description: "Manages active tasks, lifecycle state transitions, priority tracking (P0-P3), and subtask breakdowns on the docs/TASKS.md board."
---

# `/tasks` — Task Board & Lifecycle State Manager

> **Board Path:** `docs/TASKS.md`  
> **Lifecycle:** `PENDING` -> `IN_PROGRESS` -> `IN_REVIEW` -> `DONE` (or `BLOCKED`)

Use this slash command to review active work, transition task states, decompose complex user requests into atomic checklists, and ensure task traceability.

---

## Task Board Structure & Metadata
Every task in `docs/TASKS.md` adheres to the formal schema:

```markdown
### [TASK-XXX] <Concise Title>
- **Priority:** P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)
- **Status:** PENDING | IN_PROGRESS | IN_REVIEW | DONE | BLOCKED
- **Spec Reference:** `specs/<id>.md` or `docs/SPEC.md#L...`
- **Invariants:** List of non-negotiable boundaries (e.g. diff <= 150 lines, auth required)
- **Assignee:** [Agent Role / Engineer]
- **Subtask Checklist:**
  - [ ] Task contract authored in `tests/`
  - [ ] Minimal implementation in `src/` / `backend/`
  - [ ] 100% tests green
  - [ ] AST & commit guardian verified
```

---

## Execution Protocol

### 1. Board Inspection (`/tasks list`)
- Parse `docs/TASKS.md` to identify active backlog items, blocked tasks, and work in progress.
- Highlight any P0 items not yet in progress.

### 2. Task State Transition (`/tasks update <ID> <STATUS>`)
- Move task through the strict lifecycle:
  1. `PENDING` -> `IN_PROGRESS`: When implementation begins.
  2. `IN_PROGRESS` -> `IN_REVIEW`: When tests pass and PR/diff is ready.
  3. `IN_REVIEW` -> `DONE`: **Only** when `/code-review` confirms all 5 quality gates pass.
  4. Any -> `BLOCKED`: When an invariant is broken or an external dependency fails.

### 3. Task Decomposition (`/tasks add <Feature>`)
- Decompose new features into atomic tasks:
  - Each task must have a single clear deliverable.
  - Diff scope must not exceed 150 lines per task (`INV-004`).
  - Tasks must have clear acceptance criteria before work begins.

