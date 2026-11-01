#!/usr/bin/env python3
"""
Task Checklist: Production-grade OpenXML XLSX Generator & Synchronization Engine
Maintains Task-Checklist.xlsx at workspace root without external dependencies.
Features automated synchronization with docs/TASKS.md to stay always up to date.
"""

import argparse
import html
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
XLSX_PATH = WORKSPACE_ROOT / "Task-Checklist.xlsx"
DATA_BACKUP_PATH = WORKSPACE_ROOT / ".agents" / "task-checklist-data.json"
TASKS_MD_PATH = WORKSPACE_ROOT / "docs" / "TASKS.md"

COLUMNS = [
    ("Checklist-ID", 14),
    ("Task-ID", 12),
    ("Phase", 26),
    ("Category / Area", 24),
    ("Checklist Description", 45),
    ("Priority", 10),
    ("Status", 14),
    ("Assigned Agent / Role", 22),
    ("Verification Command / Method", 40),
    ("Evidence / Artifact Link", 32),
    ("Created Date-Time", 20),
    ("Last Updated Date-Time", 20),
    ("Notes & Invariants", 30)
]

SEED_ENTRIES = [
    # 3.1 Security, Auth & Quality Gates
    {
        "checklist_id": "TC-001",
        "task_id": "TSK-101",
        "phase": "Phase 1: Architecture & Invariants",
        "category": "Architecture & Schemas",
        "description": "Formalize Core Invariants & Schemas (INV-001 to INV-004 locked)",
        "priority": "P0",
        "status": "VERIFIED",
        "assigned": "Systems Architect",
        "command": ".venv\\Scripts\\python.exe .agents/scripts/validator.py",
        "evidence": "docs/SPEC.md, src/models.py",
        "created_at": "2026-10-30 08:00:00",
        "updated_at": "2026-10-30 09:30:00",
        "notes": "Invariants locked: INV-001 through INV-004."
    },
    {
        "checklist_id": "TC-002",
        "task_id": "TSK-102",
        "phase": "Phase 2: Security & Auth",
        "category": "Security & Auth",
        "description": "Store-Scoped JWT Auth & Timing-Safe Verification (HMAC-SHA256, scrypt KDF)",
        "priority": "P0",
        "status": "VERIFIED",
        "assigned": "Security Engineer",
        "command": ".venv\\Scripts\\python.exe -m pytest tests/test_auth.py -v",
        "evidence": "src/auth.py, tests/test_auth.py",
        "created_at": "2026-10-30 08:30:00",
        "updated_at": "2026-10-30 09:45:00",
        "notes": "Constant-time secrets.compare_digest active."
    },
    {
        "checklist_id": "TC-003",
        "task_id": "TSK-103",
        "phase": "Phase 2: Security & Auth",
        "category": "Security & AST",
        "description": "AST Security Scanner & Pre-Commit Hook (block eval/exec, leaks, shell=True)",
        "priority": "P0",
        "status": "VERIFIED",
        "assigned": "Security Engineer",
        "command": "python hooks/commit-guardian.py --ast-only",
        "evidence": "hooks/commit-guardian.py",
        "created_at": "2026-10-30 08:45:00",
        "updated_at": "2026-10-30 09:50:00",
        "notes": "Strix AST security baseline active."
    },
    {
        "checklist_id": "TC-004",
        "task_id": "TSK-104",
        "phase": "Phase 2: Security & Auth",
        "category": "Testing & Sandbox",
        "description": "Fix Sandboxed Socket Binding in Security Test Runner (mock transport)",
        "priority": "P0",
        "status": "VERIFIED",
        "assigned": "QA / Dev",
        "command": ".venv\\Scripts\\python.exe -m pytest tests/test_security.py -v",
        "evidence": "tests/test_security.py",
        "created_at": "2026-10-30 11:00:00",
        "updated_at": "2026-10-30 12:00:00",
        "notes": "Zero TCP binding dependencies in sandbox."
    },
    {
        "checklist_id": "TC-005",
        "task_id": "TSK-603",
        "phase": "Phase 3: CI/CD & Automation",
        "category": "Git & CI/CD",
        "description": "CI/CD Automated Security Gate Workflow (dependent code-testing -> code-review)",
        "priority": "P0",
        "status": "VERIFIED",
        "assigned": "DevOps Engineer",
        "command": ".venv\\Scripts\\python.exe .agents/scripts/workflow-orchestrator.py",
        "evidence": ".github/workflows/security.yml",
        "created_at": "2026-10-31 01:00:00",
        "updated_at": "2026-11-01 16:21:00",
        "notes": "Two-phase sequential GitHub Actions pipeline."
    },
    # 3.2 Git Workflow & Frontend Tooling
    {
        "checklist_id": "TC-006",
        "task_id": "TSK-601",
        "phase": "Phase 3: CI/CD & Automation",
        "category": "Git & Quality Gates",
        "description": "Git 7-Phase Workflow & Quality Gate Automation (/git-log conventional commit check)",
        "priority": "P1",
        "status": "VERIFIED",
        "assigned": "DevOps Engineer",
        "command": ".venv\\Scripts\\python.exe .agents/scripts/git-log-auditor.py --limit 10",
        "evidence": "specs/002-Spec-Git-Workflow-Rules.md",
        "created_at": "2026-10-31 00:30:00",
        "updated_at": "2026-11-01 16:18:00",
        "notes": "100% conventional commit compliance."
    },
    {
        "checklist_id": "TC-007",
        "task_id": "TSK-602",
        "phase": "Phase 3: CI/CD & Automation",
        "category": "Frontend Tooling",
        "description": "Frontend / Web Build Tooling Resolution (npm run build and lockfile)",
        "priority": "P1",
        "status": "PENDING",
        "assigned": "Frontend Engineer",
        "command": "cd frontend && npm run build",
        "evidence": "frontend/index.html",
        "created_at": "2026-10-31 00:40:00",
        "updated_at": "2026-10-31 00:40:00",
        "notes": "Pending client build pipeline resolution."
    },
    {
        "checklist_id": "TC-008",
        "task_id": "TSK-604",
        "phase": "Phase 3: CI/CD & Automation",
        "category": "Documentation",
        "description": "Document Architecture & Workflow Synchronization (GITHUB-WORKFLOW, APIS, RULES)",
        "priority": "P1",
        "status": "VERIFIED",
        "assigned": "Systems Architect",
        "command": "git status docs/",
        "evidence": "docs/GITHUB-WORKFLOW.md",
        "created_at": "2026-10-31 00:45:00",
        "updated_at": "2026-11-01 14:30:00",
        "notes": "Full documentation synchronization verified."
    },
    # 3.3 Scalability & Performance Optimization
    {
        "checklist_id": "TC-009",
        "task_id": "TSK-301",
        "phase": "Phase 4: Scalability & Performance",
        "category": "Performance Audit",
        "description": "Full Architecture & Backend Performance Audit (eliminate slow endpoints & N+1 queries)",
        "priority": "P1",
        "status": "IN_PROGRESS",
        "assigned": "Performance Engineer",
        "command": ".venv\\Scripts\\python.exe .agents/scripts/performance-audit.py",
        "evidence": "specs/003-Spec-Scalibility-optimization.md",
        "created_at": "2026-11-01 14:00:00",
        "updated_at": "2026-11-01 14:27:00",
        "notes": "Active profiling on serialization overhead."
    },
    {
        "checklist_id": "TC-010",
        "task_id": "TSK-302",
        "phase": "Phase 4: Scalability & Performance",
        "category": "Database Optimization",
        "description": "Database Query Optimization & Index Hardening (composite indexes, cursor pagination)",
        "priority": "P1",
        "status": "PENDING",
        "assigned": "Database Engineer",
        "command": ".venv\\Scripts\\python.exe -m pytest tests/test_services.py",
        "evidence": "docs/DATABASE.md",
        "created_at": "2026-11-01 14:00:00",
        "updated_at": "2026-11-01 14:00:00",
        "notes": "Cursor pagination schema design."
    },
    {
        "checklist_id": "TC-011",
        "task_id": "TSK-303",
        "phase": "Phase 4: Scalability & Performance",
        "category": "Stress Harness",
        "description": "High-Traffic Concurrency Stress Harness (100-10k users, p95 <= 500ms)",
        "priority": "P2",
        "status": "PENDING",
        "assigned": "SRE / DevOps",
        "command": "locust -f tests/load_test.py --headless",
        "evidence": "specs/003 §Phase 5",
        "created_at": "2026-11-01 14:00:00",
        "updated_at": "2026-11-01 14:00:00",
        "notes": "Target: 1k concurrent users sustained."
    },
    {
        "checklist_id": "TC-012",
        "task_id": "TSK-304",
        "phase": "Phase 4: Scalability & Performance",
        "category": "Web Vitals",
        "description": "Frontend Core Web Vitals & Asset Optimization (LCP <= 2.5s, INP <= 200ms)",
        "priority": "P2",
        "status": "PENDING",
        "assigned": "Frontend Engineer",
        "command": "npx lighthouse http://localhost:3000 --chrome-flags=\"--headless\"",
        "evidence": "frontend/index.html",
        "created_at": "2026-11-01 14:00:00",
        "updated_at": "2026-11-01 14:00:00",
        "notes": "Critical CSS inlining & bundle minimization."
    },
    {
        "checklist_id": "TC-013",
        "task_id": "TSK-305",
        "phase": "Phase 4: Scalability & Performance",
        "category": "Caching Tier",
        "description": "Shared Cache & Redis Tier Implementation (cache-aside for hot tasks & auth tokens)",
        "priority": "P2",
        "status": "PENDING",
        "assigned": "Systems Architect",
        "command": ".venv\\Scripts\\python.exe -m pytest tests/test_cache.py",
        "evidence": "src/services.py",
        "created_at": "2026-11-01 14:00:00",
        "updated_at": "2026-11-01 14:00:00",
        "notes": "Redis sentinel connection pool."
    },
    {
        "checklist_id": "TC-014",
        "task_id": "TSK-306",
        "phase": "Phase 4: Scalability & Performance",
        "category": "Token Optimization",
        "description": "Production Context Window & Token Optimization Engine (surgical reads, token-guard)",
        "priority": "P1",
        "status": "VERIFIED",
        "assigned": "Systems Architect",
        "command": "python .agents/hooks/token-guard.py --audit",
        "evidence": ".agents/rules/token-optimization.md",
        "created_at": "2026-11-01 14:20:00",
        "updated_at": "2026-11-01 14:40:00",
        "notes": "Token limits locked at 4,000 output tokens."
    },
    # Phase 5 Release Sign-Off Gates
    {
        "checklist_id": "TC-015",
        "task_id": "CHK-001",
        "phase": "Phase 5: Release Sign-Off",
        "category": "Release Readiness",
        "description": "Full-Stack Codebase Health Validation (/validate 5/5 quality gates pass)",
        "priority": "P0",
        "status": "VERIFIED",
        "assigned": "Lead Architect",
        "command": ".venv\\Scripts\\python.exe .agents/scripts/validator.py",
        "evidence": ".agents/scripts/validator.py",
        "created_at": "2026-11-01 16:15:00",
        "updated_at": "2026-11-01 16:23:00",
        "notes": "Full-stack validator passing clean."
    },
    {
        "checklist_id": "TC-016",
        "task_id": "CHK-002",
        "phase": "Phase 5: Release Sign-Off",
        "category": "Release Readiness",
        "description": "Error Registry Audit (Error-Tracker.xlsx zero open critical blockers)",
        "priority": "P0",
        "status": "VERIFIED",
        "assigned": "Security Engineer",
        "command": ".venv\\Scripts\\python.exe .agents/scripts/error-tracker.py list",
        "evidence": "Error-Tracker.xlsx",
        "created_at": "2026-11-01 16:15:00",
        "updated_at": "2026-11-01 16:22:00",
        "notes": "5 recorded incidents all marked VERIFIED."
    }
]


