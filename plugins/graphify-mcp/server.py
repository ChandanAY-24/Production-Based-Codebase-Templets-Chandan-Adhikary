#!/usr/bin/env python3
"""
Graphify MCP Server
Reference: [8. graphify]
Provides AST symbol graph navigation tools over JSON-RPC / MCP stdio.
"""

import ast
import json
import sys
from pathlib import Path

def extract_symbols(root_dir: Path) -> dict:
    symbols = {}
    for py_file in root_dir.rglob("*.py"):
        if ".venv" in py_file.parts:
            continue
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    rel_path = str(py_file.relative_to(root_dir))
                    symbols[node.name] = {
                        "type": "class" if isinstance(node, ast.ClassDef) else "function",
                        "file": rel_path,
                        "line": node.lineno
                    }
        except Exception:
            continue
    return symbols

def main():
    root = Path(__file__).resolve().parent.parent.parent
    if len(sys.argv) > 1 and sys.argv[1] == "--dump":
        print(json.dumps(extract_symbols(root), indent=2))
        return

    # Basic JSON-RPC handler loop (stdio)
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
                            {"name": "find_symbol", "description": "Locate symbol by name"},
                            {"name": "dump_graph", "description": "Export symbol index"}
                        ]
                    }
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                symbols = extract_symbols(root)
                if tool_name == "dump_graph":
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": symbols}
                elif tool_name == "find_symbol":
                    symbol_name = params.get("arguments", {}).get("name")
                    found = symbols.get(symbol_name, "Symbol not found")
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": found}
                else:
                    resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
