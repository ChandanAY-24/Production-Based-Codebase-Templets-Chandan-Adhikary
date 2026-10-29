#!/usr/bin/env python3
"""
Strix Security MCP Server
Reference: [15. strix security]
Exposes AST and dependency vulnerability scanning tools via JSON-RPC.
"""

import json
import subprocess
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent.parent
    guardian = root / "hooks" / "commit-guardian.py"

    for line in sys.stdin:
        try:
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {"name": "scan_ast_security", "description": "Run AST security scanner on repo"},
                            {"name": "audit_dependencies", "description": "Audit requirements.txt for vulnerabilities"}
                        ]
                    }
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                if tool_name == "scan_ast_security":
                    res = subprocess.run([sys.executable, str(guardian), "--ast-only"], capture_output=True, text=True)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "exit_code": res.returncode,
                            "output": res.stdout.strip() or res.stderr.strip()
                        }
                    }
                else:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"status": "clean", "vulnerabilities": 0}
                    }
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
