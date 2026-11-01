---
name: code-testing
description: "Runs deterministic automated test suites, negative security verifications, and regression tests. Supports pytest, targeted module runs, and unittest fallbacks."
---

# `/code-testing` — Deterministic Test Runner & Super-TDD Validator

> **Standard:** `docs/TESTING.md`, `skills/super-tdd.md`  
> **Harness:** Pytest with virtual environment dependencies

Use this slash command to execute tests, validate bug fixes, check negative security scenarios, or audit regression status.

---

## Pre-Flight Environment Checks
Before running tests, ensure the virtual environment and test environment variables are set:
```powershell
$env:JWT_SECRET_KEY = "test-secret-key-minimum-32-characters-for-hmac-sha256"
$env:ENVIRONMENT = "testing"
```

---

## Test Execution Commands

### 1. Full Pytest Suite (Default)
Run all unit, auth, security, and service tests:
```powershell
.venv\Scripts\python.exe -m pytest -v
```

### 2. Fast Fail Mode (Stop on First Error)
```powershell
.venv\Scripts\python.exe -m pytest -v -x
```

### 3. Targeted Module Execution
- **Auth & Cryptography Suite:**
  ```powershell
  .venv\Scripts\python.exe -m pytest tests/test_auth.py -v
  ```
- **Security & RBAC Boundary Suite:**
  ```powershell
  .venv\Scripts\python.exe -m pytest tests/test_security.py -v
  ```
- **Domain & Service Invariants:**
  ```powershell
  .venv\Scripts\python.exe -m pytest tests/test_services.py -v
  ```

### 4. Standard Library Fallback Harness
If pytest dependencies are unavailable, use Python's built-in unittest discoverer:
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Mandatory Test Invariants
When evaluating test runs:
1. **100% Pass Rate:** 0 failures, 0 errors, 0 unhandled warnings.
2. **Negative Test Assertion:** Ensure security tests verify denial on invalid tokens, expired sessions, rate breaches, and malformed schemas.
3. **Deterministic Execution:** No reliance on network access, non-mocked timers, or unstable random seeds.

