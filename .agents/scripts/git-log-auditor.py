#!/usr/bin/env python3
"""
Git History Explorer & Conventional Commit Auditor
Audits git history against specs/002-Spec-Git-Workflow-Rules.md.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

CONVENTIONAL_COMMIT_REGEX = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(\([a-zA-Z0-9_\-\./]+\))?(!)?:\s.+$"
)


def run_git(args: list[str]) -> str:
    """Run a git command in workspace root and return stdout."""
    res = subprocess.run(
        ["git"] + args,
        cwd=WORKSPACE_ROOT,
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        return ""
    return res.stdout.strip()


def parse_commits(limit: int = 15, file_path: str | None = None) -> list[dict]:
    """Retrieve and parse git log commits."""
    # format: hash|author|date|subject
    git_args = ["log", f"-n{limit}", "--pretty=format:%h|%an|%cr|%s"]
    if file_path:
        git_args.extend(["--", file_path])

    raw = run_git(git_args)
    if not raw:
        return []

    commits = []
    for line in raw.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commit_hash, author, date_rel, subject = parts
            is_valid = bool(CONVENTIONAL_COMMIT_REGEX.match(subject))
            commits.append({
                "hash": commit_hash,
                "author": author,
                "date": date_rel,
                "subject": subject,
                "conventional": is_valid
            })
    return commits


def main():
    parser = argparse.ArgumentParser(description="Git History & Conventional Commit Auditor")
    parser.add_argument("--limit", type=int, default=10, help="Number of commits to audit")
    parser.add_argument("--file", type=str, default=None, help="Inspect history of specific file")
    parser.add_argument("--audit", action="store_true", help="Audit conventional commit compliance")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    commits = parse_commits(limit=args.limit, file_path=args.file)
    if not commits:
        print("[GIT-LOG] No commit history found.")
        sys.exit(0)

    if args.json:
        print(json.dumps(commits, indent=2))
        return

    print("[GIT-LOG] =========================================================")
    print(f"[GIT-LOG] Git History & Audit (Last {len(commits)} commits)")
    if args.file:
        print(f"[GIT-LOG] File: {args.file}")
    print("[GIT-LOG] ---------------------------------------------------------")

    valid_count = 0
    for c in commits:
        tag = "[PASS]" if c["conventional"] else "[WARN]"
        if c["conventional"]:
            valid_count += 1
        print(f"{tag} {c['hash']} ({c['author']}, {c['date']}): {c['subject']}")

    print("[GIT-LOG] ---------------------------------------------------------")
    compliance = (valid_count / len(commits)) * 100
    print(f"[GIT-LOG] Conventional Commit Compliance: {valid_count}/{len(commits)} ({compliance:.1f}%)")
    print("[GIT-LOG] =========================================================")


if __name__ == "__main__":
    main()

