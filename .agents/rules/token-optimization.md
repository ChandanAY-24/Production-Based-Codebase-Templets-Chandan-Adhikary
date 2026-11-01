# Production Context Window & Token Optimization Rules

> **Scope:** Always-On Workspace Invariant for all Autonomous Agents, Claude Code, Codex, Antigravity, and Cursor.  
> **Mandate:** Maximize token efficiency and prompt cache hit rate WITHOUT compromising output fidelity, correctness, or quality gates.

---

## 1. The Core Invariants

Every agent executing in this workspace **MUST** adhere to the following 7 operational invariants:

### Rule 1: Surgical Read Invariant (Line-Bounded Slices)
- **Forbidden:** Never call `read_file`, `cat`, or file ingest tools on entire files exceeding 300 lines without explicit reason.
- **Enforced:**
  1. Locate target classes, functions, or keys using symbol search, `grep`, or AST tools.
  2. Ingest strictly the target line slice with bounded context ($\pm 15$ lines of surrounding code):
     `read_file(Path, StartLine=X, EndLine=Y)`.
  3. Reading more than 300 contiguous lines requires an outline check first.

### Rule 2: Surgical Diffs Over Full-File Rewrites
- **Forbidden:** Never rewrite an entire 300+ line file to apply a 10-line modification.
- **Enforced:**
  1. Always use targeted drop-in replacements (`edit_file`) or unified standard diff formats.
  2. Replacements must be bounded strictly to the modified AST node or function.
  3. Preserves prompt budget ($85\%+$ reduction in generated tokens) and prevents collateral syntax regressions in untouched code.

### Rule 3: CLI & Test Output Sanitization (Max 40 Lines)
- **Forbidden:** Never stream raw 500-line test outputs, npm install trees, or deep exception cascades into the model context.
- **Enforced:**
  1. Pipe CLI execution through filters or test summaries:
     `pytest -q --tb=short | tail -n 30`
  2. Retain only: total counts, failing test name, failing assertion, and exact file/line error.
  3. Suppress passing test traces, package download progress bars, and redundant stack frames.

### Rule 4: Subagent Context Isolation (Offload Exploratory Spikes)
- **Forbidden:** Never run open-ended codebase exploration, multi-file searches, or external documentation parsing in the primary planning context.
- **Enforced:**
  1. Launch a dedicated lightweight subagent (e.g. `research` or disposable worker).
  2. The subagent inspects files, runs regex scans, and distills documentation in an isolated context.
  3. Subagent returns **strictly** a 10–20 line synthesis and exact file/line anchors to the primary agent.

### Rule 5: KV Cache Hit-Rate Maximization (Static-Prefix Alignment)
- **Understanding:** LLM providers reuse KV cache for identical prompt prefixes. Any change to initial tokens breaks caching across the entire conversation.
- **Enforced:**
  1. Keep static guidelines, core persona, and invariant rules at the very top of context.
  2. Do not inject variable values (timestamps, dynamic process IDs, random tokens) into system prompt prefixes.
  3. Dynamic state, active file content, and user queries must strictly remain at the tail.

### Rule 6: Lazy-Loaded Tool Schemas & Tool Registry Pruning
- **Forbidden:** Do not load dozens of eager MCP tool definitions into the system prompt when unneeded.
- **Enforced:**
  1. Use lazy-loaded schemas (`call_mcp_tool`) loaded on demand.
  2. Deactivate dormant plugins and unused CLI definitions.

### Rule 7: Externalized Single-Source-of-Truth Memory
- **Forbidden:** Never rely on chat transcript history to retain project requirements, task status, or architectural decisions.
- **Enforced:**
  1. All state must be pinned to workspace markdown files:
     - Active progress and subtasks: `docs/TASKS.md`
     - Cross-session facts and decisions: `docs/MEMORY.md`
     - Domain contracts and schemas: `docs/SPEC.md`
  2. When transcript approaches saturation ($> 65\%$ context window), compress state into markdown files and invoke `/compact`.

---

## 2. Token Budget Thresholds

| Operation | Max Token Budget | Remediation if Exceeded |
|---|---|---|
| Single File Ingestion | $\le 1,500$ tokens ($\approx 300$ lines) | Use `StartLine`/`EndLine` or AST signature extraction. |
| Code Modification Patch | $\le 800$ output tokens | Use surgical `edit_file` with targeted replacement. |
| Command Stdout Ingestion | $\le 600$ tokens ($\approx 40$ lines) | Pipe through `grep`, `head`, `tail`, or error extractor. |
| Research / Multi-file Search | $\le 1,000$ distilled tokens | Delegate to isolated subagent; ingest summary only. |

---

## 3. Zero-Compromise Quality Matrix

Optimizing tokens must NEVER degrade code quality. Zero-compromise is maintained through mechanical verification:

```
[Targeted Line Read] ──> [Surgical Edit] ──> [Deterministic Test Run] ──> [AST & Security Check]
        │                       │                       │                          │
  Low Token Cost          Low Output Cost         Clean Short Log           Full Output Fidelity
```

