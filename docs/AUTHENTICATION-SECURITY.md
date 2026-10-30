# AUTHENTICATION & SECURITY: Threat Models & Zero-Trust Policies
> Reference: `specs/001-Spec-Security-guide.md`, `docs/SECURITY.md`, `docs/AUTH.md`  
> Standard: Zero-Trust, AST Security Analysis, Least Privilege  
> Detailed Documentation:
> - Complete Security Architecture & Controls: [SECURITY.md](SECURITY.md)
> - Authentication, Identity & RBAC Subsystem: [AUTH.md](AUTH.md)

---

## 1. Threat Model & Attack Vectors
| Vector | Potential Impact | Mitigation Strategy |
|---|---|---|
| **Prompt Injection / Jailbreak** | Agent executing unintended shell or filesystem commands | Strict AST validation and execution sandbox via `connectors/openclaw-daemon/` |
| **Credential & Secret Leakage** | API keys or private certificates exposed in commits | `hooks/commit-guardian.py` regex scan + AST pattern matching (`docs/SECURITY.md`) |
| **Payload Injection (SQLi / XSS)** | Database corruption or client-side compromise | Parameterized queries only; automatic HTML escaping and strict Pydantic schemas |
| **Broken Object Level Auth (BOLA / IDOR)** | User accessing another tenant's tasks or store data | Row-level tenant isolation enforced via `require_store_access` (`docs/AUTH.md`) |

---

## 2. Zero-Trust Architectural Constraints
1. **Never Trust Agent Context:** Tools must independently re-validate permissions and file paths. No path traversal (`../`) is permitted beyond the workspace root.
2. **Deterministic Token Verification:** API requests must pass asymmetric JWT or secure session token validation. Expired tokens are immediately rejected.
3. **AST Security Scanning:** All generated Python/JS code is scanned by `plugins/strix-security-mcp` before being staged in git. Calls to `eval()`, `exec()`, or unescaped subprocess shells are strictly forbidden.
4. **Comprehensive Guides:**
   - Refer to [SECURITY.md](SECURITY.md) for full Gate 3 checklist, AST scanner rules, and security incident response.
   - Refer to [AUTH.md](AUTH.md) for token lifecycle, scrypt KDF standards, RBAC matrix, and MFA / TOTP specifications.

