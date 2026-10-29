# SKILL: Grill-Me (Pre-Implementation Edge-Case Interview)
> Reference: [1. grill-me]
> Purpose: Extract hidden requirements, unearth edge cases, and eliminate assumptions before code generation.

---

## 1. When to Use
- Whenever a task, feature request, or refactoring scope has multiple possible interpretations.
- Before editing core domain contracts in `docs/SPEC.md` or `docs/APIS.md`.
- When encountering ambiguous edge cases (e.g., null values, network partition handling, concurrent operations).

---

## 2. Procedure
1. **Analyze Incoming Request:**
   - Identify implicit assumptions, unstated error paths, and missing schema bounds.
2. **Draft Up to 5 Adversarial Questions:**
   - Formulate specific, high-leverage multiple-choice or short-answer questions.
   - Example categories:
     - *State Boundary:* "What happens if a user submits an empty task payload?"
     - *Concurrency:* "How should duplicate simultaneous requests be handled (idempotency key vs DB constraint)?"
     - *Auth/Permission:* "Can guest users read public tasks, or is auth strictly required?"
3. **Present Questions to User:**
   - Provide recommended defaults for each question.
   - Halt execution and await explicit user responses.
4. **Lock Answers into Documentation:**
   - Record user choices directly into `docs/SPEC.md` under "Invariants".
   - Proceed to `skills/super-tdd.md`.
