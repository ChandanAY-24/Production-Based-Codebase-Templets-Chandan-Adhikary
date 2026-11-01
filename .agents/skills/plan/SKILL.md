---
name: plan
description: "Executes Recursive Epistemic Action (REA) and Spec-Driven Development (SDD) planning. Analyzes domain contracts, resolves ambiguities, defines test contracts, and decomposes features into atomic subtasks."
---

# `/plan` — Spec-Driven Architecture & Execution Planner

> **Engine:** Recursive Epistemic Action (REA) & Hierarchical Decomposition  
> **Standards:** `docs/PLAN.md`, `docs/SPEC.md`, `docs/CONSTITUTION.md`

Use this slash command when starting any new feature, architectural change, or non-trivial bugfix to establish formal contracts and prevent scope creep.

---

## Execution Protocol

### Step 1: Invariant & Memory Discovery
1. Read existing specifications and architecture contracts:
   - `docs/SPEC.md` and any domain specs in `specs/`
   - Active system invariants and data contracts in `src/` and `auth/`
   - Review core guardrails in `docs/CONSTITUTION.md` and `docs/RULES.md`
2. Identify dependencies, affected components, and external boundaries.

### Step 2: Epistemic Uncertainty & Clarification Gate
- If any business rule, data format, or security constraint is ambiguous:
  - **Halt immediately and invoke `/clarify`**.
  - Do not guess schema structures or trust loose assumptions.

### Step 3: Formal Specification Authoring
1. Author or update formal specification in `specs/` or `docs/SPEC.md` specifying:
   - Functional requirements & domain models
   - Invariants (e.g., `INV-001: Zero unbounded mutations`, `INV-004: Diff size <= 150 lines`)
   - Security constraints & input boundaries (Pydantic models, rate limits, RBAC)
   - OpenAPI request/response envelopes

### Step 4: Atomic Work Decomposition (P0 - P3)
Decompose execution into discrete subtasks in `docs/TASKS.md` and `docs/PLAN.md`:
- **P0 (Critical Path):** Schema models, core invariants, failing test contracts.
- **P1 (Core Implementation):** Surgical domain implementation, service logic.
- **P2 (Security & Boundary Hardening):** Negative tests, rate limits, audit logging.
- **P3 (Documentation & Review):** API contract sync, 5-gate consensus review.

### Step 5: Test Contract Establishment (Super-TDD Red Gate)
- Define exact failing test cases in `tests/` before generating implementation code.
- Ensure every positive test has at least one companion negative security test.

---

## Output Artifacts
When executing `/plan`, present:
1. **Feature Specification:** Link to `specs/<id>-<name>.md` or `docs/SPEC.md`.
2. **Execution Roadmap:** Phased milestones with explicit entry/exit criteria.
3. **Task Checklist:** Ready for ingestion by `/tasks`.

