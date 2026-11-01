#!/usr/bin/env python3
"""
Error Tracker: Production-grade OpenXML XLSX Generator & Registry Manager
Maintains Error-Tracker.xlsx at workspace root without external dependencies.
Tracks errors encountered during agent development to prevent regressions.
"""

import argparse
import html
import json
import sys
import zipfile
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
XLSX_PATH = WORKSPACE_ROOT / "Error-Tracker.xlsx"
DATA_BACKUP_PATH = WORKSPACE_ROOT / ".agents" / "error-tracker-data.json"

COLUMNS = [
    ("Error-ID", 12),
    ("Date-times", 20),
    ("Which path", 28),
    ("Which phase", 20),
    ("Describe error", 45),
    ("How to resolve", 45),
    ("Verified", 25),
    ("Important checks & prevention rules", 45)
]

SEED_ENTRIES = [
    {
        "error_id": "ERR-001",
        "date_time": "2026-10-30 08:45:00",
        "path": "hooks/*.sh",
        "phase": "Environment/Hooks",
        "error": "Line-ending discrepancies: shell scripts failing with '\\r' unexpected carriage return character in POSIX runtimes.",
        "resolve": "Added .gitattributes with '* text=auto eol=lf' for all *.sh shell scripts and hook files.",
        "verified": "YES (Verified on git checkout)",
        "checks": "Always enforce LF line endings on executable scripts via .gitattributes."
    },
    {
        "error_id": "ERR-002",
        "date_time": "2026-10-30 09:12:00",
        "path": "connectors/vector-memory/store.py",
        "phase": "Concurrency/Memory",
        "error": "sqlite3.OperationalError: database is locked when multiple agent tasks execute concurrent writes.",
        "resolve": "Enabled 'PRAGMA journal_mode=WAL;' and 'PRAGMA busy_timeout=5000;' on SQLite initialization.",
        "verified": "YES (Concurrency stress verified)",
        "checks": "Always configure WAL journal mode and busy_timeout on SQLite stores."
    },
    {
        "error_id": "ERR-003",
        "date_time": "2026-10-30 11:30:00",
        "path": "tests/test_security.py",
        "phase": "Testing/Sandbox",
        "error": "Socket binding EACCES permission failure during live HTTP server test in restricted sandbox.",
        "resolve": "Implemented mock transport and in-memory test clients instead of live TCP network binding.",
        "verified": "YES (Pytest passing in sandbox)",
        "checks": "Never rely on physical TCP listening sockets in unit test suites; use TestClient / mocks."
    },
    {
        "error_id": "ERR-004",
        "date_time": "2026-11-01 16:18:00",
        "path": "auth/session.py",
        "phase": "Validation/Lint",
        "error": "Flake8 F821 undefined name 'Any' in type annotation: 'List[Dict[str, Any]]'.",
        "resolve": "Added 'Any' to 'from typing import Optional, List, Dict, Any' in auth/session.py.",
        "verified": "YES (Flake8 passed 0 errors)",
        "checks": "Run /validate or flake8 before completing auth/session model modifications."
    },
    {
        "error_id": "ERR-005",
        "date_time": "2026-11-01 16:20:00",
        "path": ".agents/scripts/workflow-orchestrator.py",
        "phase": "Terminal/Encoding",
        "error": "UnicodeEncodeError: 'charmap' codec can't encode emoji character '\\u2705' on Windows cp1252 terminal.",
        "resolve": "Replaced unicode emojis with standard ASCII indicators: [PASS], [FAIL], [SUCCESS].",
        "verified": "YES (Clean exit code 0 on Windows)",
        "checks": "Use pure ASCII tags [PASS]/[FAIL] in Python CLI scripts destined for Windows command line."
    }
]


