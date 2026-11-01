#!/usr/bin/env python3
"""
Local Smoke Runner & Pre-Deployment Verification Script
Spawns backend/main.py, probes health endpoints and security headers,
and verifies runtime health before production deployment.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
import subprocess
from typing import Dict, Any

HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"

def check_port_free(host: str, port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) != 0

def probe_http(url: str, method: str = "GET", headers: Dict[str, str] = None, data: bytes = None) -> tuple[int, Dict[str, str], bytes]:
    req = urllib.request.Request(url, data=data, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, resp_headers, resp.read()
    except urllib.error.HTTPError as e:
        resp_headers = {k.lower(): v for k, v in e.headers.items()}
        return e.code, resp_headers, e.read()

def run_smoke_suite() -> bool:
    print(f"[SMOKE] Starting local pre-deployment smoke checks on {BASE_URL}...")
    
    python_exe = sys.executable
    server_process = None
    started_by_us = False

    # Check if server is already running
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if check_port_free(HOST, PORT):
        print(f"[SMOKE] Launching backend server: {python_exe} backend/main.py")
        env = os.environ.copy()
        env["PORT"] = str(PORT)
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{project_root};{existing_pythonpath}" if existing_pythonpath else project_root
        server_process = subprocess.Popen(
            [python_exe, os.path.join(project_root, "backend", "main.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            cwd=project_root
        )
        started_by_us = True
        
        # Wait for server to bind
        ready = False
        for attempt in range(15):
            time.sleep(0.4)
            if not check_port_free(HOST, PORT):
                ready = True
                break
        if not ready:
            print("[SMOKE] ERROR: Backend server failed to start within 6 seconds.")
            if server_process.poll() is not None:
                _, err = server_process.communicate()
                print(f"[SMOKE] Server STDERR: {err}")
            server_process.terminate()
            return False
    else:
        print(f"[SMOKE] Detected existing server listening on {BASE_URL}.")

    passed = 0
    total = 3

    try:
        # Check 1: Health endpoint
        status, headers, body = probe_http(f"{BASE_URL}/api/v1/health")
        if status == 200:
            payload = json.loads(body.decode("utf-8"))
            if payload.get("data", {}).get("status") == "healthy":
                print("  [PASS] GET /api/v1/health -> 200 OK (Status: healthy)")
                passed += 1
            else:
                print(f"  [FAIL] GET /api/v1/health -> Unexpected data: {payload}")
        else:
            print(f"  [FAIL] GET /api/v1/health -> HTTP {status}")

        # Check 2: Mandatory security headers
        nosniff = headers.get("x-content-type-options") == "nosniff"
        content_type = "application/json" in headers.get("content-type", "")
        if nosniff and content_type:
            print("  [PASS] Security Headers -> X-Content-Type-Options: nosniff verified")
            passed += 1
        else:
            print(f"  [FAIL] Missing security headers. Headers received: {headers}")

        # Check 3: RFC 9116 security.txt
        status, _, body = probe_http(f"{BASE_URL}/.well-known/security.txt")
        if status == 200 and b"Contact: mailto:security@agentic.sdd" in body:
            print("  [PASS] GET /.well-known/security.txt -> 200 OK (RFC 9116 compliant)")
            passed += 1
        else:
            print(f"  [FAIL] GET /.well-known/security.txt -> HTTP {status}")

    finally:
        if started_by_us and server_process:
            print("[SMOKE] Terminating temporary test server process...")
            server_process.terminate()
            server_process.wait(timeout=3)
            print("[SMOKE] Test server stopped cleanly.")

    print(f"\n[SMOKE] Verdict: {passed}/{total} checks passed.")
    return passed == total

if __name__ == "__main__":
    success = run_smoke_suite()
    sys.exit(0 if success else 1)
