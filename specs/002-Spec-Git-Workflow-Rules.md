# GitHub Workflow Specification (GITHUB-WORKFLOW.md)

> **Mandate:** Every feature, update, and bugfix in this repository follows this lifecycle, from repository binding to branch cleanup. It provides a standardized, production-grade Git workflow adapted to spec-driven development, conventional commits, and automated quality gates.

```
PHASE 1  one-time setup ─► PHASE 2  sync + branch ─► PHASE 3  five gates (no commits yet)
   ─► PHASE 4  stage + conventional commit ─► PHASE 5  HUMAN approval ─► push
   ─► PHASE 6  PR + review + merge ─► PHASE 7  sync main + HUMAN approval ─► delete branch
```

Claude Code / Antigravity enforces the two human gates mechanically: configuration and agent hooks set `git push`, `git branch -d/-D`, `git reset --hard` and `git remote add/set-url` to **ask** for permission every time ([HOOKS.md](http://HOOKS.md)).

---

## Phase 1 — One-time setup

```sh
git init
git config user.name  "<your-name-or-bot-identity>"
git config user.email "<your-email@domain.com>"
git remote add origin "https://github.com/<org-or-user>/<repository-name>.git"
git branch -M main
```

> **Repository Isolation:** Configured via repo-local git config (`.git/config`) to isolate project identity, email, and origin remote without mutating global user configuration.

## Phase 2 — Pre-development sync & branch

```sh
git checkout main
git pull origin main
git status                       # must be clean
git checkout -b "features/<slug>"
```

Branch names: `features/<slug>`, `fix/<slug>`, `docs/<slug>` (lowercase, hyphenated, matching the task/feature title). When using spec-kit, the spec folder `specs/NNN-<slug>/` and the branch `features/<slug>` share the slug.

## Phase 3 — The five quality gates (hold all commits)

| Gate | Requirement | Command / evidence |
| :---- | :---- | :---- |
| **1 Task** | Change traces to [PRD.md](http://PRD.md) / [SPEC.md](http://SPEC.md) or a `specs/NNN-*/spec.md`; modules stay in their layer (`src/`, `backend/`, `frontend/`, `auth/`, `connectors/`) | Spec/task ID in the PR |
| **2 Build** | Backend imports cleanly; frontend builds if touched | see below |
| **3 Validate** | Security spec rules hold for the diff | checklist below |
| **4 Test** | Full suite, 100 % pass, no regressions | `.venv/Scripts/python.exe -m pytest` |
| **5 Review** | Self-review against [CODE-REVIEW.md](http://CODE-REVIEW.md) | `/code-review` or `requesting-code-review` skill |

**Gate 2 commands (PowerShell):**

```powershell
$env:JWT_SECRET_KEY = & .venv/Scripts/python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
& .venv/Scripts/python.exe -c "import src.auth, src.services; print('App syntax OK')"
.venv/Scripts/ruff.exe check .
cd frontend; npm run build    # only when frontend/ changed
```

&nbsp;

**Gate 3 checklist** ([specs/001-Spec-Security-guide.md](http://specs/001-Spec-Security-guide.md)):

- **AUTH** — new `/api/*` routes are under a router with `dependencies=[Depends(get_current_user)]` (only health is public).  
- **IDOR** — every tenant/store or user-owned object is checked with `require_store_access(store_id, principal)` / `principal.can_access_store(...)`.  
- **SEC** — no secrets in the diff; `.env` not staged (`git status` must not list it).  
- **INP** — Pydantic models with bounds (`max_length`, `ge/le`, `Literal`); uploads ≤ `MAX_UPLOAD_BYTES` (10 MB) with magic-byte type check.  
- **WEB** — `install_hardening(app)` applied (CSP, `X-Frame-Options`, `X-Content-Type-Options`, CORS allow-list).  
- **Tests** — at least one negative test per new control in `tests/test_security.py` or `tests/test_auth.py`.

## Phase 4 — Stage & commit (Conventional Commits)

```sh
git status
git add <paths>          # prefer explicit paths; never stage .env, certs/, *.key
git status               # re-verify
git commit -m "<type>(<scope>): <imperative summary>"
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `perf`. Scopes: `edge`, `api`, `agents`, `web`, `security`, `docs`, `infra`.

```
feat(api): enforce store-scoped JWT auth on all REST routes
fix(ocr): return 422 instead of max markdown when expiry date is unreadable
docs(security): add PROJECT_PROFILE and SECURITY_REPORT
```

## Phase 5 — Push (human-in-the-loop, mandatory)

AI agents never push on their own. They ask:

> "All 5 gates passed (tests: N/N). Commit `<hash>` is ready on `features/<slug>`. Push to origin?"

On explicit approval: `git push origin "features/<slug>"`.

## Phase 6 — Pull request & merge

1. Open a PR `features/<slug>` → `main` using the template in [CODE-REVIEW.md §3](http://CODE-REVIEW.md).  
2. CI must pass (the `security.yml` workflow is planned as TSK-603).  
3. Lead/admin review against [CODE-REVIEW.md](http://CODE-REVIEW.md); squash or merge.

## Phase 7 — Sync & branch cleanup

```sh
git checkout main
git pull origin main
```

Ask: *"`features/<slug>` is merged and pulled. May I delete the local branch?"* Then on approval: `git branch -d "features/<slug>"` (use `-D` only after a squash-merge, and only with approval).