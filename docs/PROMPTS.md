# PROMPTS: Reusable Agent Prompt Snippets
> Purpose: Standardized invocation commands for agent workflows
> Formats: Slash commands & trigger blocks

---

## 1. `/grill-me` (Edge-Case & Spec Extraction)
```markdown
You are an adversarial Systems Architect and Lead QA Engineer.
Before writing any code or modifying existing contracts:
1. Challenge all assumptions in the request.
2. Probe for corner cases (empty payloads, network partitions, race conditions, type mismatches).
3. Ask up to 5 pointed, high-impact multiple-choice or short-answer questions.
4. Stop immediately after asking and wait for user clarification.
```

---

## 2. `/distill` (Context Compaction & Memory Sync)
```markdown
Analyze the current session trajectory and distill the core knowledge:
1. Extract newly established domain invariants into `docs/SPEC.md`.
2. Record durable technical facts, decisions, and resolved bugs into `docs/MEMORY.md`.
3. Strip ephemeral conversational back-and-forth and summarize remaining blockers.
4. Output a clean, updated state checkpoint for future sessions.
```

---

## 3. `/octo:review` (Multi-Model Consensus Review)
```markdown
Act as the Consensus Verification Arbiter.
Review the proposed patch against the following strict criteria:
- Contract Adherence: Does this strictly follow `docs/SPEC.md`?
- Simplicity: Does this follow `docs/RULES.md` without speculative bloat?
- Security: Are input validation, auth rules, and zero-trust policies intact?
- Test Completeness: Are there unit/integration tests confirming the behavior?
Return a structured table: [Model Name | Verdict (APPROVE/REJECT) | Detailed Findings].
```

---

## 4. `/tdd:red` (Red-Green-Refactor Trigger)
```markdown
Generate ONLY the failing unit test for the described feature.
- Follow the Arrange-Act-Assert pattern.
- Run the test suite and confirm it fails for the EXACT expected reason.
- Do NOT generate production code yet.
```
