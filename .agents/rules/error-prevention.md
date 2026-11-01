# Error Prevention & Development Incident Registry Rule

> **Standard:** `Error-Tracker.xlsx`, `.agents/scripts/error-tracker.py`  
> **Mandate:** Zero-Regression & Systematic Error Elimination

All AI agents and developers modifying code in this repository MUST observe this rule to ensure errors encountered during development are never repeated.

---

## 1. Pre-Implementation Check
Before modifying any files in the repository:
1. Consult `Error-Tracker.xlsx` (or run `.venv\Scripts\python.exe .agents/scripts/error-tracker.py list`).
2. Verify if the target file or component has known failure modes (e.g., line-ending CRLF bugs, SQLite WAL concurrency, sandbox socket binding, type import omissions, or Windows terminal encoding).
3. Strictly adhere to the recorded **"Important checks & prevention rules"**.

---

## 2. Real-Time Incident Logging
When any new development error, runtime crash, linting breach, or test failure occurs during code generation:
1. Identify the root cause and formulate the surgical fix.
2. Verify the fix with an automated test or validator pass.
3. Append the error incident into `Error-Tracker.xlsx` via CLI:
   ```powershell
   .venv\Scripts\python.exe .agents/scripts/error-tracker.py add `
       --path "<affected-path>" `
       --phase "<Implementation|Testing|Code-Review|Deployment>" `
       --error "<describe error symptom & trace>" `
       --resolve "<how it was resolved>" `
       --verified "YES (<test command>)" `
       --checks "<invariant check to prevent recurrence>"
   ```

---

## 3. Required Schema Fields
Every incident logged must provide:
- **`Error-ID`**: Auto-assigned `ERR-XXX` unique identifier.
- **`Date-times`**: Timestamp of error occurrence.
- **`Which path`**: Path to the affected file or component.
- **`Which phase`**: Lifecycle phase (`Implementation`, `Testing`, `Code-Review`, `Environment/Hooks`, `Deployment`).
- **`Describe error`**: Exact error trace and failure symptom.
- **`How to resolve`**: Concrete resolution, patch, or architectural fix.
- **`Verified`**: Verification status (`YES` / `PENDING`) and verification method.
- **`Important checks & prevention rules`**: Invariants, guards, or checklist items to prevent repetition.

