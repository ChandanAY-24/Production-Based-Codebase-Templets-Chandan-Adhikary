---
name: implement
description: "Executes surgical, deterministic code implementation using Super-TDD (Red-Green-Refactor) and Karpathy simplicity rules. Enforces contiguous diffs, function size <= 40 lines, and pre-commit security gates."
---

# `/implement` — Surgical Super-TDD Code Implementation

> **Methodology:** Super-TDD (Red-Green-Refactor)  
> **Directives:** `docs/CONSTITUTION.md`, `docs/RULES.md`, `skills/super-tdd.md`

Use this slash command to implement a specific subtask defined in `docs/TASKS.md` or a formal specification contract.

---

## Pre-Conditions
1. An active task ID must exist in `docs/TASKS.md` in state `PENDING` or `IN_PROGRESS`.
2. The domain specification and schema invariants must be documented in `specs/` or `docs/SPEC.md`.

---

## Execution Protocol

### Phase 1: RED (Failing Test Creation)
1. Navigate to `tests/` and create or append the test case enforcing the specification contract.
2. Run the test suite using pytest:
   ```powershell
   .venv\Scripts\python.exe -m pytest tests/test_<module>.py -v
   ```
3. **Verify RED:** The test MUST fail with an expected assertion error or missing symbol. Do not proceed until failure is confirmed.

### Phase 2: GREEN (Minimal Surgical Implementation)
1. Write the minimal contiguous code necessary to turn the test green.
2. Adhere strictly to the **Karpathy Simplicity Directives**:
   - Keep functions under 40 lines.
   - Max nesting depth: 2 (fail fast, return early).
   - Zero speculative abstractions (YAGNI).
   - Domain logic in `src/` must remain independent of presentation/controller layers.
3. Run the test suite:
   ```powershell
   .venv\Scripts\python.exe -m pytest tests/test_<module>.py -v
   ```
4. **Verify GREEN:** Confirm all tests pass.

### Phase 3: REFACTOR & HARDEN
1. Remove all dead code, unused imports, temporary prints, and commented-out blocks.
2. Ensure diff size does not exceed 150 lines (`INV-004`).
3. Add companion negative tests (invalid input types, unauthenticated access, rate breaches).

### Phase 4: Gate 3 Security Pre-Flight
Execute local security and AST scans:
```powershell
python hooks/commit-guardian.py --ast-only
```
Verify zero AST violations, zero secret leaks, and strict schema compliance.

---

## Post-Execution
- Transition task in `docs/TASKS.md` to `IN_REVIEW`.
- Hand off to `/code-review` for 5-gate quality sign-off.

