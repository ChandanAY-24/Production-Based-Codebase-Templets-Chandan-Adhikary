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
│   ├── CODE-REVIEW.md               # Five quality gates, surgical review checklists & consensus protocols
│   ├── TESTING.md                   # Super-TDD (Red-Green-Refactor), negative security testing & pytest suite
│   ├── TASKS.md                     # Active task tracking board, priorities (P0-P3) & lifecycle states
│   ├── SECURITY.md                  # Comprehensive security guide, AST scanning rules & Gate 3 controls
│   ├── AUTH.md                      # Token lifecycle (JWT/scrypt), RBAC matrix, IDOR isolation & MFA/TOTP
│   ├── GITHUB-WORKFLOW.md           # 7-phase git workflow, conventional commits & human-in-the-loop gates
│   ├── PERFORMANCE-SCALABILITY.md   # Concurrency tiers (100-10k users), Core Web Vitals & query optimization
│   ├── AUTHENTICATION-SECURITY.md   # [15. strix] Threat models, zero-trust constraints, AST security rules
│   ├── ERROR-HANDLING-TRACKER.md    # Known edge cases, bug reproduction traces
│   ├── CONSTITUTION.md              # [4. i-have-adhd / 3. karpathy] Core agent guardrails (concise, direct)
│   ├── SKILLS.md                    # Index of markdown-based procedural task workflows
│   ├── HOOKS.md                     # Documentation of lifecycle interception scripts
│   └── reference-artifacts/         # Supplementary architecture specs, wireframes, checklists
│
├── specs/                           # Specifications and Standards
│   ├── 001-Spec-Security-guide.md   # Production-Grade Security Checks Specification (102 checks)
│   ├── 002-Spec-Git-Workflow-Rules.md # GitHub Workflow & 5 Quality Gates Specification
│   └── 003-Spec-Scalibility-optimization.md # Website Audit, Performance Optimization & Scalability Standard
│
├── security/                        # Project Security Profiles, Reports & Threat Models
│   ├── PROJECT_PROFILE.md           # Detected project security flags, stack, attack surface
│   ├── SECURITY_REPORT.md           # Full audit report and release gate verdict
│   ├── THREAT_MODEL.md              # STRIDE analysis and trust boundary mapping
│   └── RUNBOOK.md                   # Incident response, containment, and rotation procedures
│
├── auth/                            # Authentication & Authorization Subsystem (AUTH-01 to AUTH-06)
│   ├── README.md                    # Subsystem overview, quickstart & integration contracts
│   ├── SPEC.md                      # Formal domain specifications, contracts & invariants
│   ├── THREAT_MODEL.md              # STRIDE threat model for credentials, tokens, and sessions
│   ├── RUNBOOK.md                   # Emergency revocation, key rotation & lockout recovery SOPs
│   ├── models.py                    # Domain models (AuthUser, UserRecord, TokenPair, Session)
│   ├── passwords.py                 # Memory-hard KDF (scrypt / PBKDF2), timing-safe verify
│   ├── tokens.py                    # HMAC-SHA256 signed JWTs & single-use rotating refresh tokens
│   ├── session.py                   # Server-side session store with idle/absolute TTL
│   ├── mfa.py                       # RFC 6238 TOTP 2FA engine & single-use backup recovery codes
│   └── service.py                   # Central AuthService orchestrating credentials and RBAC
│
├── payment/                         # Payment Integration Gateway (Placeholder)
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

### 3. Production Security Spec Verification
```bash
# Run full unit and security suite
python -m unittest discover -s tests -p "test_*.py" -v
# Run dependency vulnerability audit
python -m pip_audit -r requirements.txt
# Follow specs/001-Spec-Security-guide.md for every security review and new feature
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
