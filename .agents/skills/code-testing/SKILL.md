---
name: code-testing
description: "Runs deterministic automated test suites, negative security verifications, and regression tests. Enforces test-writer and test-runner separation."
---

# `/code-testing` — Deterministic Test Suite & Super-TDD Validator

> **Standard:** `docs/TESTING.md`, `skills/super-tdd.md`  
> **Harness:** Pytest with virtual environment dependencies (unittest fallback)  
> **Order Invariant:** When automated workflows trigger, `code-testing` MUST execute BEFORE `code-review`.

Use this slash command to author and execute tests, validate bug fixes, check negative security scenarios, or audit regression status.

---

## 1. Sub-Component: test-writer (Super-TDD Test Authoring)

The `test-writer` sub-component is responsible for authoring and maintaining deterministic tests before or alongside code modifications:
- **Red-Green Contract:** Author tests that fail before the fix/feature, verifying test correctness.
- **Negative Security Verification:**
  - Unauthorized requests return `401 Unauthorized` or `InvalidTokenError`.
  - Expired tokens or invalid HMAC-SHA256 signatures are rejected immediately.
  - Rate limit breaches trigger `429 Too Many Requests`.
  - Malformed or oversized payloads trigger `422 Unprocessable Entity`.
- **Mock Transports:** Use mock sockets and deterministic seeds to ensure zero reliance on external networks or unpinned system states.
- **Test Locations:**
  - `tests/test_auth.py`: JWT, PBKDF2/scrypt, session lifecycle.
  - `tests/test_security.py`: RBAC, input validation, security headers, rate limiting.
  - `tests/test_services.py`: Domain tasks and business logic contracts.

---

## 2. Sub-Component: test-runner (Automated Harness Execution)

The `test-runner` sub-component executes the test suite with strict pass/fail guarantees:

### Pre-Flight Environment Setup
```powershell
$env:PYTHONPATH = "."
$env:ENVIRONMENT = "testing"
$env:JWT_SECRET_KEY = "test-secret-key-minimum-32-characters-for-hmac-sha256"
```

### Full Pytest Suite (Default)
```powershell
.venv\Scripts\python.exe -m pytest -v
```

### Fast-Fail Mode (Stop on First Error)
```powershell
.venv\Scripts\python.exe -m pytest -v -x
```

### Targeted Module Execution
```powershell
# Auth suite
.venv\Scripts\python.exe -m pytest tests/test_auth.py -v

# Security & RBAC suite
.venv\Scripts\python.exe -m pytest tests/test_security.py -v

# Domain & Service Invariants
.venv\Scripts\python.exe -m pytest tests/test_services.py -v
```

### Unittest Fallback Harness
If pytest runtime is unavailable:
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Mandatory Test Invariants
1. **100% Pass Rate:** 0 failures, 0 errors, 0 unhandled warnings.
2. **Negative Test Assertion:** Every security boundary must be covered by a negative assertion test.
3. **Deterministic Execution:** No network calls, non-mocked timers, or unstable randomness.
