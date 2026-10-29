# RULES: Karpathy Simplicity & Surgical Engineering
> Reference: [3. karpathy-skills]
> Philosophy: "Write plain code. Don't build empires. Edit with a laser."

---

## 1. Simplicity First
- **Vanilla Over Magic:** Prefer straightforward standard-library functions or lightweight idiomatic solutions over heavyweight metaprogramming or complex dependency chains.
- **Readable Flow:** Readability always trumps clever one-liners. A flat pipeline of transparent steps beats recursive generator gymnastics.
- **Minimal Dependencies:** Audit third-party packages ruthlessly. Every new package in `requirements.txt` or `package.json` must have documented justification in `TECH-STACKS.md`.

---

## 2. Surgical Modification Policy
- **Contiguous Edits Only:** Never overwrite unchanged methods, headers, or licenses. Use surgical search/replace operations.
- **Preserve Comments & Docstrings:** Do not wipe out preexisting developer annotations unless explicitly asked to refactor them.
- **Maintain Invariants:** Check `docs/SPEC.md` invariants before touching core domain handlers. Any patch violating a contract will be rejected by `hooks/post-code-generation.sh`.

---

## 3. Communication Rules
- **No Apologies:** Never say "I apologize for the oversight" or "You are correct!". Immediately diagnose the issue, state the root cause in one sentence, and provide the fix.
- **Diff Transparency:** State exact files modified, functions touched, and lines affected.
- **Structured Explanations:** Use standard Markdown headers, tables, and short bullet points.
