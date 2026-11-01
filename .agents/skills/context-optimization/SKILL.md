---
name: context-optimization
description: "Surgically optimizes context window token usage, compacts conversation history, sanitizes CLI output, isolates research via subagents, and prevents reasoning degradation while maintaining 100% output fidelity."
---

# `/context-optimization` — Context Window & Token Optimization Skill

> **Scope:** High-efficiency context budget management for AI agents (Antigravity, Claude Code, Codex, Cursor).  
> **Rule Reference:** `.agents/rules/token-optimization.md`  
> **Guardian Tool:** `.agents/hooks/token-guard.py`

Use this skill whenever:
1. Conversation history is growing long ($> 20$ turns or $> 60\%$ context window capacity).
2. Investigating large codebases or large files without blowing up the context budget.
3. Running test suites or commands that produce verbose output.
4. Performing heavy exploratory research before writing code.

---

## 1. Surgical Ingestion Protocols

### A. The Bounded Read Protocol
Never ingest whole files $> 300$ lines. Execute targeted discovery:
1. **Find Target Lines:**
   ```powershell
   # Search for definition or class
   git grep -n "class OrderProcessor"
   # or
   python -c "import ast; tree = ast.parse(open('src/core.py').read()); ..."
   ```
2. **Read Target Slice:**
   Use line boundaries with $\pm 15$ lines of padding:
   `read_file(Path="src/core.py", StartLine=140, EndLine=185)`

### B. The Outline First Protocol
Before reading any file you haven't seen:
- Run a structural outline script or regex to get function/class names and line numbers.
- Ingest only the specific function needed to solve the task.

---

## 2. Terminal Output Sanitization Protocol

Raw terminal output frequently causes context explosion. Always cap output:
```powershell
# For pytest: concise output + tb short
python -m pytest tests/test_core.py -q --tb=short

# If expecting large output, pipe into token-guard sanitizer
python tests/heavy_suite.py | python .agents/hooks/token-guard.py sanitize --max-lines 30
```

---

## 3. Subagent Offloading Protocol

When deep codebase analysis, multi-file searches, or external documentation lookups are required:
1. **Do NOT** read multiple files in the primary agent session.
2. **Invoke a subagent** (e.g. `research` or `self` with prompt):
   > "Inspect `src/auth/` and `src/models/`, identify how session tokens are validated, and report back ONLY: 1) the function signature, 2) the file path and line numbers, and 3) any edge-case exceptions thrown. Maximum 20 lines summary."
3. The subagent processes the thousands of tokens in its isolated sandbox and returns only the distilled 200-token result.

---

## 4. Context Compaction & Memory Grounding Protocol

When the turn count crosses 20 turns or context approaches $60\% - 70\%$ saturation:
1. **Flush Active Status to Disk:**
   - Update `docs/TASKS.md` with completed items and current in-progress task.
   - Update `docs/MEMORY.md` with new architectural facts or invariant decisions.
2. **Trigger Compaction:**
   - Recommend or execute `/compact` to summarize previous conversational turns.
   - Because all ground truths are saved in `docs/TASKS.md` and `docs/MEMORY.md`, no knowledge or requirements are lost.

---

## 5. Verification Checklist

Before issuing output:
- [ ] No file read $> 300$ lines was ingested without line boundaries.
- [ ] Code modifications were generated as surgical drop-in replacements (`edit_file`) rather than full-file rewrites.
- [ ] Command outputs were filtered or truncated to the essential error lines.
- [ ] Output preserves 100% adherence to all project specs, types, and quality gates.

