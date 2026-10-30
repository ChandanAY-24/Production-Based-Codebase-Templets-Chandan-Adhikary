"""
Password Hashing and Validation Service.
Reference: Spec/001-Spec-Security-guide.md (AUTH-02, CRYPTO-05, INP-01)
Enforces scrypt / PBKDF2-HMAC-SHA256, constant-time verification, and strong complexity bounds.
"""

import hashlib
import hmac
import os
import re
import secrets
from typing import Tuple

# Parameters for scrypt (RFC 7914 / OWASP recommendation)
SCRYPT_N = 16384  # CPU/memory cost
SCRYPT_R = 8      # Block size
SCRYPT_P = 1      # Parallelization parameter
SCRYPT_KEY_LEN = 32

# Fallback parameters for PBKDF2
PBKDF2_ITERATIONS = 600000
PBKDF2_ALGO = "sha256"

# Password complexity pattern: min 12 chars, upper, lower, number, special symbol
PASSWORD_COMPLEXITY_RE = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]).{12,128}$"
)

# Precomputed dummy hash for timing-attack mitigation (AUTH-01 / AUTH-02)
# When verifying against a non-existent user, this hash is verified to maintain constant execution time.
DUMMY_SALT = b"\x00" * 16
DUMMY_HASH = hashlib.scrypt(
    b"dummy_timing_mitigation_password",
    salt=DUMMY_SALT,
    n=SCRYPT_N,
    r=SCRYPT_R,
    p=SCRYPT_P,
    maxmem=32 * 1024 * 1024,
    dklen=SCRYPT_KEY_LEN
).hex()
DUMMY_STORED = f"$scrypt$ln=14,r={SCRYPT_R},p={SCRYPT_P}${DUMMY_SALT.hex()}${DUMMY_HASH}"


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate that password satisfies OWASP minimum security requirements (AUTH-01).
    Returns (is_valid, reason).
    """
    if not password or not isinstance(password, str):
        return False, "Password cannot be empty"

    if len(password) < 12:
        return False, "Password must be at least 12 characters long"

    if len(password) > 128:
        return False, "Password must not exceed 128 characters (DoS prevention)"

    if not PASSWORD_COMPLEXITY_RE.match(password):
        return False, "Password must contain uppercase, lowercase, numbers, and special characters"

    return True, ""


def hash_password(password: str, algorithm: str = "scrypt") -> str:
    """
    Hash password using cryptographically secure salt and memory-hard KDF (AUTH-02).
    Format:
      scrypt: $scrypt$ln=14,r=8,p=1$<salt_hex>$<hash_hex>
      pbkdf2: $pbkdf2-sha256$i=600000$<salt_hex>$<hash_hex>
    """
    salt = secrets.token_bytes(16)
    salt_hex = salt.hex()

    if algorithm == "scrypt":
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=SCRYPT_N,
            r=SCRYPT_R,
            p=SCRYPT_P,
            maxmem=32 * 1024 * 1024,
            dklen=SCRYPT_KEY_LEN
        )
        return f"$scrypt$ln=14,r={SCRYPT_R},p={SCRYPT_P}${salt_hex}${derived.hex()}"

    # Default to PBKDF2-HMAC-SHA256
    derived = hashlib.pbkdf2_hmac(
        PBKDF2_ALGO,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=32
    )
    return f"$pbkdf2-sha256$i={PBKDF2_ITERATIONS}${salt_hex}${derived.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify password against modular stored hash using constant-time comparison (CRYPTO-05).
    """
    if not stored_hash or not isinstance(stored_hash, str) or not password:
        return False

    parts = stored_hash.split("$")
    # Expected format: ['', algo, params, salt, hash]
    if len(parts) < 5:
        return False

    algo = parts[1]
    params_str = parts[2]
    salt_hex = parts[3]
    expected_hash_hex = parts[4]

    try:
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(expected_hash_hex)
    except ValueError:
        return False

    if algo == "scrypt":
        # Extract parameters
        # e.g., ln=14,r=8,p=1
        try:
            param_dict = dict(p.split("=") for p in params_str.split(","))
            ln = int(param_dict.get("ln", 14))
            n = 1 << ln
            r = int(param_dict.get("r", 8))
            p = int(param_dict.get("p", 1))
        except (ValueError, KeyError):
            n, r, p = SCRYPT_N, SCRYPT_R, SCRYPT_P

        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=n,
            r=r,
            p=p,
            maxmem=32 * 1024 * 1024,
            dklen=len(expected_hash)
        )
        return hmac.compare_digest(derived, expected_hash)

    elif algo == "pbkdf2-sha256":
        try:
            iterations = int(params_str.split("=")[1])
        except (ValueError, IndexError):
            iterations = PBKDF2_ITERATIONS

        derived = hashlib.pbkdf2_hmac(
            PBKDF2_ALGO,
            password.encode("utf-8"),
            salt,
            iterations,
            dklen=len(expected_hash)
        )
        return hmac.compare_digest(derived, expected_hash)

    return False


def verify_dummy_password(password: str) -> bool:
    """
    Executes dummy verification to maintain constant-time response on user-not-found (AUTH-01).
    Always returns False.
    """
    verify_password(password, DUMMY_STORED)
    return False
