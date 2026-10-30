# Authentication & Access Control Subsystem (`auth/`)
> Standard: Zero-Trust, Spec-Driven Development (SDD), OWASP ASVS Level 2
> Reference: `specs/001-Spec-Security-guide.md` (AUTH-01 through AUTH-06, AC-01 through AC-04)

---

## 🏛️ Directory Architecture & File Manifest

```
auth/
├── README.md              # Subsystem overview, quickstart & integration contracts
├── SPEC.md                # Formal domain specifications, contracts & invariants (INV-AUTH-001 - 008)
├── THREAT_MODEL.md        # STRIDE analysis for authentication and session hijack vectors
├── RUNBOOK.md             # Incident response, credential rotation & lockout recovery runbook
├── __init__.py            # Package entrypoint and clean functional exports
├── models.py              # Domain models (AuthUser, UserRecord, TokenPair, Session, AuthResult)
├── passwords.py           # Memory-hard KDF (scrypt / PBKDF2), constant-time verify, strength checks
├── tokens.py              # Cryptographic token manager (HMAC-SHA256 signed JWTs & rotating refresh tokens)
├── session.py             # Server-side thread-safe session store with idle and absolute TTL
├── mfa.py                 # RFC 6238 TOTP 2FA engine & single-use recovery code manager
└── service.py             # Central AuthService orchestrating credentials, tokens, lockouts, RBAC
```

---

## 🔒 Security Capabilities & Guide Mapping

| Check ID | Requirement | Implementation Module | Technical Control |
|---|---|---|---|
| **AUTH-01** | Secure Authentication | `auth/service.py`, `auth/passwords.py` | Generic errors ("Invalid email or password"), dummy verification for non-existent users, lockout after 5 failures |
| **AUTH-02** | Password Storage | `auth/passwords.py` | scrypt (N=16384, r=8, p=1) and PBKDF2-HMAC-SHA256 (600,000 rounds); 16-byte random salt |
| **AUTH-03** | Password Reset & Recovery | `auth/service.py`, `auth/tokens.py` | CSPRNG reset tokens, single-use, 15-minute expiry, global session invalidation on reset |
| **AUTH-04** | Multi-Factor Authentication | `auth/mfa.py` | RFC 6238 TOTP 6-digit verification with drift tolerance, single-use hashed backup recovery codes |
| **AUTH-05** | Session & Token Security | `auth/tokens.py`, `auth/session.py` | HMAC-SHA256 signed JWTs (15m TTL), single-use rotating refresh tokens with family revocation on replay |
| **AUTH-06** | Account Takeover Defense | `auth/session.py`, `auth/service.py` | Active session tracking, user-driven session revocation, progressive lockout delays |
| **AC-01** | Role-Based Access Control | `auth/service.py` | Server-side `require_role()` checks; deny-by-default on unauthenticated requests |

---

## 🚀 Quickstart & Usage

### 1. User Registration & Password Hashing
```python
from auth import default_auth_service, UserRole

# Register user with automated strength validation
result = default_auth_service.register(
    email="alice@agentic.sdd",
    password="SecurePassword2026!#",
    role=UserRole.DEVELOPER
)
assert result.success
```

### 2. User Authentication & Token Generation
```python
login_res = default_auth_service.login(
    email="alice@agentic.sdd",
    password="SecurePassword2026!#"
)
print("Access Token:", login_res.tokens.access_token)
print("Refresh Token:", login_res.tokens.refresh_token)
```

### 3. Token Verification
```python
from auth import verify_token, require_role

user = verify_token(login_res.tokens.access_token)
if user and require_role(user, ["developer", "architect"]):
    print(f"Authorized user: {user.user_id} with role: {user.role}")
```

### 4. Single-Use Refresh Token Rotation
```python
# Rotate refresh token (old token is marked spent)
new_tokens = default_auth_service.refresh_token(login_res.tokens.refresh_token)
assert new_tokens is not None

# Replaying old refresh token triggers family revocation (AUTH-05 replay defense)
replay_attempt = default_auth_service.refresh_token(login_res.tokens.refresh_token)
assert replay_attempt is None
```

### 5. Multi-Factor Authentication (RFC 6238 TOTP)
```python
from auth import generate_totp_secret, generate_totp_code, verify_totp_code

secret = generate_totp_secret()
code = generate_totp_code(secret)
assert verify_totp_code(secret, code) is True
```

---

## 🧪 Testing Suite
Execute the full test suite verifying all 8 domain invariants and security checks:
```bash
python -m unittest discover -s tests -p "test_auth.py" -v
```
