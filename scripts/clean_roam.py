#!/usr/bin/env python3
"""Clean Roam Research syntax from Obsidian vault markdown files.

Transformations:
  1. {{[[TODO]]}}  → [ ]       (Obsidian checkbox, unchecked)
  2. {{[[DONE]]}}  → [x]       (Obsidian checkbox, checked)
  3. [[Month Dth, YYYY]] → [[YYYY-MM-DD]]  (Roam date links → ISO wikilinks)
  4. ((block refs))  → strip parens, keep text

Usage:
  python3 scripts/clean_roam.py [path]          # dry-run (default)
  python3 scripts/clean_roam.py [path] --apply  # apply changes

If path is omitted, defaults to /workspace/ObsidianVault.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}

# Patterns
TODO_RE = re.compile(r'\{\{\[\[TODO\]\]\}\}')
DONE_RE = re.compile(r'\{\{\[\[DONE\]\]\}\}')
ROAM_DATE_RE = re.compile(
    r'\[\[('
    + '|'.join(MONTH_MAP.keys())
    + r')\s+(\d{1,2})(?:st|nd|rd|th),\s+(\d{4})\]\]'
)
BLOCK_REF_RE = re.compile(r'\(\(([^)]+)\)\)')


def roam_date_to_iso(match: re.Match) -> str:
    month_name, day, year = match.group(1), int(match.group(2)), int(match.group(3))
    month = MONTH_MAP[month_name]
    try:
        d = datetime(year, month, day)
        return f'[[{d.strftime("%Y-%m-%d")}]]'
    except ValueError:
        return match.group(0)  # invalid date, leave as-is


def clean_content(text: str) -> str:
    text = TODO_RE.sub('[ ]', text)
    text = DONE_RE.sub('[x]', text)
    text = ROAM_DATE_RE.sub(roam_date_to_iso, text)
    text = BLOCK_REF_RE.sub(r'\1', text)
    return text


def main():
    parser = argparse.ArgumentParser(description="Clean Roam syntax from markdown files")
    parser.add_argument('path', nargs='?', default='/workspace/ObsidianVault',
                        help='Vault directory to process')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default is dry-run)')
    args = parser.parse_args()

    vault = Path(args.path)
    if not vault.is_dir():
        print(f"Error: {vault} is not a directory", file=sys.stderr)
        sys.exit(1)

    stats = {"files_changed": 0, "todo": 0, "done": 0, "dates": 0, "block_refs": 0}

    for md in sorted(vault.rglob('*.md')):
        original = md.read_text(encoding='utf-8')
        cleaned = original

        n_todo = len(TODO_RE.findall(cleaned))
        cleaned = TODO_RE.sub('[ ]', cleaned)

        n_done = len(DONE_RE.findall(cleaned))
        cleaned = DONE_RE.sub('[x]', cleaned)

        n_dates = len(ROAM_DATE_RE.findall(cleaned))
        cleaned = ROAM_DATE_RE.sub(roam_date_to_iso, cleaned)

        n_refs = len(BLOCK_REF_RE.findall(cleaned))
        cleaned = BLOCK_REF_RE.sub(r'\\1', cleaned)

        if cleaned != original:
            stats["files_changed"] += 1
            stats["todo"] += n_todo
            stats["done"] += n_done
            stats["dates"] += n_dates
            stats["block_refs"] += n_refs

            rel = md.relative_to(vault)
            changes = []
            if n_todo: changes.append(f"{n_todo} TODO")
            if n_done: changes.append(f"{n_done} DONE")
            if n_dates: changes.append(f"{n_dates} dates")
            if n_refs: changes.append(f"{n_refs} block-refs")
            print(f"  {'WRITE' if args.apply else 'WOULD'} {rel}  ({', '.join(changes)})")

            if args.apply:
                md.write_text(cleaned, encoding='utf-8')

    mode = "Applied" if args.apply else "Dry-run"
    print(f"\n{mode}: {stats['files_changed']} files | "
          f"{stats['todo']} TODO → [ ], {stats['done']} DONE → [x], "
          f"{stats['dates']} date links → ISO, {stats['block_refs']} block refs stripped")


if __name__ == '__main__':
    main()
