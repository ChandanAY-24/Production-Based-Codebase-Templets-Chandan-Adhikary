#!/usr/bin/env python3
"""
token-guard.py - Production Context Window & Token Optimization Guardian
Enforces surgical file reading, truncated command logs, and diff bounds.
"""

import sys
import os
import argparse

MAX_READ_LINES = 350
MAX_OUTPUT_LINES = 40
MAX_DIFF_LINES = 150

def check_file_read(filepath: str, start_line: int = 1, end_line: int = 0) -> int:
    """Blocks unbounded reads of large files into agent context."""
    if not os.path.isfile(filepath):
        return 0

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        total_lines = len(lines)
    except Exception as e:
        print(f"[TOKEN-GUARD WARN] Unable to read {filepath}: {e}", file=sys.stderr)
        return 0

    if end_line <= 0:
        if total_lines > MAX_READ_LINES:
            print(
                f"[TOKEN-GUARD BLOCKED] '{filepath}' has {total_lines} lines.\n"
                f"Full-file read exceeds the {MAX_READ_LINES}-line token budget.\n"
                f"Remedy: Use StartLine and EndLine to read targeted slices (e.g., +/- 15 lines).",
                file=sys.stderr,
            )
            return 1
    else:
        slice_size = end_line - start_line + 1
        if slice_size > MAX_READ_LINES:
            print(
                f"[TOKEN-GUARD BLOCKED] Requested slice of {slice_size} lines exceeds maximum allowed {MAX_READ_LINES} lines.\n"
                f"Remedy: Narrow down your query to the specific function or class block.",
                file=sys.stderr,
            )
            return 1

    return 0

def sanitize_output(content: str, max_lines: int = MAX_OUTPUT_LINES) -> str:
    """Truncates excessive terminal stdout/stderr to protect context window."""
    lines = content.splitlines()
    if len(lines) <= max_lines:
        return content

    head_count = max_lines // 2
    tail_count = max_lines - head_count
    omitted = len(lines) - max_lines

    truncated = (
        lines[:head_count]
        + [f"\n... [TOKEN-GUARD: Truncated {omitted} lines of verbose log output to conserve context] ...\n"]
        + lines[-tail_count:]
    )
    return "\n".join(truncated)

def main():
    parser = argparse.ArgumentParser(description="Context window & token optimization utility.")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: check-read
    read_parser = subparsers.add_parser("check-read", help="Verify file read bounds")
    read_parser.add_argument("--file", required=True, help="Target file path")
    read_parser.add_argument("--start", type=int, default=1, help="Start line")
    read_parser.add_argument("--end", type=int, default=0, help="End line")

    # Subcommand: sanitize
    sanitize_parser = subparsers.add_parser("sanitize", help="Sanitize standard output string from stdin or file")
    sanitize_parser.add_argument("--max-lines", type=int, default=MAX_OUTPUT_LINES)

    args = parser.parse_args()

    if args.command == "check-read":
        sys.exit(check_file_read(args.file, args.start, args.end))
    elif args.command == "sanitize":
        raw = sys.stdin.read()
        sanitized = sanitize_output(raw, args.max_lines)
        sys.stdout.write(sanitized)
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()

