#!/usr/bin/env python3
"""
Backend API Server
Reference: docs/APIS.md & docs/SPEC.md
Provides HTTP REST endpoints conforming to the global JSON envelope.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from src.services import TaskService
from src.models import TaskStatus

task_service = TaskService()

# Preload initial demo task
task_service.create_task(
    title="Scaffold SDD Agentic Architecture",
    spec_ref="docs/SPEC.md#L45",
    invariants=["Zero unbounded mutations", "Deterministic rollback", "Surgical diff bounds"]
)

class APIRequestHandler(BaseHTTPRequestHandler):
    def _send_response_json(self, status_code: int, data=None, error=None):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        payload = {
            "success": error is None,
            "data": data,
            "error": error,
            "meta": {
                "timestamp": "2026-10-30T00:00:00Z"
            }
        }
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/v1/tasks":
            tasks = [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status.value,
                    "specReference": t.spec_reference,
                    "invariants": t.invariants,
                    "assignedAgent": t.assigned_agent,
                    "createdAt": t.created_at,
                    "updatedAt": t.updated_at
                }
                for t in task_service.list_tasks()
            ]
            self._send_response_json(200, data=tasks)
        elif parsed.path == "/health":
            self._send_response_json(200, data={"status": "healthy"})
        else:
            self._send_response_json(404, error="Endpoint not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body) if body else {}
        except Exception:
            self._send_response_json(400, error="Invalid JSON payload")
            return

        if parsed.path == "/api/v1/tasks":
            title = payload.get("title")
            spec_ref = payload.get("specReference", "docs/SPEC.md")
            invariants = payload.get("invariants", ["Standard invariant"])

            try:
                task = task_service.create_task(title=title, spec_ref=spec_ref, invariants=invariants)
                self._send_response_json(201, data={"id": task.id, "title": task.title, "status": task.status.value})
            except ValueError as e:
                self._send_response_json(422, error=str(e))
        else:
            self._send_response_json(404, error="Endpoint not found")

def run_server(port: int = 8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, APIRequestHandler)
    print(f"[BACKEND] API Server listening on port {port} (docs/APIS.md)...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[BACKEND] Stopping API Server.")

if __name__ == "__main__":
    run_server()
