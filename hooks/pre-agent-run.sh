#!/usr/bin/env bash
# ==============================================================================
# Hook: pre-agent-run.sh
# Reference: [6. claude-mem / 8. graphify]
# Purpose: Sync memory vector DB, refresh code symbol graph & export context
# ==============================================================================

set -euo pipefail

echo "[HOOK:pre-agent-run] Initializing session context..."

# 1. Verify environment
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WORKSPACE_ROOT"

# 2. Sync vector memory store if available
if [ -f "connectors/vector-memory/store.py" ]; then
    echo "[HOOK:pre-agent-run] Syncing local vector memory database..."
    python connectors/vector-memory/store.py --sync || echo "[WARN] Vector store sync returned warning, continuing."
else
    echo "[WARN] connectors/vector-memory/store.py not found. Using static docs/MEMORY.md"
fi

# 3. Check for docs/SPEC.md invariants
if [ ! -f "docs/SPEC.md" ]; then
    echo "[ERROR] docs/SPEC.md missing! Agents require domain invariants to proceed." >&2
    exit 1
fi

echo "[HOOK:pre-agent-run] Pre-run checks passed. Agent environment ready."
exit 0
