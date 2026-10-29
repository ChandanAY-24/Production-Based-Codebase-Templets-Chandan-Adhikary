#!/usr/bin/env python3
"""
Commit Guardian: Pre-commit Safety Gate & AST Security Scanner
Reference: [15. strix security / 3. karpathy-skills]
Purpose: Block unverified commits, API leaks, AST vulnerabilities, or untested logic.
"""

import ast
import os
import re
import sys
from pathlib import Path

# High-risk patterns for API keys and tokens
SECRET_PATTERNS = [
    (re.compile(r"AIza[0-9A-Za-z-_]{35}"), "Google API Key"),
    (re.compile(r"sk-[a-zA-Z0-9]{32,}"), "OpenAI / Anthropic Secret Key"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "GitHub Personal Access Token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key ID"),
    (re.compile(r"(?i)(password|secret|api_key|token)\s*=\s*['\"][a-zA-Z0-9@#$%^&+=_-]{8,}['\"]"), "Hardcoded Secret Assignment")
]

class ASTSecurityVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.violations = []

    def visit_Call(self, node: ast.Call):
        # Detect eval() and exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec"):
                self.violations.append(
                    f"[BLOCK] Unsafe dynamic execution '{node.func.id}()' at {self.filename}:{node.lineno}"
                )
        # Detect os.system()
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and node.func.attr == "system":
                self.violations.append(
                    f"[WARN] Direct 'os.system()' call at {self.filename}:{node.lineno}. Use subprocess.run(..., shell=False)"
                )
        self.generic_visit(node)


def scan_file_for_secrets(filepath: Path) -> list[str]:
    violations = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [f"[WARN] Could not read {filepath}: {e}"]

    # Skip example/env templates
    if filepath.name.endswith(".example") or "tests" in filepath.parts:
        return []

    for pattern, desc in SECRET_PATTERNS:
        for idx, line in enumerate(content.splitlines(), start=1):
            if pattern.search(line):
                violations.append(f"[BLOCK] Potential {desc} detected at {filepath}:{idx}")
    return violations


def scan_python_ast(filepath: Path) -> list[str]:
    violations = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(content, filename=str(filepath))
        visitor = ASTSecurityVisitor(str(filepath))
        visitor.visit(tree)
        violations.extend(visitor.violations)
    except SyntaxError as e:
        violations.append(f"[BLOCK] Syntax error in {filepath}:{e.lineno} -> {e.msg}")
    except Exception as e:
        violations.append(f"[WARN] Failed to parse AST for {filepath}: {e}")
    return violations


def main():
    root = Path(__file__).resolve().parent.parent
    ast_only = "--ast-only" in sys.argv

    print("[COMMIT-GUARDIAN] Running security and AST audit...")
    all_violations = []

    target_dirs = [root / "src", root / "backend", root / "connectors", root / "plugins"]
    python_files = []

    for d in target_dirs:
        if d.exists():
            python_files.extend(d.rglob("*.py"))

    # Also scan hooks
    python_files.extend((root / "hooks").glob("*.py"))

    # Scan python files
    for py_file in python_files:
        if py_file.name == "commit-guardian.py":
            continue
        all_violations.extend(scan_python_ast(py_file))
        if not ast_only:
            all_violations.extend(scan_file_for_secrets(py_file))

    # Scan env/config files for secrets
    if not ast_only:
        for config_file in root.glob("*.json"):
            all_violations.extend(scan_file_for_secrets(config_file))

    # Output results
    if all_violations:
        print("\n--- VIOLATIONS FOUND ---")
        blocks = 0
        for v in all_violations:
            print(v)
            if "[BLOCK]" in v:
                blocks += 1

        if blocks > 0:
            print(f"\n[FAILED] Commit Guardian blocked execution: {blocks} blocking issue(s) detected.")
            sys.exit(1)
        else:
            print("\n[PASSED WITH WARNINGS] Only non-blocking warnings found.")
            sys.exit(0)
    else:
        print("[SUCCESS] Commit Guardian: AST and Secrets scan clean! Zero violations detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
