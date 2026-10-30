"""
Comprehensive Unit Test Suite for auth/ Subsystem.
Reference: specs/001-Spec-Security-guide.md (AUTH-01 through AUTH-06, AC-01 through AC-04)
Tests:
- AUTH-01: Secure authentication, generic error messages, lockout prevention
- AUTH-02: Memory-hard password hashing (scrypt / PBKDF2), timing-safe verify, complexity
- AUTH-03: Single-use password reset tokens and session invalidation
- AUTH-04: RFC 6238 TOTP verification and single-use backup recovery codes
- AUTH-05: Access token JWT signing, expiration, and single-use refresh token rotation
- AUTH-06: Session lifecycle, idle and absolute timeout, user session revocation
- AC-01: Server-side role-based access control and deny-by-default
"""

import time
import unittest
from auth import (
    AuthService,
    UserRole,
    hash_password,
    verify_password,
    validate_password_strength,
    generate_totp_secret,
    generate_totp_code,
    verify_totp_code,
    generate_backup_codes,
    verify_and_consume_backup_code,
    TokenManager,
    SessionStore
)


class TestAuthSubsystem(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService(token_secret="test-secret-key-for-testing-only-12345")

    # --- AUTH-02: Password Hashing & Complexity Tests ---
    def test_password_strength_validation(self):
        """Verify strict password complexity requirements (min 12 chars, diversity)."""
        valid, _ = validate_password_strength("Short1!")
        self.assertFalse(valid)

        valid, _ = validate_password_strength("alllowercase1234567!")
        self.assertFalse(valid)

        valid, _ = validate_password_strength("ALLUPPERCASE1234567!")
        self.assertFalse(valid)

        valid, _ = validate_password_strength("NoSpecialChar1234567")
        self.assertFalse(valid)

        valid, _ = validate_password_strength("ValidPassword1234#$!")
        self.assertTrue(valid)

    def test_scrypt_hashing_and_verification(self):
        """Verify scrypt hashing produces valid modular format and verifies in constant time."""
        pwd = "ComplexP@ssw0rd2026!"
        h = hash_password(pwd, algorithm="scrypt")
        self.assertTrue(h.startswith("$scrypt$"))
        self.assertTrue(verify_password(pwd, h))
        self.assertFalse(verify_password("WrongPassword!", h))

    def test_pbkdf2_hashing_and_verification(self):
        """Verify PBKDF2 fallback hashing produces valid modular format and verifies."""
        pwd = "ComplexP@ssw0rd2026!"
        h = hash_password(pwd, algorithm="pbkdf2")
        self.assertTrue(h.startswith("$pbkdf2-sha256$"))
        self.assertTrue(verify_password(pwd, h))
        self.assertFalse(verify_password("WrongPassword!", h))

    # --- AUTH-01 & AUTH-06: Authentication & Account Lockout ---
    def test_user_registration_and_login(self):
        """Verify registration and subsequent login flow."""
        email = "bob@agentic.sdd"
        pwd = "BobSecureP@ssword2026!"
        reg = self.auth_service.register(email, pwd, role=UserRole.DEVELOPER)
        self.assertTrue(reg.success)

        login = self.auth_service.login(email, pwd)
        self.assertTrue(login.success)
        self.assertIsNotNone(login.tokens)
        self.assertIsNotNone(login.tokens.access_token)
        self.assertIsNotNone(login.tokens.refresh_token)

    def test_generic_error_on_unknown_user_or_bad_password(self):
        """Verify generic error message prevents user enumeration (AUTH-01)."""
        res_unknown = self.auth_service.login("nonexistent@agentic.sdd", "AnyPassword123!")
        self.assertFalse(res_unknown.success)
        self.assertEqual(res_unknown.error, "Invalid email or password")

        res_bad_pwd = self.auth_service.login("dev@agentic.sdd", "WrongPassword123!")
        self.assertFalse(res_bad_pwd.success)
        self.assertEqual(res_bad_pwd.error, "Invalid email or password")

    def test_account_lockout_after_max_failed_attempts(self):
        """Verify account lockout triggers after 5 failed login attempts (AUTH-06)."""
        email = "lockout_test@agentic.sdd"
        pwd = "LockoutTarget123#$"
        self.auth_service.register(email, pwd)

        for _ in range(4):
            res = self.auth_service.login(email, "WrongPassword1!")
            self.assertEqual(res.error, "Invalid email or password")

        # 5th attempt locks the account
        res5 = self.auth_service.login(email, "WrongPassword1!")
        self.assertIn("locked", res5.error.lower())

        # Even with correct password, login is blocked
        res_locked = self.auth_service.login(email, pwd)
        self.assertIn("locked", res_locked.error.lower())

    # --- AUTH-05: Tokens, Rotation & Replay Attack Protection ---
    def test_access_token_signature_and_expiration(self):
        """Verify access token verification and expiry rejection."""
        tm = TokenManager(secret_key="unit-test-secret")
        token = tm.create_access_token("u_test_01", "developer", ttl_seconds=2)
        claims = tm.verify_access_token(token)
        self.assertIsNotNone(claims)
        self.assertEqual(claims["sub"], "u_test_01")
        self.assertEqual(claims["role"], "developer")

        # Tampered token fails verification
        tampered = token[:-4] + "abcd"
        self.assertIsNone(tm.verify_access_token(tampered))

        # Expired token fails verification
        time.sleep(2.1)
        self.assertIsNone(tm.verify_access_token(token))

    def test_refresh_token_single_use_rotation(self):
        """Verify single-use refresh token rotation issuing new token pair."""
        login = self.auth_service.login("dev@agentic.sdd", "Developer@Agentic2026!")
        orig_refresh = login.tokens.refresh_token

        # First rotation succeeds
        rotated = self.auth_service.refresh_token(orig_refresh)
        self.assertIsNotNone(rotated)
        self.assertNotEqual(rotated.refresh_token, orig_refresh)

        # Second rotation with original spent token fails (replay detection)
        replay = self.auth_service.refresh_token(orig_refresh)
        self.assertIsNone(replay)

        # Furthermore, the token family was revoked, so rotated token also fails
        subsequent = self.auth_service.refresh_token(rotated.refresh_token)
        self.assertIsNone(subsequent)

    # --- AUTH-05 & AUTH-06: Session Lifecycle & Invalidation ---
    def test_session_idle_timeout(self):
        """Verify session invalidation after idle timeout threshold."""
        store = SessionStore(idle_timeout_seconds=1, absolute_timeout_seconds=10)
        s = store.create_session("u_test")
        self.assertIsNotNone(store.get_session(s.session_id))

        time.sleep(1.2)
        # Idle timeout exceeded
        self.assertIsNone(store.get_session(s.session_id))

    def test_session_revocation(self):
        """Verify user session revocation on logout."""
        store = SessionStore()
        s1 = store.create_session("u_user_99")
        s2 = store.create_session("u_user_99")

        self.assertEqual(len(store.list_user_sessions("u_user_99")), 2)
        store.revoke_session(s1.session_id)
        self.assertIsNone(store.get_session(s1.session_id))
        self.assertIsNotNone(store.get_session(s2.session_id))

        store.revoke_all_for_user("u_user_99")
        self.assertEqual(len(store.list_user_sessions("u_user_99")), 0)

    # --- AUTH-04: Multi-Factor Authentication (TOTP) ---
    def test_totp_generation_and_verification(self):
        """Verify RFC 6238 TOTP generation and drift window verification."""
        secret = generate_totp_secret()
        self.assertTrue(len(secret) >= 26)

        code = generate_totp_code(secret)
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

        # Verify correct code
        self.assertTrue(verify_totp_code(secret, code))

        # Bad code fails
        self.assertFalse(verify_totp_code(secret, "000000" if code != "000000" else "111111"))

    def test_backup_codes_single_use(self):
        """Verify backup recovery codes are consumed upon first use."""
        plaintext, hashed = generate_backup_codes(count=4)
        self.assertEqual(len(plaintext), 4)

        # Consume code 0
        valid, remaining = verify_and_consume_backup_code(plaintext[0], hashed)
        self.assertTrue(valid)
        self.assertEqual(len(remaining), 3)

        # Attempt to reuse consumed code 0
        valid_again, remaining2 = verify_and_consume_backup_code(plaintext[0], remaining)
        self.assertFalse(valid_again)
        self.assertEqual(len(remaining2), 3)

    # --- AC-01: Role-Based Access Control ---
    def test_require_role_enforcement(self):
        """Verify role validation denies unauthenticated and unauthorized users."""
        self.assertFalse(self.auth_service.require_role(None, ["developer"]))

        architect_user = self.auth_service.verify_token("sdd-dev-token-architect-2026")
        self.assertIsNotNone(architect_user)
        self.assertTrue(self.auth_service.require_role(architect_user, ["architect"]))
        self.assertFalse(self.auth_service.require_role(architect_user, ["developer"]))

        dev_user = self.auth_service.verify_token("sdd-dev-token-developer-2026")
        self.assertIsNotNone(dev_user)
        self.assertTrue(self.auth_service.require_role(dev_user, ["developer"]))
        self.assertFalse(self.auth_service.require_role(dev_user, ["architect"]))


if __name__ == "__main__":
    unittest.main()