def load_entries() -> list[dict]:
    """Load registry entries from JSON store or fallback to seed entries."""
    if DATA_BACKUP_PATH.exists():
        try:
            with open(DATA_BACKUP_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return list(SEED_ENTRIES)


def save_entries(entries: list[dict]):
    """Save entries to persistent JSON store."""
    DATA_BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def col_letter(idx: int) -> str:
    """Convert 0-based column index to Excel column letters (A, B, C...)."""
    result = ""
    while idx >= 0:
        result = chr(65 + (idx % 26)) + result
        idx = (idx // 26) - 1
    return result


def build_sheet_xml(entries: list[dict]) -> str:
    """Build OpenXML sheet1.xml with styled headers, custom widths, and conditional formatting styles."""
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
        '  <sheetViews><sheetView tabSelected="1" workbookViewId="0"/></sheetViews>',
        '  <sheetFormatPr defaultRowHeight="20"/>',
        '  <cols>'
    ]

    for col_idx, (_, width) in enumerate(COLUMNS):
        c_num = col_idx + 1
        xml_parts.append(f'    <col min="{c_num}" max="{c_num}" width="{width}" customWidth="1"/>')
    xml_parts.append('  </cols>')
    xml_parts.append('  <sheetData>')

    # Header Row (Row 1, style 1: Navy/Slate header)
    xml_parts.append('    <row r="1" ht="26" customHeight="1">')
    for col_idx, (col_name, _) in enumerate(COLUMNS):
        cell_ref = f"{col_letter(col_idx)}1"
        escaped_val = html.escape(col_name)
        xml_parts.append(
            f'      <c r="{cell_ref}" s="1" t="inlineStr"><is><t>{escaped_val}</t></is></c>'
        )
    xml_parts.append('    </row>')

    # Data Rows (Row 2+)
    for r_idx, entry in enumerate(entries, start=2):
        status_val = str(entry.get("status", "PENDING")).upper()
        # Choose status style:
        # 2: Default Normal
        # 3: Zebra row
        # 4: VERIFIED (Green #E2EFDA)
        # 5: IN_PROGRESS (Amber #FFF2CC)
        # 6: BLOCKED (Coral #FCE4D6)
        is_zebra = (r_idx % 2 == 1)
        base_style = "3" if is_zebra else "2"

        xml_parts.append(f'    <row r="{r_idx}" ht="24" customHeight="1">')

        row_vals = [
            entry.get("checklist_id", f"TC-{r_idx-1:03d}"),
            entry.get("task_id", ""),
            entry.get("phase", ""),
            entry.get("category", ""),
            entry.get("description", ""),
            entry.get("priority", "P1"),
            entry.get("status", "PENDING"),
            entry.get("assigned", "Unassigned"),
            entry.get("command", ""),
            entry.get("evidence", ""),
            entry.get("created_at", ""),
            entry.get("updated_at", ""),
            entry.get("notes", "")
        ]

        for col_idx, val in enumerate(row_vals):
            cell_ref = f"{col_letter(col_idx)}{r_idx}"
            escaped_val = html.escape(str(val))

            # Style column 6 (Status) with distinctive soft colors
            if col_idx == 6:
                if "VERIFIED" in status_val:
                    cell_style = "4"
                elif "PROGRESS" in status_val:
                    cell_style = "5"
                elif "BLOCKED" in status_val:
                    cell_style = "6"
                else:
                    cell_style = base_style
            else:
                cell_style = base_style

            xml_parts.append(
                f'      <c r="{cell_ref}" s="{cell_style}" t="inlineStr"><is><t>{escaped_val}</t></is></c>'
            )
        xml_parts.append('    </row>')

    xml_parts.append('  </sheetData>')
    xml_parts.append('</worksheet>')
    return "\n".join(xml_parts)


def build_styles_xml() -> str:
    """Build OpenXML styles.xml with corporate palette."""
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3">
    <font><name val="Segoe UI"/><sz val="10"/><color rgb="FF000000"/></font>
    <font><b/><name val="Segoe UI"/><sz val="11"/><color rgb="FFFFFFFF"/></font>
    <font><b/><name val="Segoe UI"/><sz val="10"/><color rgb="FF1B365D"/></font>
  </fonts>
  <fills count="7">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <!-- 2: Header Dark Navy/Slate #1B365D -->
    <fill><patternFill patternType="solid"><fgColor rgb="FF1B365D"/></patternFill></fill>
    <!-- 3: Zebra Row #F8F9FA -->
    <fill><patternFill patternType="solid"><fgColor rgb="FFF8F9FA"/></patternFill></fill>
    <!-- 4: VERIFIED Soft Green #E2EFDA -->
    <fill><patternFill patternType="solid"><fgColor rgb="FFE2EFDA"/></patternFill></fill>
    <!-- 5: IN_PROGRESS Soft Amber #FFF2CC -->
    <fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/></patternFill></fill>
    <!-- 6: BLOCKED Soft Coral #FCE4D6 -->
    <fill><patternFill patternType="solid"><fgColor rgb="FFFCE4D6"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/></border>
    <border>
      <left style="thin"><color rgb="FFD9D9D9"/></left>
      <right style="thin"><color rgb="FFD9D9D9"/></right>
      <top style="thin"><color rgb="FFD9D9D9"/></top>
      <bottom style="thin"><color rgb="FFD9D9D9"/></bottom>
    </border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="7">
    <!-- 0: Default -->
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <!-- 1: Header (Navy, White Bold, Center, Border) -->
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="center" vertical="center" wrapText="1"/>
    </xf>
    <!-- 2: Normal Row (White, Segoe UI 10, Border, Wrap) -->
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment vertical="center" wrapText="1"/>
    </xf>
    <!-- 3: Zebra Row (#F8F9FA, Segoe UI 10, Border, Wrap) -->
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment vertical="center" wrapText="1"/>
    </xf>
    <!-- 4: VERIFIED (Green #E2EFDA, Border, Center, Wrap) -->
    <xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="center" vertical="center" wrapText="1"/>
    </xf>
    <!-- 5: IN_PROGRESS (Amber #FFF2CC, Border, Center, Wrap) -->
    <xf numFmtId="0" fontId="0" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="center" vertical="center" wrapText="1"/>
    </xf>
    <!-- 6: BLOCKED (Coral #FCE4D6, Border, Center, Wrap) -->
    <xf numFmtId="0" fontId="0" fillId="6" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="center" vertical="center" wrapText="1"/>
    </xf>
  </cellXfs>
</styleSheet>"""


def export_xlsx(entries: list[dict]):
    """Assemble OpenXML package and write Task-Checklist.xlsx."""
    sheet_xml = build_sheet_xml(entries)
    styles_xml = build_styles_xml()

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    wb_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    workbook_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Task-Checklist" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""

    with zipfile.ZipFile(XLSX_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/styles.xml", styles_xml)
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)

    save_entries(entries)


def cmd_init():
    """Initialize or reset Task-Checklist.xlsx with comprehensive seed data."""
    entries = load_entries()
    export_xlsx(entries)
    print(f"[TASK-CHECKLIST] [SUCCESS] Generated '{XLSX_PATH.name}' with {len(entries)} items.")


def cmd_sync():
    """Parse docs/TASKS.md and synchronize states, priorities, and updated timestamps."""
    if not TASKS_MD_PATH.exists():
        print(f"[TASK-CHECKLIST] [WARN] '{TASKS_MD_PATH.name}' not found. Skipping markdown parse.")
        return

    content = TASKS_MD_PATH.read_text(encoding="utf-8")
    entries = load_entries()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Match rows like: | **TSK-101** | Title | Priority | Status | Spec | Assigned | Criteria |
    row_pattern = re.compile(
        r"\|\s*\*\*(TSK-\d+)\*\*\s*\|\s*([^|]+)\|\s*(P\d+)\s*\|\s*`?([A-Z_]+)`?\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|"
    )

    synced_count = 0
    existing_map = {e.get("task_id"): e for e in entries if e.get("task_id")}

    for match in row_pattern.finditer(content):
        task_id, title, priority, status, spec_ref, assigned, criteria = [m.strip() for m in match.groups()]
        if task_id in existing_map:
            entry = existing_map[task_id]
            changed = False
            if entry.get("status") != status:
                entry["status"] = status
                changed = True
            if entry.get("priority") != priority:
                entry["priority"] = priority
                changed = True
            if changed:
                entry["updated_at"] = now_str
                synced_count += 1
        else:
            # New task found in TASKS.md
            next_idx = len(entries) + 1
            new_entry = {
                "checklist_id": f"TC-{next_idx:03d}",
                "task_id": task_id,
                "phase": "Active Delivery",
                "category": "Domain Feature",
                "description": title,
                "priority": priority,
                "status": status,
                "assigned": assigned,
                "command": ".venv\\Scripts\\python.exe .agents/scripts/validator.py",
                "evidence": spec_ref,
                "created_at": now_str,
                "updated_at": now_str,
                "notes": criteria
            }
            entries.append(new_entry)
            synced_count += 1

    export_xlsx(entries)
    print(f"[TASK-CHECKLIST] [SUCCESS] Synchronized '{XLSX_PATH.name}': {synced_count} items updated. Total: {len(entries)}.")


def cmd_list():
    """Print structured terminal table of tasks grouped by status."""
    entries = load_entries()
    print("[TASK-CHECKLIST] ===========================================================================================")
    print(f"[TASK-CHECKLIST] Production Task & Release Checklist Registry ({len(entries)} items)")
    print("[TASK-CHECKLIST] ===========================================================================================")
    for e in entries:
        status_tag = f"[{e['status']}]".ljust(14)
        print(f"{status_tag} {e['checklist_id']} | {e['task_id']} ({e['priority']}): {e['description']}")
        print(f"             Phase: {e['phase']} | Area: {e['category']} | Assigned: {e['assigned']}")
        print(f"             Updated: {e['updated_at']} | Cmd: {e['command']}")
        print("  " + "-" * 88)


def cmd_update(args):
    """Update status, timestamp, and notes for a specific checklist item."""
    entries = load_entries()
    target_id = args.id.upper()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    found = False
    for e in entries:
        if e.get("checklist_id") == target_id or e.get("task_id") == target_id:
            e["status"] = args.status.upper()
            e["updated_at"] = now_str
            if args.notes:
                e["notes"] = args.notes
            found = True
            print(f"[TASK-CHECKLIST] [SUCCESS] Updated '{target_id}' -> Status: {e['status']} @ {now_str}")
            break

    if not found:
        print(f"[TASK-CHECKLIST] [ERROR] Item '{target_id}' not found.")
        sys.exit(1)

    export_xlsx(entries)


def cmd_stats():
    """Output completion percentage and SLA status."""
    entries = load_entries()
    total = len(entries)
    if total == 0:
        print("[TASK-CHECKLIST] No entries recorded.")
        return

    verified = sum(1 for e in entries if "VERIFIED" in str(e.get("status", "")).upper())
    in_progress = sum(1 for e in entries if "PROGRESS" in str(e.get("status", "")).upper())
    pending = sum(1 for e in entries if "PENDING" in str(e.get("status", "")).upper())
    blocked = sum(1 for e in entries if "BLOCKED" in str(e.get("status", "")).upper())

    pct_verified = (verified / total) * 100
    print("[TASK-CHECKLIST] =========================================================")
    print(f"[TASK-CHECKLIST] Task Checklist Statistics & SLA Readiness")
    print("[TASK-CHECKLIST] ---------------------------------------------------------")
    print(f"  Total Items:    {total}")
    print(f"  VERIFIED:       {verified} ({pct_verified:.1f}%)")
    print(f"  IN_PROGRESS:    {in_progress}")
    print(f"  PENDING:        {pending}")
    print(f"  BLOCKED:        {blocked}")
    print("[TASK-CHECKLIST] ---------------------------------------------------------")
    verdict = "RELEASE READY" if blocked == 0 and pending == 0 and in_progress == 0 else "DELIVERY IN PROGRESS"
    print(f"[TASK-CHECKLIST] Operational State: {verdict}")
    print("[TASK-CHECKLIST] =========================================================")


def main():
    parser = argparse.ArgumentParser(description="Task Checklist: Production XLSX Generator & Sync Engine")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")

    # init
    subparsers.add_parser("init", help="Initialize or regenerate Task-Checklist.xlsx")

    # sync
    subparsers.add_parser("sync", help="Synchronize task states from docs/TASKS.md")

    # list
    subparsers.add_parser("list", help="List all tracked tasks & checklist items")

    # stats
    subparsers.add_parser("stats", help="Show completion statistics and gate readiness")

    # update
    up_parser = subparsers.add_parser("update", help="Update task status & timestamp")
    up_parser.add_argument("--id", type=str, required=True, help="Checklist-ID (TC-XXX) or Task-ID (TSK-XXX)")
    up_parser.add_argument("--status", type=str, required=True, choices=["VERIFIED", "IN_PROGRESS", "PENDING", "BLOCKED"], help="New status")
    up_parser.add_argument("--notes", type=str, default="", help="Optional notes")

    args = parser.parse_args()

    if args.subcommand == "init" or not args.subcommand:
        cmd_init()
    elif args.subcommand == "sync":
        cmd_sync()
    elif args.subcommand == "list":
        cmd_list()
    elif args.subcommand == "stats":
        cmd_stats()
    elif args.subcommand == "update":
        cmd_update(args)


if __name__ == "__main__":
    main()

