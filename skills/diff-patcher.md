# SKILL: Diff-Patcher (Unified Diff Formatting & Validation)
> Reference: [7. ponytail]
> Standard: Exact, Contiguous Patch Application

---

## 1. Objectives
- Prevent whole-file re-writes during automated agent edits.
- Enforce strict whitespace and line boundary preservation.
- Ensure rollback capability if a patch fails to apply cleanly.

---

## 2. Surgical Diff Rules
1. **Target Contiguity:** All replacements must target a single contiguous block of code.
2. **Context Window:** Include 2-3 lines of unchanged surrounding context to guarantee deterministic matching.
3. **Zero Whitespace Distortion:** Preserve existing indentation (tabs vs 2/4 spaces).
4. **Validation Pipeline:**
   ```bash
   git apply --check patch.diff
   ```
   If `--check` fails, DO NOT attempt fuzzy matching or force apply. Abort and re-read file offsets.

---

## 3. Patch Template
```diff
--- a/src/auth.py
+++ b/src/auth.py
@@ -24,7 +24,7 @@ def verify_jwt(token: str) -> dict:
     except ExpiredSignatureError:
-        return None
+        raise TokenExpiredException("JWT token has expired")
     except JWTError:
```
