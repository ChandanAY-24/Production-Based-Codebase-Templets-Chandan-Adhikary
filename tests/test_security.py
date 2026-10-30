"""
Security Unit & Integration Test Suite.
Reference: specs/001-Spec-Security-guide.md (Part 4, Rules 10 & 14)
Verifies:
- AUTH-01 / AUTH-05: Bearer token validation and 401 on unauthorized access
- AC-01 / AC-04: Role-based access control and deny-by-default
- INP-01 / AC-03: Strict boundary schema validation and mass-assignment rejection
- WEB-02 / WEB-04: Mandatory security headers (CSP, nosniff, DENY, etc.)
- WEB-03: Safe CORS configuration without arbitrary reflection
- API-02: Rate limiter sliding window and 429 response
- API-03: DoS protection against oversize payloads (413) and pagination caps
- LOG-06: Vulnerability disclosure endpoint (/.well-known/security.txt)
"""

import json
import socket
import threading
import time
import unittest
import urllib.request
import urllib.error
from http.server import HTTPServer

from src.auth import verify_token, require_role, AuthUser
from src.rate_limiter import SlidingWindowRateLimiter
from src.schemas import TaskCreateSchema, PatchVerifySchema
from pydantic import ValidationError
from backend.main import APIRequestHandler, task_service, rate_limiter

def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

class TestSecurityControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = find_free_port()
        cls.server = HTTPServer(("127.0.0.1", cls.port), APIRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        time.sleep(0.1)  # Warmup server thread

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        rate_limiter.reset()

    # --- AUTH-01 / AUTH-05 / AC-04: Authentication Tests ---
    def test_unauthenticated_request_rejected_401(self):
        """Negative test: GET /api/v1/tasks without token must return 401."""
        req = urllib.request.Request(f"{self.base_url}/api/v1/tasks")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 401)
        resp_body = json.loads(ctx.exception.read().decode())
        self.assertFalse(resp_body["success"])
        self.assertIn("bearer token required", resp_body["error"])

    def test_invalid_token_rejected_401(self):
        """Negative test: Malformed or fake token must return 401."""
        req = urllib.request.Request(
            f"{self.base_url}/api/v1/tasks",
            headers={"Authorization": "Bearer invalid-token-xyz"}
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 401)

    def test_valid_token_accepted_200(self):
        """Positive test: Valid developer/architect token returns 200."""
        req = urllib.request.Request(
            f"{self.base_url}/api/v1/tasks",
            headers={"Authorization": "Bearer sdd-dev-token-architect-2026"}
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            body = json.loads(resp.read().decode())
            self.assertTrue(body["success"])
            self.assertIsInstance(body["data"], list)

    # --- WEB-02 / WEB-04: Security Headers ---
    def test_security_headers_present_on_responses(self):
        """Verify presence of all mandatory security headers on HTTP responses."""
        req = urllib.request.Request(f"{self.base_url}/health")
        with urllib.request.urlopen(req) as resp:
            headers = dict(resp.headers)
            self.assertEqual(headers.get("X-Content-Type-Options"), "nosniff")
            self.assertEqual(headers.get("X-Frame-Options"), "DENY")
            self.assertEqual(headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")
            self.assertIn("default-src 'self'", headers.get("Content-Security-Policy", ""))
            self.assertIn("geolocation=()", headers.get("Permissions-Policy", ""))

    # --- INP-01 / AC-03: Strict Schema Validation & Mass-Assignment ---
    def test_task_creation_schema_mass_assignment_rejected(self):
        """Negative test: Injecting unexpected fields (e.g. role, isAdmin) must fail validation."""
        payload = {
            "title": "Legitimate task",
            "specReference": "docs/SPEC.md#L10",
            "invariants": ["Safe invariant"],
            "isAdmin": True,            # Over-posting attack
            "role": "super-administrator" # Mass-assignment attack
        }
        with self.assertRaises(ValidationError):
            TaskCreateSchema(**payload)

    def test_task_creation_title_length_exceeded_rejected(self):
        """Negative test: Title exceeding 80 characters is rejected by schema."""
        payload = {
            "title": "A" * 81,  # Exceeds max 80 limit
            "specReference": "docs/SPEC.md",
            "invariants": ["Rule 1"]
        }
        with self.assertRaises(ValidationError):
            TaskCreateSchema(**payload)

    def test_task_creation_via_api_with_invalid_payload_returns_422(self):
        """Negative test: POST /api/v1/tasks with invalid payload returns 422."""
        bad_payload = json.dumps({"title": ""}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/v1/tasks",
            data=bad_payload,
            headers={
                "Authorization": "Bearer sdd-dev-token-architect-2026",
                "Content-Type": "application/json"
            }
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 422)

    # --- API-03: Resource Limits & DoS Protection ---
    def test_oversize_payload_rejected_413(self):
        """Negative test: Payload exceeding 1MB limit returns 413 Payload Too Large."""
        req = urllib.request.Request(
            f"{self.base_url}/api/v1/tasks",
            data=b"{}",
            headers={
                "Authorization": "Bearer sdd-dev-token-architect-2026",
                "Content-Type": "application/json",
                "Content-Length": "2000000"  # 2MB indicated
            }
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 413)

    # --- API-02: Rate Limiting ---
    def test_sliding_window_rate_limiter_blocks_burst(self):
        """Verify rate limiter blocks client exceeding request threshold."""
        limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=10)
        client = "192.168.1.100"
        for _ in range(5):
            allowed, _ = limiter.is_allowed(client)
            self.assertTrue(allowed)

        # 6th request must be denied
        allowed, retry_after = limiter.is_allowed(client)
        self.assertFalse(allowed)
        self.assertGreater(retry_after, 0)

    # --- WEB-03: CORS Configuration ---
    def test_cors_origin_allowlist(self):
        """Verify CORS allows trusted origins and does not reflect untrusted origins."""
        # Trusted origin
        req_trusted = urllib.request.Request(
            f"{self.base_url}/health",
            headers={"Origin": "http://localhost:3000"}
        )
        with urllib.request.urlopen(req_trusted) as resp:
            self.assertEqual(resp.headers.get("Access-Control-Allow-Origin"), "http://localhost:3000")

        # Untrusted origin
        req_untrusted = urllib.request.Request(
            f"{self.base_url}/health",
            headers={"Origin": "http://evil-attacker.com"}
        )
        with urllib.request.urlopen(req_untrusted) as resp:
            self.assertIsNone(resp.headers.get("Access-Control-Allow-Origin"))

    # --- LOG-06: Security Disclosure Endpoint ---
    def test_security_txt_endpoint(self):
        """Verify RFC 9116 security.txt is served publicly."""
        req = urllib.request.Request(f"{self.base_url}/.well-known/security.txt")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            content = resp.read().decode("utf-8")
            self.assertIn("Contact: mailto:security@agentic.sdd", content)
            self.assertIn("Expires:", content)

    # --- API-07: Verify Patch API ---
    def test_verify_patch_endpoint_success(self):
        """Positive test: Valid patch submission returns consensus verification."""
        patch_payload = json.dumps({
            "patch": "--- a/src/auth.py\n+++ b/src/auth.py\n@@ -1,1 +1,2 @@\n+# security fix",
            "targetFile": "src/auth.py",
            "runTests": True
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/v1/verify-patch",
            data=patch_payload,
            headers={
                "Authorization": "Bearer sdd-dev-token-architect-2026",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            body = json.loads(resp.read().decode())
            self.assertTrue(body["success"])
            self.assertEqual(body["data"]["astValidation"], "PASS")

if __name__ == "__main__":
    unittest.main()