def load_entries() -> list[dict]:
    """Load registry entries from JSON store."""
    if DATA_BACKUP_PATH.exists():
        try:
            with open(DATA_BACKUP_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return list(SEED_ENTRIES)


def save_entries(entries: list[dict]):
    """Save entries to JSON store."""
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
    """Build OpenXML sheet1.xml with styled headers and data rows."""
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

    # Header Row (Row 1, style 1: Navy header)
    xml_parts.append('    <row r="1" ht="26" customHeight="1">')
    for col_idx, (col_name, _) in enumerate(COLUMNS):
        cell_ref = f"{col_letter(col_idx)}1"
        escaped_val = html.escape(col_name)
        xml_parts.append(
            f'      <c r="{cell_ref}" s="1" t="inlineStr"><is><t>{escaped_val}</t></is></c>'
        )
    xml_parts.append('    </row>')

    # Data Rows (Row 2+, style 2 for normal, style 3 for zebra, style 4 for verified pass)
    for r_idx, entry in enumerate(entries, start=2):
        is_zebra = (r_idx % 2 == 1)
        base_style = "3" if is_zebra else "2"
        xml_parts.append(f'    <row r="{r_idx}" ht="24" customHeight="1">')

        row_vals = [
            entry.get("error_id", f"ERR-{r_idx-1:03d}"),
            entry.get("date_time", ""),
            entry.get("path", ""),
            entry.get("phase", ""),
            entry.get("error", ""),
            entry.get("resolve", ""),
            entry.get("verified", ""),
            entry.get("checks", "")
        ]

        for col_idx, val in enumerate(row_vals):
            cell_ref = f"{col_letter(col_idx)}{r_idx}"
            escaped_val = html.escape(str(val))
            # Column 6 is Verified: if YES, style 4
            style = "4" if (col_idx == 6 and "YES" in str(val).upper()) else base_style
            xml_parts.append(
                f'      <c r="{cell_ref}" s="{style}" t="inlineStr"><is><t>{escaped_val}</t></is></c>'
            )
        xml_parts.append('    </row>')

    xml_parts.append('  </sheetData>')
    xml_parts.append('</worksheet>')
    return "\n".join(xml_parts)


def build_styles_xml() -> str:
    """Build OpenXML styles.xml with corporate colors and fonts."""
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><name val="Segoe UI"/><sz val="10"/><color rgb="FF000000"/></font>
    <font><b/><name val="Segoe UI"/><sz val="11"/><color rgb="FFFFFFFF"/></font>
  </fonts>
  <fills count="5">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF2F4F7"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE2EFDA"/></patternFill></fill>
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
  <cellXfs count="5">
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
    <!-- 3: Zebra Row (Light Gray #F2F4F7, Segoe UI 10, Border, Wrap) -->
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment vertical="center" wrapText="1"/>
    </xf>
    <!-- 4: Verified Pass (Light Green #E2EFDA, Segoe UI 10, Border, Wrap) -->
    <xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment vertical="center" wrapText="1"/>
    </xf>
  </cellXfs>
</styleSheet>"""


def export_xlsx(entries: list[dict]):
    """Assemble OpenXML package and write Error-Tracker.xlsx."""
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
    <sheet name="Error-Log" sheetId="1" r:id="rId1"/>
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
    """Initialize or reset Error-Tracker.xlsx with seed data."""
    entries = load_entries()
    export_xlsx(entries)
    print(f"[ERROR-TRACKER] Successfully generated '{XLSX_PATH.name}' with {len(entries)} entries.")


def cmd_list():
    """Print formatted error registry table."""
    entries = load_entries()
    print("[ERROR-TRACKER] ===========================================================================================")
    print(f"[ERROR-TRACKER] Error Incident & Prevention Registry ({len(entries)} items)")
    print("[ERROR-TRACKER] ===========================================================================================")
    for e in entries:
        print(f"[{e['error_id']}] ({e['phase']}) {e['path']} @ {e['date_time']}")
        print(f"  Error:    {e['error']}")
        print(f"  Resolve:  {e['resolve']}")
        print(f"  Verified: {e['verified']}")
        print(f"  Check:    {e['checks']}")
        print("  " + "-" * 85)


def cmd_add(args):
    """Append a new error incident to the registry."""
    entries = load_entries()
    next_num = len(entries) + 1
    new_id = args.id or f"ERR-{next_num:03d}"
    now_str = args.date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_entry = {
        "error_id": new_id,
        "date_time": now_str,
        "path": args.path,
        "phase": args.phase,
        "error": args.error,
        "resolve": args.resolve,
        "verified": args.verified or "PENDING",
        "checks": args.checks or "Review relevant spec before modification."
    }

    entries.append(new_entry)
    export_xlsx(entries)
    print(f"[ERROR-TRACKER] [SUCCESS] Added incident '{new_id}' to '{XLSX_PATH.name}'.")


def main():
    parser = argparse.ArgumentParser(description="Error Tracker: XLSX Manager & Incident Registry")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")

    # init
    subparsers.add_parser("init", help="Initialize or regenerate Error-Tracker.xlsx")

    # list
    subparsers.add_parser("list", help="List all tracked error incidents")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new error incident")
    add_parser.add_argument("--id", type=str, default=None, help="Error ID (e.g., ERR-006)")
    add_parser.add_argument("--date", type=str, default=None, help="Date-time string")
    add_parser.add_argument("--path", type=str, required=True, help="Affected file or component path")
    add_parser.add_argument("--phase", type=str, required=True, help="Development phase")
    add_parser.add_argument("--error", type=str, required=True, help="Error description & symptom")
    add_parser.add_argument("--resolve", type=str, required=True, help="Resolution applied")
    add_parser.add_argument("--verified", type=str, default="YES", help="Verification status")
    add_parser.add_argument("--checks", type=str, default="", help="Important checks & prevention rules")

    args = parser.parse_args()

    if args.subcommand == "init" or not args.subcommand:
        cmd_init()
    elif args.subcommand == "list":
        cmd_list()
    elif args.subcommand == "add":
        cmd_add(args)


if __name__ == "__main__":
    main()

