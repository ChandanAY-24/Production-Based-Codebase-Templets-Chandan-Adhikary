# Spec-Driven Development (SDD) & Agentic Coding Framework

> A battle-tested codebase architecture designed for autonomous AI agents, multi-agent swarms, and pair programming under deterministic contracts, surgical diff checking, and multi-model consensus verification.

---

## 🏛️ Codebase Directory Structure

```
.
├── docs/                            # Core specifications, contracts & guardrails
│   ├── SPEC.md                      # [14. spec-kit] Core domain logic, schema contracts & invariants
│   ├── PRD.md                       # Product requirements, user journeys, success metrics
│   ├── PLAN.md                      # [2. superpowers / 20. rea] Recursive reasoning & execution roadmaps
│   ├── PROMPTS.md                   # Reusable prompt snippets (e.g., /grill-me, /distill, /octo:review)
│   ├── TECH-STACKS.md               # Pinned runtimes, model configurations, router topology
│   ├── RULES.md                     # [3. karpathy-skills] Simplicity first, surgical changes, no fluff
│   ├── ARCHITECTURE.md              # [8. graphify] Codebase knowledge graph & symbol relationships
│   ├── DESIGN.md                    # [12. impeccable / 13. ui-ux-pro-max / 14. taste-skill / 16. emilkowalski]
│   ├── MEMORY.md                    # [6. claude-mem] Persistent cross-session facts, state tracking
│   ├── APIS.md                      # OpenAPI contracts, serializers, endpoints
│   ├── AGENTS.md                    # [10. gstack / 12. ECC] Roster: PM, Architect, QA, Consensus Reviewer
│   ├── PHASES.md                    # Milestone exit criteria & TDD deliverables
│   ├── DATABASE.md                  # ER schemas, indexes, migration rollback policies
│   ├── AUTHENTICATION-SECURITY.md   # [15. strix] Threat models, zero-trust constraints, AST security rules
│   ├── ERROR-HANDLING-TRACKER.md    # Known edge cases, bug reproduction traces
│   ├── CONSTITUTION.md              # [4. i-have-adhd / 3. karpathy] Core agent guardrails (concise, direct)
│   ├── SKILLS.md                    # Index of markdown-based procedural task workflows
│   ├── HOOKS.md                     # Documentation of lifecycle interception scripts
│   └── reference-artifacts/         # Supplementary architecture specs, wireframes, checklists
│
├── skills/                          # Declarative markdown instructions (usable by any agent)
│   ├── grill-me.md                  # [1. grill-me] Pre-implementation edge-case extraction interview
│   ├── super-tdd.md                 # [2. superpowers] Red-Green-Refactor test cycle enforcement
│   ├── multi-model-review.md        # [5. claude-octopus] Consensus verification prompt across external models
│   ├── diff-patcher.md              # [7. ponytail] Exact unified diff formatting & validation protocol
│   ├── ui-polish.md                 # [12. impeccable / 16. emilkowalski] Micro-interactions, spacing, typography
│   ├── db-migrate.md                # Migration generation, application, and rollback workflow
│   ├── api-test-runner.md           # [11. playwright] Headless E2E / integration testing execution
│   └── ast-security-scan.md         # [15. strix] Pre-commit security analysis and OWASP validation
│
├── hooks/                           # Lifecycle triggers & safety gates
│   ├── pre-agent-run.sh             # [6. claude-mem / 8. graphify] Sync memory vector DB & refresh code graph
│   ├── post-code-generation.sh      # [7. ponytail / 3. karpathy] Validate surgical diffs & format compliance
│   ├── commit-guardian.py           # [15. strix] Block unverified commits, API leaks, or untested logic
│   └── routing-proxy.sh             # [21. OmniRoute] Point local calls to cheapest/strongest inference model
│
├── plugins/                         # MCP (Model Context Protocol) tool servers & extensions
│   ├── graphify-mcp/                # Symbol graph navigation server
│   ├── playwright-mcp/              # Headless browser capture & DOM automation tools
│   ├── strix-security-mcp/          # AST scanner & dependency vulnerability checker
│   └── omniroute-proxy/             # Unified API proxy for heterogeneous model inference
│
├── connectors/                      # External bridge adapters
│   ├── openclaw-daemon/             # [20. openclaw] Sandboxed background task runner / worker daemon
│   └── vector-memory/               # SQLite / local vector store backing claude-mem
│
├── backend/                         # Server application source code
├── frontend/                        # Client application source code
├── database/                        # Migrations, seeds, snapshots
├── src/                             # Core shared logic / microservices
├── tests/                           # Super-TDD automated test suites
├── .env.example                     # Environment variables template
├── requirements.txt / package.json  # Locked dependencies
├── settings.json                    # Workspace editor & MCP client settings
└── .claude.json / AGENTS.json       # Cross-agent adapter configuration (Claude Code, OpenCode, Codex)
```

---

## 🚀 Quickstart & Operational Commands

### 1. Test Suite (Super-TDD)
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### 2. Security Guardian & AST Audit
```bash
python hooks/commit-guardian.py
```

### 3. Sync Vector Memory
```bash
python connectors/vector-memory/store.py --sync
```

### 4. Run Backend API Server
```bash
python backend/main.py
```

### 5. Check OpenClaw Worker Daemon
```bash
python connectors/openclaw-daemon/daemon.py --once
```
