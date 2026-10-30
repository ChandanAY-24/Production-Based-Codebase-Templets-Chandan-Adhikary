# SDD Agentic Coding Framework Constitution

## Core Principles

### I. Simplicity & Karpathy Surgical Engineering
Every modification is minimal, contiguous, and targeted. Functions remain under 40 lines; maximum branching depth is 2. No speculative abstractions or dead code. Write plain, readable code instead of complex metaprogramming.

### II. Test-First (Super-TDD Non-Negotiable)
Every new feature, API route, or bugfix must follow the Red-Green-Refactor cycle:
1. Author deterministic test fixtures under `tests/`.
2. Execute suite to prove expected failure (RED verified).
3. Author minimal surgical implementation to turn tests passing (GREEN verified).
4. Refactor while maintaining 100% test pass rate.

### III. Zero-Trust Security & AST Scanning
All external inputs validated using bounded Pydantic schemas. Row-level tenant/store isolation is strictly enforced. Pre-commit hooks (`hooks/commit-guardian.py`) and AST scanners reject unverified code, dynamic execution (`eval`/`exec`), shell invocations, and credential leaks.

### IV. Five Quality Gates Enforcement
No commit or merge occurs without passing all 5 quality gates:
1. Task Traceability (`docs/TASKS.md`, `specs/`)
2. Build & Syntax Verification
3. Security Validation (Gate 3 checklist)
4. 100% Test Suite Pass
5. Code Review & Consensus (`docs/CODE-REVIEW.md`)

### V. Contract Completeness & Spec Lock
Domain entities, API schemas, and database invariants must be formally documented in `docs/SPEC.md`, `docs/APIS.md`, and `docs/DATABASE.md` before or concurrent with implementation.

## Governance
This Constitution supersedes informal practices. Any proposed amendment requires documentation in `docs/CONSTITUTION.md` and explicit lead approval. All pull requests must verify compliance against `docs/CODE-REVIEW.md`.

**Version**: 1.0.0 | **Ratified**: 2026-10-31 | **Last Amended**: 2026-10-31
