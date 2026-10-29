# SKILL: API & E2E Test Runner (Playwright & Headless Integration)
> Reference: [11. playwright]
> Purpose: Automated contract and browser-driven end-to-end test execution

---

## 1. When to Use
- Validating REST API endpoints against contracts in `docs/APIS.md`.
- Running headless browser flows for critical user paths (auth, task creation, review).
- Pre-release smoke testing.

---

## 2. API Contract Verification
1. Run backend server in isolated test mode.
2. Execute automated API test suite:
   ```bash
   pytest tests/api/ -v
   ```
3. Assert status codes, envelope shape (`{ success, data, error, meta }`), and header invariants.

---

## 3. Playwright E2E Execution
1. Ensure Playwright headless drivers are ready:
   ```bash
   npx playwright test --headed=false
   ```
2. Verify visual regression snapshots, console error counts (must be 0), and network request statuses.
3. Attach screenshot artifacts of any failure to `docs/reference-artifacts/`.
