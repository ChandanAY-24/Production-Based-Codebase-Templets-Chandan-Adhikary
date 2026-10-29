# SKILL: AST Security Scan (Static Analysis & OWASP Defense)
> Reference: [15. strix security]
> Standard: Automated AST Traversal & Vulnerability Detection

---

## 1. Scope & Capabilities
Scans all modified files before git commit to detect:
- Dangerous dynamic execution: `eval()`, `exec()`, `__import__()`, `os.system()` without shell escaping.
- Hardcoded secrets: High-entropy strings, AWS/GCP keys, JWT secrets, passwords.
- Path traversal vulnerabilities: Unsanitized string concatenations inside `open()` or `os.path.join()`.
- SQL injection: String formatting inside raw database queries.

---

## 2. Scan Execution
1. Invoke the scanner utility:
   ```bash
   python hooks/commit-guardian.py --ast-only
   ```
2. Interpret findings:
   - **BLOCK:** Immediate stop. Critical risk (e.g., hardcoded token or raw SQL formatting).
   - **WARN:** Review required. Unsafe casting or unbounded array allocation.
   - **PASS:** Clean code. Proceed with commit.
