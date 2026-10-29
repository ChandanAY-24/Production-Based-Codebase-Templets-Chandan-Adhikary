# SKILL: Multi-Model Review (Consensus Verification)
> Reference: [5. claude-octopus]
> Protocol: Distributed Model Ensemble Arbitration

---

## 1. When to Trigger
- Any pull request or diff modifying > 150 lines of code.
- Core authentication, cryptography, or security rule updates.
- Database schema changes involving migrations with potential data loss risk.
- Milestone phase transitions defined in `docs/PHASES.md`.

---

## 2. Review Ensemble Matrix
| Reviewer Role | Primary Focus | Criteria |
|---|---|---|
| **Architect Auditor** | Contract & Domain Invariants | Conformance to `docs/SPEC.md` |
| **Security Sentinel** | AST, Injection & Leakage | Zero-trust compliance in `docs/AUTHENTICATION-SECURITY.md` |
| **Simplicity Sentry** | Karpathy Rules | Minimal diff size, zero dead code, `docs/RULES.md` |
| **QA Arbiter** | Test coverage & Edge Cases | Red-Green evidence in `skills/super-tdd.md` |

---

## 3. Consensus Protocol
1. **Prepare Review Packet:**
   - Unified git diff.
   - Associated spec clause from `docs/SPEC.md`.
   - Test execution logs.
2. **Dispatch Review Packet:**
   - Send review payload across distinct model backends via `plugins/omniroute-proxy`.
3. **Collate Votes:**
   - Consensus requires >= 75% approval (`APPROVE`) with ZERO hard security blocks (`VETO`).
4. **Action:**
   - If approved: Proceed to `hooks/commit-guardian.py`.
   - If rejected: Return issues to developer agent with line-specific remediation steps.
