# ERROR HANDLING TRACKER: Known Edge Cases & Reproduction Traces
> Purpose: Living incident registry & regression prevention

---

## 1. Registry Format
Each incident or edge case must be logged with:
- **ID:** Unique issue identifier (e.g., `ERR-001`)
- **Category:** Domain / Network / Concurrency / Parsing / Security
- **Symptom:** Observed failure or error trace
- **Root Cause:** Underlying architectural or logic bug
- **Reproduction Steps / Test Case:** Path to deterministic test reproducing the issue
- **Resolution:** Surgical patch applied & verified

---

## 2. Active Registry

### [ERR-001] Line-Ending Discrepancies on Windows Git Checkout
- **Category:** Environment / Hooks
- **Symptom:** Shell scripts in `hooks/` failing with `\r` unexpected character errors in WSL or Linux containers.
- **Root Cause:** Git autocrlf altering line endings to CRLF on Windows hosts.
- **Reproduction:** Run `.sh` hook directly inside bash without `.gitattributes` LF enforcement.
- **Resolution:** Added `.gitattributes` with `* text=auto eol=lf` for `*.sh` and hook files.

### [ERR-002] Concurrent Vector Store SQLite Lock Contention
- **Category:** Concurrency / Memory
- **Symptom:** `sqlite3.OperationalError: database is locked` when multiple agents write to `connectors/vector-memory`.
- **Root Cause:** Default SQLite connection lacking WAL (Write-Ahead Logging) mode and busy timeout.
- **Reproduction:** Fire 5 concurrent async write tasks into `store.py`.
- **Resolution:** Enabled `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;` on store initialization.
