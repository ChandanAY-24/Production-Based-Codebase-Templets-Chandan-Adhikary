# Vector Memory Connector
> Reference: [6. claude-mem]
> Purpose: SQLite / local vector store backing persistent cross-session facts

---

## Functionality
- Acts as local fast retrieval memory across agent context compactions and new sessions.
- Ingests structured facts from `docs/MEMORY.md` via `python store.py --sync`.
- Safe concurrent read/write enabled via SQLite Write-Ahead Logging (`WAL`).
