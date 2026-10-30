# SECURITY: Architecture, Threat Models & Production Security Controls
> Reference: `specs/001-Spec-Security-guide.md`, `security/THREAT_MODEL.md`, `security/SECURITY_REPORT.md`  
> Compliance Standard: Zero-Trust, AST Verification, Gate 3 Quality Checklist

---

## 1. Security Architecture & Threat Topology

The system operates under a strict **Zero-Trust Security Model**. Every agent execution, API request, database query, and code diff is treated as untrusted until cryptographically verified and bounded by explicit contracts.

```mermaid
graph TD
    Client([Client / Agent]) -->|HTTPS + Bearer Token| Gate[Reverse Proxy / Hardening Gate]
    Gate -->|Security Headers, Rate Limiting| AuthBridge[Auth & Token Verification]
    AuthBridge -->|Constant-Time Check| RBAC[Role & Tenant Scoping]
    RBAC -->|Validated Principal| Router[API Route Handlers]
    Router -->|Pydantic Bounds Check| Domain[src/ Core Logic]
    Domain -->|Parameterized Queries| DB[(Database / SQLite / Vector DB)]
    
    subgraph Pre-Commit Hardening
        GitStaging[Git Staged Changes] --> Guardian[hooks/commit-guardian.py]
        Guardian -->|Regex Scan| SecretCheck{Secret Leaks?}
        Guardian -->|AST Parse| AstCheck{eval/exec/shell=True?}
        Guardian -->|Pass| CommitAllowed[Commit Permitted]
    end
```

---

## 2. Gate 3 Quality Checklist (Mandatory for Every Diff)

Every pull request and code modification must satisfy the **Gate 3 Validation Checklist** (`specs/002-Spec-Git-Workflow-Rules.md`):

| Check Code | Category | Requirement | Enforcement Mechanism |
|---|---|---|---|
| **AUTH-01** | Authentication | All `/api/*` endpoints require authentication dependencies (`Depends(get_current_user)`), except `/health` and `/.well-known/security.txt`. | `backend/main.py`<br/>`src/auth.py` |
| **IDOR-01** | Multi-Tenancy | Every access to a store or user-owned object must verify access via `require_store_access(store_id, principal)` or `principal.can_access_store(...)`. | `src/auth.py`<br/>`src/services.py` |
| **SEC-01** | Secret Leaks | No secrets, credentials, API keys, private keys, or `.env` entries staged in git. `git status` must never list sensitive files. | `hooks/commit-guardian.py` |
| **INP-01** | Input Validation | All request bodies and query parameters validated via bounded Pydantic models (`max_length`, `ge/le`, strict types). | `src/schemas.py` |
| **INP-02** | Upload Bounds | File uploads capped at `MAX_UPLOAD_BYTES` (10 MB) with magic-byte file signature verification. | `backend/main.py` |
| **WEB-01** | Web Hardening | Security headers applied to all responses: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`. | `backend/main.py` |
| **WEB-02** | CORS Restrictions | Explicit origin whitelist enforced. Wildcard `Access-Control-Allow-Origin: *` is strictly forbidden. | `backend/main.py` |
| **TEST-01**| Negative Tests | At least one negative test included for every new security control in `tests/test_security.py` or `tests/test_auth.py`. | Pytest Suite |

---

## 3. Abstract Syntax Tree (AST) Security Rules

The AST Security Scanner (`skills/ast-security-scan.md` and `hooks/commit-guardian.py`) inspects all Python and JavaScript source files before staging:

1. **Prohibited Dynamic Execution:**
   - Any invocation of `eval()`, `exec()`, or `compile()` raises a fatal pre-commit error.
   - Dynamic `__import__()` with user-supplied arguments is blocked.
2. **Subprocess Shell Prohibition:**
   - `subprocess.Popen(..., shell=True)` and `os.system()` are strictly forbidden.
   - Subprocess calls must pass explicit argument lists without shell wrappers.
3. **Filesystem Traversal Guard:**
   - All filesystem operations must resolve canonical paths (`os.path.realpath`) and assert that targets reside within the authorized workspace root.
   - Sequences containing `../` or unvalidated path concatenation are blocked.

---

## 4. Secret Management & Staged File Protection

### Protected Patterns:
The commit guardian scans staged diffs against patterns matching:
- High-entropy tokens (`[A-Za-z0-9_-]{32,}`)
- Private keys (`-----BEGIN PRIVATE KEY-----`, `-----BEGIN RSA PRIVATE KEY-----`)
- Provider API keys (`sk_live_`, `ghp_`, `xoxb-`, `AIzaSy`)
- Database connection URLs containing passwords (`postgres://user:pass@host/db`)

### Git Status Rules:
- Staging `.env`, `.env.local`, `*.key`, `*.pem`, or `credentials.json` causes immediate commit rejection.
- Developers must use `.env.example` with sanitized placeholders.

---

## 5. Security Incident Response & Runbook

In the event of an identified security anomaly or credential compromise:

1. **Containment:** Immediately invoke `security/RUNBOOK.md` rotation procedure:
   - Revoke compromised bearer tokens via `AuthService.revoke_user_sessions(user_id)`.
   - Rotate `JWT_SECRET_KEY` in environment configuration.
2. **Audit & Trace:** Review audit logs in `logger.py` for unauthorized access traces and IDOR attempts.
3. **Remediation & TDD:** Implement a regression test in `tests/test_security.py` reproducing the attack vector, patch the vulnerability surgically, and verify 100% test pass.
4. **Vulnerability Disclosure:** Inquiries and responsible disclosures should follow instructions at `/.well-known/security.txt`.

