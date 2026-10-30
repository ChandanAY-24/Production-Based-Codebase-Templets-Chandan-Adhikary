"""
RFC 6238 Multi-Factor Authentication (TOTP) & Backup Code Engine.
Reference: Spec/001-Spec-Security-guide.md (AUTH-04, CRYPTO-05)
Standard-library RFC 6238 implementation with drift tolerance and single-use hashed recovery codes.
"""

import base64
import hashlib
import hmac
import secrets
import struct
import time
from typing import List, Tuple, Optional


def generate_totp_secret() -> str:
    """Generate a 160-bit (20 byte) Base32-encoded secret key (RFC 6238)."""
    random_bytes = secrets.token_bytes(20)
    return base64.b32encode(random_bytes).decode("utf-8").replace("=", "")


def generate_totp_code(secret: str, for_time: Optional[float] = None, interval: int = 30) -> str:
    """
    Generate 6-digit TOTP code for a given timestamp (defaults to now).
    Implements RFC 6238 / RFC 4226 HOTP algorithm.
    """
    current_time = for_time if for_time is not None else time.time()
    counter = int(current_time // interval)

    # Pad Base32 secret if needed
    secret_clean = secret.strip().upper()
    missing_padding = len(secret_clean) % 8
    if missing_padding:
        secret_clean += "=" * (8 - missing_padding)

    key = base64.b32decode(secret_clean, casefold=True)
    counter_bytes = struct.pack(">Q", counter)

    # Compute HMAC-SHA1
    hmac_digest = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # Dynamic truncation (RFC 4226 Section 5.4)
    offset = hmac_digest[-1] & 0x0F
    code_int = struct.unpack(">I", hmac_digest[offset:offset + 4])[0] & 0x7FFFFFFF
    code = code_int % 1000000

    return f"{code:06d}"


def verify_totp_code(secret: str, candidate_code: str, window: int = 1, interval: int = 30) -> bool:
    """
    Verify TOTP code within a drift window (default +/- 1 step = +/- 30s) using constant-time comparison.
    """
    if not candidate_code or len(candidate_code.strip()) != 6 or not candidate_code.strip().isdigit():
        return False

    clean_code = candidate_code.strip()
    now = time.time()

    for step in range(-window, window + 1):
        expected_code = generate_totp_code(secret, for_time=now + (step * interval), interval=interval)
        if hmac.compare_digest(clean_code.encode("utf-8"), expected_code.encode("utf-8")):
            return True

    return False


def generate_backup_codes(count: int = 8) -> Tuple[List[str], List[str]]:
    """
    Generate single-use backup recovery codes (AUTH-04).
    Returns (plaintext_codes_for_user, hashed_codes_for_storage).
    """
    plaintext_codes = []
    hashed_codes = []

    for _ in range(count):
        code = f"{secrets.token_hex(4)}-{secrets.token_hex(4)}"
        plaintext_codes.append(code)
        # Store as SHA-256 hash
        code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
        hashed_codes.append(code_hash)

    return plaintext_codes, hashed_codes


def verify_and_consume_backup_code(candidate_code: str, hashed_codes: List[str]) -> Tuple[bool, List[str]]:
    """
    Verify backup recovery code and remove it from the pool (single-use enforcement).
    Returns (is_valid, remaining_hashed_codes).
    """
    if not candidate_code:
        return False, hashed_codes

    candidate_hash = hashlib.sha256(candidate_code.strip().encode("utf-8")).hexdigest()
    matched_idx = -1

    for idx, stored_hash in enumerate(hashed_codes):
        if hmac.compare_digest(candidate_hash.encode("utf-8"), stored_hash.encode("utf-8")):
            matched_idx = idx
            break

    if matched_idx >= 0:
        remaining = [h for i, h in enumerate(hashed_codes) if i != matched_idx]
        return True, remaining

    return False, hashed_codes
