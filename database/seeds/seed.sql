-- Seed: Initial test users and baseline spec task
-- Reference: docs/DATABASE.md

INSERT OR IGNORE INTO users (id, email, role)
VALUES ('u_admin_01', 'admin@agentic.sdd', 'architect');

INSERT OR IGNORE INTO tasks (id, user_id, title, status, spec_ref, invariants)
VALUES (
    't_init_01',
    'u_admin_01',
    'Scaffold SDD Agentic Architecture',
    'VERIFIED',
    'docs/SPEC.md#L45',
    '["Zero unbounded mutation", "Deterministic rollback", "Surgical diff bounds"]'
);
