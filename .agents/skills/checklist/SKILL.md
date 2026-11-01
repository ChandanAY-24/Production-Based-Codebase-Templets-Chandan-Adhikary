---
name: checklist
description: "Generates and audits production release readiness checklists, security sign-offs, and quality gate verifications. Ensures zero unverified deployments."
---

# `/checklist` — Production Release Readiness & Quality Sign-Off Checklist

> **Purpose:** Release gate sign-off, deployment checklists, and invariant audits  
> **Reference:** `docs/CODE-REVIEW.md`, `specs/001-Spec-Security-guide.md`, `specs/002-Spec-Git-Workflow-Rules.md`

Use this slash command before merging a pull request, tagging a milestone release, or deploying code to verify that all release invariants are fulfilled.

---

## Production Release Checklist

Review each item. Mark `[x]` **only** when verified with test/audit evidence:

### 1. Specification & Contract Alignment
- [ ] **CHK-001:** Change explicitly traces to a task ID in `docs/TASKS.md` and a contract in `docs/SPEC.md` or `specs/`.
- [ ] **CHK-002:** Invariants verified (zero unbounded mutations `INV-001`, deterministic rollback `INV-002`).
- [ ] **CHK-003:** API request/response envelopes conform strictly to global JSON structure in `docs/APIS.md`.

### 2. Code Simplicity & Surgical Boundaries
- [ ] **CHK-004:** Function lengths comply with Karpathy simplicity guidelines ($\le 40$ lines per function).
- [ ] **CHK-005:** Max nesting depth $\le 2$; code fails fast with early returns.
- [ ] **CHK-006:** Total patch size $\le 150$ contiguous lines (`INV-004`).
- [ ] **CHK-007:** Zero dead code, unused imports, or temporary debug prints.

### 3. Security, AST & Cryptography (Gate 3)
- [ ] **CHK-008:** Commit Guardian and AST scan pass with zero violations (`python hooks/commit-guardian.py --ast-only`).
- [ ] **CHK-009:** Zero hardcoded secrets, API tokens, or credentials in git history.
- [ ] **CHK-010:** Strict input validation enforced via Pydantic schemas on all external endpoints.
- [ ] **CHK-011:** Mandatory security headers verified (`X-Content-Type-Options: nosniff`, RFC 9116 security.txt).
- [ ] **CHK-012:** Rate limiting active on all entrypoints (Sliding window rate limiter).

### 4. Super-TDD & Testing Verification (Gate 4)
- [ ] **CHK-013:** 100% of automated tests passing in `.venv` (`.venv\Scripts\python.exe -m pytest -v`).
- [ ] **CHK-014:** At least one negative security test authored for every new route or permission rule.
- [ ] **CHK-015:** Code coverage meets or exceeds threshold ($\ge 85\%$ domain, $\ge 95\%$ auth).

### 5. Local Runtime & Smoke Verification
- [ ] **CHK-016:** Local pre-deployment smoke checks pass cleanly (`.venv\Scripts\python.exe .agents/scripts/smoke-runner.py`).
- [ ] **CHK-017:** Frontend Content Security Policy verified with zero console errors.

### 6. Performance & Scalability (15 Distributed Pillars)
> Reference: `docs/PERFORMANCE-SCALABILITY-CHECKS.md`
- [ ] **CHK-018 (Scalability & Statelessness):** Shared-nothing architecture; zero local server session storage; connection pool capped.
- [ ] **CHK-019 (Availability & Probes):** Multi-AZ deployment verified; `/health` liveness and readiness probes active.
- [ ] **CHK-020 (Reliability & Idempotency):** `Idempotency-Key` supported on mutations; saga/rollback logic tested.
- [ ] **CHK-021 (Fault Tolerance & Resilience):** Circuit breakers on external APIs; jittered exponential backoff; sliding-window rate limiters.
- [ ] **CHK-022 (Latency & Throughput):** p95 latency $\le 500\text{ms}$; database queries $\le 50\text{ms}$; zero N+1 loops; async I/O.
- [ ] **CHK-023 (Consistency & Durability):** Strong vs eventual consistency explicit; WAL fsync verified; backups tested.
- [ ] **CHK-024 (Partition & CAP):** Consensus quorum $\ge 3$ nodes; fencing tokens on locks; CAP trade-offs documented.
- [ ] **CHK-025 (Scaling & Balancing):** Least-connections/round-robin LB; no sticky sessions; auto-scaling metrics and cooldowns set.

---

## Sign-Off Decision
- **RELEASE READY:** All 25 checks marked `[x]`.
- **RELEASE BLOCKED:** Any item unchecked. Document exact failure in `docs/ERROR-HANDLING-TRACKER.md`.

