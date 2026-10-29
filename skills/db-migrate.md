# SKILL: DB-Migrate (Database Migration & Rollback Lifecycle)
> Purpose: Deterministic schema evolution with guaranteed zero-loss rollback

---

## 1. Migration File Standard
All migrations live in `database/migrations/` and follow the naming format:
`YYYYMMDD_HHMMSS_<action_description>.sql`

Every file MUST contain explicit `-- UP` and `-- DOWN` blocks:
```sql
-- UP
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- DOWN
DROP TABLE IF EXISTS tasks;
```

---

## 2. Execution Workflow
1. **Author Schema Delta:** Draft the changes adhering to `docs/DATABASE.md`.
2. **Author Reversible Migration:** Create the migration file with matching UP and DOWN SQL.
3. **Dry-Run Rollback Test:**
   - Execute UP against test database.
   - Verify tables/columns created.
   - Execute DOWN against test database.
   - Verify state returns exactly to pre-migration baseline.
   - Execute UP once more.
4. **Update ER Documentation:** Update the diagram in `docs/DATABASE.md`.
