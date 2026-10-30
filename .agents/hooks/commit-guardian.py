#!/usr/bin/env python3
import json
import sys

def main():
    # PreToolUse hook requires JSON output with decision
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
