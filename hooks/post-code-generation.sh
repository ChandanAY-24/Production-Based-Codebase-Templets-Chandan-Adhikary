#!/usr/bin/env bash
# ==============================================================================
# Hook: post-code-generation.sh
# Reference: [7. ponytail / 3. karpathy]
# Purpose: Validate surgical diff bounds, check format compliance, prevent file blowouts
# ==============================================================================

set -euo pipefail

echo "[HOOK:post-code-generation] Inspecting generated patch compliance..."

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WORKSPACE_ROOT"

# Check git diff bounds if in a git repo
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    CHANGED_LINES=$(git diff --stat | tail -n 1 | awk '{print $4}' || echo "0")
    if [ "$CHANGED_LINES" -gt 250 ]; then
        echo "[WARN] Patch alters more than 250 lines ($CHANGED_LINES lines changed)."
        echo "[ACTION] Recommend invoking skills/multi-model-review.md before committing."
    fi
else
    echo "[INFO] Git tree not initialized yet. Skipping diff stat check."
fi

echo "[HOOK:post-code-generation] Surgical diff validation complete."
exit 0
