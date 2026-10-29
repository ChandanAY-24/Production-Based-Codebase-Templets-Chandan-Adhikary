# AUTHENTICATION & SECURITY: Threat Models & Zero-Trust Policies
> Reference: [15. strix security]
> Standard: Zero-Trust, AST Security Analysis, Least Privilege

---

## 1. Threat Model & Attack Vectors
| Vector | Potential Impact | Mitigation Strategy |
|---|---|---|
| **Prompt Injection / Jailbreak** | Agent executing unintended shell or filesystem commands | Strict AST validation and execution sandbox via `connectors/openclaw-daemon/` |
| **Credential & Secret Leakage** | API keys or private certificates exposed in commits | `hooks/commit-guardian.py` regex scan + AST pattern matching |
| **Payload Injection (SQLi / XSS)** | Database corruption or client-side compromise | Parameterized queries only; automatic HTML escaping and strict Pydantic schemas |
| **Broken Object Level Auth (BOLA)** | User accessing another tenant's tasks | Row-level tenant isolation enforced in database queries |

---

## 2. Zero-Trust Architectural Constraints
1. **Never Trust Agent Context:** Tools must independently re-validate permissions and file paths. No path traversal (`../`) is permitted beyond the workspace root.
2. **Deterministic Token Verification:** API requests must pass asymmetric JWT or secure session token validation. Expired tokens are immediately rejected.
3. **AST Security Scanning:** All generated Python/JS code is scanned by `plugins/strix-security-mcp` before being staged in git. Calls to `eval()`, `exec()`, or unescaped subprocess shells are strictly forbidden.
