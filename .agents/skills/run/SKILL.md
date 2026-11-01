---
name: run
description: "Starts the application locally, runs smoke health checks, verifies security headers and API endpoints before proper deployment. Guides local dev servers and clean shutdown."
---

# `/run` — Local Project Execution & Pre-Deployment Smoke Runner

> **Targets:** `backend/main.py` (Port 8000), `frontend/index.html`  
> **Script:** `.agents/scripts/smoke-runner.py`  
> **Standards:** `specs/001-Spec-Security-guide.md`, `docs/APIS.md`

Use this slash command to run the project locally, probe health endpoints, verify security headers, and smoke test the system before deploying to staging or production.

---

## Step 1: Automated Smoke Check (Recommended)
Execute the non-interactive automated smoke runner to verify that the backend starts, responds with 200 OK on health checks, and returns mandatory RFC 9116 and security headers:

```powershell
.venv\Scripts\python.exe .agents/scripts/smoke-runner.py
```

Expected output:
```text
[SMOKE] Launching backend server: backend/main.py
  [PASS] GET /api/v1/health -> 200 OK (Status: healthy)
  [PASS] Security Headers -> X-Content-Type-Options: nosniff verified
  [PASS] GET /.well-known/security.txt -> 200 OK (RFC 9116 compliant)
[SMOKE] Verdict: 3/3 checks passed.
```

---

## Step 2: Interactive Local Backend Execution
To run the backend server continuously on your local machine for manual development or API testing:

```powershell
# Set PYTHONPATH and launch server
$env:PYTHONPATH = "."
.venv\Scripts\python.exe backend/main.py
```

The server listens on `http://127.0.0.1:8000`.

### Health & Contract Probes (In another terminal)
```powershell
# 1. Health check
curl http://127.0.0.1:8000/api/v1/health

# 2. Security disclosure (RFC 9116)
curl http://127.0.0.1:8000/.well-known/security.txt

# 3. Authenticated task list query
curl -H "Authorization: Bearer sdd-dev-token-architect-2026" http://127.0.0.1:8000/api/v1/tasks
```

---

## Step 3: Frontend Cockpit Execution
To view the frontend cockpit (`frontend/index.html`):
1. Serve the frontend with any local HTTP server (or Vite if installed):
   ```powershell
   cd frontend
   python -m http.server 3000
   ```
2. Open `http://localhost:3000` in your browser.
3. The frontend is configured with strict Content Security Policy (`default-src 'self'`) and connects to `http://localhost:8000/api/v1/*`.

---

## Step 4: Graceful Shutdown
To stop running servers:
- Press `Ctrl + C` in the running server terminal.
- Or terminate by port in PowerShell:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
  ```

