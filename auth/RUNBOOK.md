# AUTH RUNBOOK: Incident Response, Credential Rotation & Session Management
> Standard: Operational Security & Threat Containment
> Reference: `specs/001-Spec-Security-guide.md` (LOG-05, SEC-04, CRYPTO-06, OPS-02)
> Target Package: `auth/`

---

## 1. Critical Escalation & Operational Contacts
- **Security Lead:** `security-lead@agentic.sdd`
- **Core Systems Architect:** `architect@agentic.sdd`
- **Identity & Access Management (IAM):** `auth-ops@agentic.sdd`

---

## 2. Standard Operating Procedures (SOPs)

### SOP-AUTH-01: User Credential Compromise & Revocation
When a developer or architect reports suspected credential exposure or token leakage:
1. **Identify the compromised user:**
   ```bash
   python -c "from auth import default_auth_service; print(default_auth_service.sessions.list_user_sessions('u_dev_01'))"
   ```
2. **Execute Emergency Session Invalidation:**
   ```python
   from auth import default_auth_service
   revoked = default_auth_service.sessions.revoke_all_for_user("u_dev_01")
   print(f"Terminated {revoked} active session(s).")
   ```
3. **Trigger Mandatory Password Reset:**
   - Invalidate existing password hash.
   - User must supply a fresh password conforming to `validate_password_strength()`.

---

### SOP-AUTH-02: Emergency Signing Secret Rotation
If the `AUTH_SIGNING_SECRET` or server environment is suspected of compromise:
1. **Generate New Cryptographically Secure Key:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. **Deploy New Secret:**
   - Update `AUTH_SIGNING_SECRET` environment variable in deployment orchestrator / `.env`.
   - Restart backend instances (`pkill -f backend/main.py; python backend/main.py`).
3. **Effect on Active Sessions:**
   - All existing access tokens become immediately invalid (signature mismatch).
   - Legitimate clients automatically exchange their refresh tokens or re-authenticate via `/auth/login`.

---

### SOP-AUTH-03: Replay Attack Containment
When a spent refresh token is submitted for rotation:
1. **Automated Containment:**
   - `TokenManager.rotate_refresh_token()` immediately deletes all refresh tokens in that `family_id`.
   - The response returns `None` (HTTP 401 Unauthorized).
2. **Investigation:**
   - Inspect audit logs for `TOKEN_ROTATION_REPLAY_DETECTED`.
   - Note client IP address and user-agent.
   - If the origin IP does not match known developer subnets, temporarily add to sliding window blocklist.

---

### SOP-AUTH-04: Account Lockout Release
When a legitimate developer is locked out due to accidental repeated failed logins (5 attempts):
1. **Verify Developer Identity via Secondary Channel (Slack / Voice / Security Lead).**
2. **Reset Failed Counter & Release Lock:**
   ```python
   from auth import default_auth_service
   user = default_auth_service._users.get("u_dev_01")
   if user:
       user.locked_until = None
       user.failed_login_attempts = 0
       print("User lockout cleared.")
   ```
