---
name: clarify
description: "Executes the Grill-Me pre-implementation protocol. Probes ambiguous requirements, identifies edge cases, resolves invariants, and prevents guesswork before coding begins."
---

# `/clarify` — The Grill-Me Protocol & Requirement Disambiguator

> **Directives:** `docs/CONSTITUTION.md` (Prime Directive 1: Never Assume — Always Verify), `skills/grill-me.md`  
> **Rule:** Never guess data shapes, domain rules, or error behaviors.

Use this slash command whenever a prompt, feature request, or bug report has missing constraints, underspecified schemas, or ambiguous edge cases.

---

## When to Trigger `/clarify`
Trigger this command immediately when:
1. The user asks to build a feature without specifying schema fields, error states, or authorization roles.
2. A database schema, migration, or external API integration lacks explicit contracts.
3. Edge cases (rate limiting, timeouts, concurrency, rollback strategies) are not documented.
4. Security trust boundaries or tenant isolation rules are unspecified.

---

## The Grill-Me Interrogation Structure
Formulate **2 to 4 high-impact, targeted questions** using this structure:

### 1. Identify Implicit Assumptions
State the assumption or ambiguity explicitly:
> *"The requirement states 'users can export tasks', but does not specify file format or authorization scope."*

### 2. Present Structured Options
Offer concrete choices (with a recommended default where applicable):
```markdown
1. Which export format and authorization level is required?
   - [ ] (Recommended) JSON with strict schema validation; restricted to users with `task:export` RBAC scope.
   - [ ] CSV stream with rate limiting (max 10 exports / hour).
   - [ ] Unauthenticated public download. (Violates Gate 3 security guidelines)
```

### 3. Invariant & Boundary Probing
Ask about critical limits:
- Maximum payload / file size? (Default: 1MB, max 10MB)
- Tenant isolation: Can admin cross store/tenant boundaries (`IDOR isolation`)?
- Rollback policy: On partial failure, should mutations roll back atomically?

---

## Invariant Crystallization
Once the user responds:
1. Record the agreed-upon contracts in `docs/SPEC.md` or the active feature spec under `Invariants & Domain Contracts`.
2. Update `docs/PLAN.md` with the verified requirements.
3. Proceed safely to `/plan` or `/implement`.

