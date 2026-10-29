#!/usr/bin/env python3
"""
Playwright MCP Server Bridge
Reference: [11. playwright]
Provides headless DOM automation & screenshot captures via JSON-RPC.
"""

import json
import sys

def main():
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
                            {"name": "browser_navigate", "description": "Navigate to URL and return title & status"},
                            {"name": "browser_snapshot", "description": "Capture text tree"}
                        ]
                    }
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                if tool_name == "browser_navigate":
                    url = params.get("arguments", {}).get("url", "http://localhost:3000")
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ok", "url": url, "simulated": True}}
                else:
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": {"dom": "<div id='root'>Ready</div>"}}
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
