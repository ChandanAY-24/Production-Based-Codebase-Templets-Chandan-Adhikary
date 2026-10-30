# Security Runbook & Incident Response Plan
Reference: specs/001-Spec-Security-guide.md (LOG-05, SEC-04, PRIV-08, CRYPTO-06, OPS-02)
Project: Spec-Driven Development (SDD) & Agentic Coding Framework

---

## 1. Contacts
- **Incident Lead:** Antigravity Security Lead (`security-lead@agentic.sdd`)
- **Engineering Backup:** Core Systems Architect (`architect@agentic.sdd`)
- **Hosting / Infra Support:** Local Host Admin / Infrastructure Operations
- **Payment Provider:** N/A (Not configured)
- **Legal & Privacy Counsel:** Data Protection Officer (`privacy@agentic.sdd`)
- **Regulatory Contacts:**
  - **CERT-In:** `incident@cert-in.org.in` | Phone: +91-1800-11-4949
  - **Data Protection Board (DPDP):** Designated portal / registry

---

## 2. Severity Levels & Response Gates
| Severity | Definition | Response SLA | Release Gate |
|---|---|---|---|
| **Critical** | Live secret leak, unauthenticated RCE, auth bypass, arbitrary data tampering | Immediate (< 1 hour) | **Block Release** |
| **High** | BOLA/IDOR, missing rate limiting on auth, mass data exposure, CSRF | < 4 hours | **Block Release** (unless waiver signed) |
| **Medium** | Missing security headers, verbose internal errors, weak logging | < 24 hours | Fix before next sprint |
| **Low** | Minor configuration hardening, backlog audit updates | < 7 days | Backlog tracking |

---

## 3. Containment Checklist
When a security incident or compromise is suspected, execute the following containment sequence:
- [ ] **1. Revoke & Rotate Credentials:** Rotate compromised API tokens, database passwords, or JWT secrets immediately.
- [ ] **2. Invalidate Sessions:** Clear active session tokens and force client re-authentication.
- [ ] **3. Feature Flag Disablement:** Use configuration flags to shut down affected endpoints without full server teardown.
- [ ] **4. Block Offending IPs:** Add malicious IP addresses to transport firewall or rate-limiter blocklist.
- [ ] **5. Snapshot & Evidence Preservation:** Preserve server audit logs (`[AUDIT]` streams), database state, and network traces before applying hotfixes.

---

## 4. Breach Notification Deadlines
- **CERT-In (India):** Mandatory notification within **6 hours** of noticing specified cyber security incidents.
- **DPDP Act (India):** Notice to Data Protection Board and affected Data Principals **without delay**, with comprehensive incident report within **72 hours**.
- **GDPR (EU):** Supervisory authority notification within **72 hours** of becoming aware of a personal data breach.
- **Notification Template:**
  ```text
  Incident Notice: [INCIDENT-ID]
  Time of Occurrence: [UTC Timestamp]
  Nature of Breach: [Description of affected data and components]
  Estimated Impact: [Number of users / records affected]
  Containment Measures Applied: [Credentials rotated, endpoints blocked]
  Remediation Next Steps: [Patches, audits, customer outreach]
  Contact Person: Antigravity Security Lead (security-lead@agentic.sdd)
  ```

---

## 5. Recovery & Disaster Procedures
- **RPO (Recovery Point Objective):** 1 hour for local SQLite database backups.
- **RTO (Recovery Time Objective):** < 15 minutes to redeploy from git repository.
- **Restoration Sequence:**
  1. Terminate compromised running instances (`pkill -f backend/main.py`).
  2. Verify clean git checkout against verified commit SHA (`git checkout <sha>`).
  3. Restore SQLite database snapshot from verified backup directory.
  4. Run migrations check: `python database/migrations/...`.
  5. Run Super-TDD and Security test suites: `python -m unittest discover -s tests -p "test_*.py" -v`.
  6. Relaunch hardened server: `python backend/main.py`.

---

## 6. Secret Rotation Procedures (SEC-04)
1. **API Tokens (`API_TOKENS`):**
   - Generate new cryptographically secure 256-bit token: `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
   - Update `.env` or deployment secret store with new token.
   - Retain dual-token overlap window for max 2 hours to avoid client disruption.
   - Deprecate old token and verify rejection in test suite.
2. **Database Keys & Local Stores:**
   - Terminate SQLite connections, rename/archive `app.db`, initialize fresh schema via `database/migrations/`.

---

## 7. Periodic Logs & Review Audits
- **Backup Restore Test Log (CRYPTO-06):** Conducted quarterly; last verified restore test: 2026-10-30.
- **Access & Role Review Log (OPS-02):** Quarterly review of developer and architect identities; last reviewed: 2026-10-30.
