---
name: git-log
description: "Inspects git commit history, branch topology, conventional commit compliance, and file changelogs according to specs/002-Spec-Git-Workflow-Rules.md."
---

# `/git-log` — Git History Explorer & Conventional Commit Auditor

> **Standard:** `specs/002-Spec-Git-Workflow-Rules.md`, `docs/GITHUB-WORKFLOW.md`  
> **Script:** `.agents/scripts/git-log-auditor.py`  
> **Purpose:** Transparent history inspection, commit compliance audit, branch tree visualization

Use this slash command to review recent git history, verify conventional commit standards (`feat`, `fix`, `docs`, `ci`, `test`, `refactor`, `perf`), trace file diffs, and inspect uncommitted changes.

---

## Capabilities & Usage Modes

### 1. Visual Topology Graph
Displays branch and merge topology with decorated branch pointers:
```powershell
git log --graph --oneline --decorate --all -n 20
```

### 2. Conventional Commit Compliance Audit
Audits recent commits against the required specification:
```powershell
.venv\Scripts\python.exe .agents/scripts/git-log-auditor.py --audit --limit 15
```

Valid conventional commit types:
- `feat(...)`: New user-facing or agent capability
- `fix(...)`: Bug fix or error resolution
- `docs(...)`: Documentation or spec updates
- `test(...)`: Adding or refactoring tests
- `refactor(...)`: Code changes without functional impact
- `perf(...)`: Performance and scalability optimization
- `ci(...)`: GitHub Actions or hook pipeline adjustments
- `chore(...)`: Maintenance or dependency updates

### 3. File History & Change Tracing
Trace the chronological history and unified diffs of a specific file:
```powershell
git log -p -n 5 -- <path-to-file>
```
Or with the auditor:
```powershell
.venv\Scripts\python.exe .agents/scripts/git-log-auditor.py --file <path-to-file>
```

### 4. Working Tree & Stash Inspection
Summarizes uncommitted modifications, staged items, and active branch status:
```powershell
git status --short --branch
```

---

## Output Format
```text
[GIT-LOG] Commit History Audit (Last 10 commits)
--------------------------------------------------------------------------------
[PASS] 391fd5f feat(perf): add token optimization, performance rules, and agent skills suite
[PASS] 36602db ci: surface test failure annotations
[PASS] abc54b2 fix(ci): align test runner with package.json and standard library unittest discover
[PASS] 33288bf fix(ci): ensure pytest is installed and invoked via python module
[PASS] 67fcd74 fix(ci): configure PYTHONPATH, tests package marker, and pytest in security workflow
--------------------------------------------------------------------------------
[AUDIT] 5/5 commits comply with specs/002 Conventional Commits.
```

