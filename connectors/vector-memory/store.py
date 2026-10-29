#!/usr/bin/env python3
"""
Vector Memory Store
Reference: [6. claude-mem]
Persistent SQLite-backed entity, fact, and context store for cross-session agent memory.
"""

import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timezone

class VectorMemoryStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path), timeout=5.0)
        # Enable Write-Ahead Logging & busy timeout for concurrency (fixes ERR-002)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_entities (
                    id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_key ON memory_entities(key);")
            conn.commit()

    def set(self, category: str, key: str, value: str):
        now = datetime.now(timezone.utc).isoformat()
        entity_id = f"{category}:{key}"
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO memory_entities (id, category, key, value, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at;
            """, (entity_id, category, key, value, now))
            conn.commit()

    def get(self, category: str, key: str) -> str | None:
        entity_id = f"{category}:{key}"
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT value FROM memory_entities WHERE id = ?;", (entity_id,))
            row = cursor.fetchone()
            return row[0] if row else None

    def list_all(self) -> list[dict]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT id, category, key, value, updated_at FROM memory_entities;")
            return [
                {"id": r[0], "category": r[1], "key": r[2], "value": r[3], "updated_at": r[4]}
                for r in cursor.fetchall()
            ]

    def sync_from_markdown(self, markdown_path: Path):
        """Parse docs/MEMORY.md and synchronize durable facts."""
        if not markdown_path.exists():
            return
        content = markdown_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("- **[FACT-"):
                parts = line.split("]**", 1)
                if len(parts) == 2:
                    fact_key = parts[0].replace("- **[", "").strip()
                    fact_val = parts[1].strip()
                    self.set("facts", fact_key, fact_val)

def main():
    root = Path(__file__).resolve().parent.parent.parent
    db_file = root / "connectors" / "vector-memory" / "memory.db"
    store = VectorMemoryStore(db_file)

    if "--sync" in sys.argv:
        md_file = root / "docs" / "MEMORY.md"
        store.sync_from_markdown(md_file)
        print(f"[VECTOR-MEMORY] Synced facts from {md_file}. Total entities: {len(store.list_all())}")
    elif "--dump" in sys.argv:
        print(json.dumps(store.list_all(), indent=2))
    else:
        print(f"[VECTOR-MEMORY] Store ready at {db_file}. Use --sync or --dump.")

if __name__ == "__main__":
    main()
