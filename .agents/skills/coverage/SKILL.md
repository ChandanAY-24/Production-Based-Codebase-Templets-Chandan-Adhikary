---
name: coverage
description: "Audits test coverage across domain logic, auth, and backend modules. Highlights uncovered lines, enforces minimum coverage thresholds (85%+ domain, 95%+ auth), and detects blind spots."
---

# `/coverage` — Automated Test Coverage & Boundary Audit

> **Thresholds:** Domain Logic $\ge 85\%$, Auth & Crypto $\ge 95\%$  
> **Standard:** `docs/TESTING.md`

Use this slash command to measure code coverage, locate untested execution branches, and ensure critical security pathways are exercised by tests.

---

## Execution Protocol

### Step 1: Run Coverage via Pytest
Run pytest with coverage calculation across active codebase modules:

```powershell
# Set test environment
$env:ENVIRONMENT = "testing"

# If pytest-cov or coverage is available in venv:
.venv\Scripts\python.exe -m pytest --cov=src --cov=auth --cov=backend --cov-report=term-missing
```

### Step 2: Fallback Coverage Script
If pytest coverage plugins are not yet installed in the environment, install coverage into `.venv` or run:
```powershell
.venv\Scripts\python.exe -m pip install coverage pytest-cov
.venv\Scripts\python.exe -m pytest --cov=src --cov=auth --cov=backend --cov-report=term-missing
```

---

## Minimum Threshold Matrix

| Module / Scope | Minimum Required Coverage | Critical Paths |
|---|---|---|
| `auth/passwords.py`, `auth/tokens.py` | **$\ge 95\%$** | Scrypt KDF, JWT sign/verify, single-use refresh token revocation |
| `auth/session.py`, `auth/mfa.py` | **$\ge 90\%$** | TTL expiry, lockout counters, RFC 6238 TOTP window |
| `src/auth.py`, `src/rate_limiter.py` | **$\ge 90\%$** | Bearer auth header parsing, sliding window rate limiter |
| `src/services.py`, `src/models.py` | **$\ge 85\%$** | Task state transitions, invariants enforcement |
| `backend/main.py` | **$\ge 80\%$** | Health probes, error envelopes, security headers |

---

## Reporting Format
When `/coverage` completes, summarize:
```markdown
### Code Coverage Audit Report
| Module | Statements | Missing Lines | Coverage % | Status |
|---|---|---|---|---|
| `src/auth.py` | 45 | 2 | 95.5% | PASS |
| `src/services.py` | 60 | 4 | 93.3% | PASS |
| `backend/main.py` | 120 | 18 | 85.0% | PASS |

**Total Project Coverage:** 91.2% (Threshold: >= 85%) -> PASS

### Untested Branch Analysis
- `src/services.py:L78`: Rollback on concurrent conflict not exercised.
- `backend/main.py:L340`: Malformed patch boundary handler not exercised.
```

