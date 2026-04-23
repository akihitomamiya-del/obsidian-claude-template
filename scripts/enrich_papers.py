#!/usr/bin/env python3
"""
Batch paper metadata enrichment for Obsidian vault.

Workflows:
  1. pdf-extract   — Extract metadata (DOI, title, authors, journal, year) from PDFs using PyMuPDF
  2. crossref      — Look up missing metadata via CrossRef API using DOI or title
  3. audit         — Report gaps in paper note frontmatter
  4. enrich        — Fill missing frontmatter fields from CrossRef data

Usage:
  python3 scripts/enrich_papers.py audit
  python3 scripts/enrich_papers.py pdf-extract /workspace/drop
  python3 scripts/enrich_papers.py crossref
  python3 scripts/enrich_papers.py enrich [--dry-run]
"""

import os
import re
import json
import sys
from pathlib import Path

VAULT_PAPERS = Path("/workspace/ObsidianVault/01_Research/Papers")
MANIFEST_FILE = Path("/workspace/papers_manifest.json")


def parse_frontmatter(filepath: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        m = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if m:
            key, val = m.group(1), m.group(2)
            if val in ("", "[]"):
                fm[key] = ""
            else:
                fm[key] = val
    return fm


def audit():
    """Report metadata gaps across all paper notes."""
    papers = sorted(VAULT_PAPERS.glob("*.md"))
    fields = ["title", "authors", "journal", "year", "doi"]
    gaps = {f: [] for f in fields}
    total = 0

    for p in papers:
        total += 1
        fm = parse_frontmatter(p)
        for f in fields:
            val = fm.get(f, "")
            if not val or val in ("Not available in metadata", "Unknown"):
                gaps[f].append(p.stem)

    print(f"\n{'='*60}")
    print(f"PAPER METADATA AUDIT — {total} papers")
    print(f"{'='*60}\n")

    for f in fields:
        missing = gaps[f]
        pct = (total - len(missing)) / total * 100
        print(f"  {f:10s}: {total - len(missing):3d}/{total} ({pct:.0f}%) complete")
        if missing:
            for name in missing[:5]:
                print(f"             - {name}")
            if len(missing) > 5:
                print(f"             ... and {len(missing) - 5} more")
    print()

    # Papers with 3+ gaps
    multi_gap = []
    for p in papers:
        fm = parse_frontmatter(p)
        gap_count = sum(1 for f in fields if not fm.get(f, "") or fm.get(f, "") in ("Not available in metadata", "Unknown"))
        if gap_count >= 3:
            multi_gap.append((p.stem, gap_count))

    if multi_gap:
        print(f"Papers with 3+ missing fields ({len(multi_gap)}):")
        for name, count in sorted(multi_gap, key=lambda x: -x[1]):
            print(f"  [{count} gaps] {name}")
    print()


def pdf_extract(input_dir: str):
    """Extract metadata from PDFs using PyMuPDF and write manifest."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("ERROR: PyMuPDF not installed. Run: pip3 install pymupdf")
        sys.exit(1)

    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"ERROR: {input_dir} does not exist")
        sys.exit(1)

    pdfs = sorted(input_path.rglob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs in {input_dir}")

    # Skip common non-paper PDF file patterns (supplementary materials,
    # author instructions, publishing agreements, etc.). Add your own
    # domain-specific filename patterns here if you want to skip certain
    # PDFs automatically (e.g. specific journals or reagent datasheets).
    skip_re = re.compile(r"(^mmc\d|MOESM|_ESM|SUPPLEMENTARY|Author_Instruct|AUTHOR.AGREE|_sm\.|_checklist)", re.IGNORECASE)

    manifest = []
    for pdf in pdfs:
        if skip_re.search(pdf.name):
            continue

        entry = {"file": str(pdf), "title": "", "authors": "", "journal": "", "year": "", "doi": ""}

        try:
            doc = fitz.open(str(pdf))
            meta = doc.metadata or {}
            entry["title"] = (meta.get("title") or "").strip()
            entry["authors"] = (meta.get("author") or "").strip()

            # XMP metadata
            xmp = doc.get_xml_metadata() or ""
            if xmp:
                for tag, key in [
                    ("prism:doi", "doi"),
                    ("prism:publicationName", "journal"),
                ]:
                    m = re.search(f"<{tag}>(.*?)</{tag}>", xmp)
                    if m:
                        entry[key] = m.group(1).strip()

                # Title from XMP
                tm = re.search(r"<dc:title>.*?<rdf:li[^>]*>(.*?)</rdf:li>", xmp, re.DOTALL)
                if tm and tm.group(1).strip():
                    entry["title"] = tm.group(1).strip()

                # Year
                dm = re.search(r"<prism:coverDate>(.*?)</prism:coverDate>", xmp)
                if dm:
                    ym = re.search(r"(\d{4})", dm.group(1))
                    if ym:
                        entry["year"] = ym.group(1)

            # DOI from text if not in XMP
            if not entry["doi"]:
                text = ""
                for i in range(min(2, len(doc))):
                    text += doc[i].get_text()
                doi_m = re.search(r"(10\.\d{4,}/[^\s\]>)]+)", text)
                if doi_m:
                    entry["doi"] = doi_m.group(1).rstrip(".,;")

            doc.close()
        except Exception as e:
            entry["error"] = str(e)

        manifest.append(entry)
        print(f"  {pdf.name}: doi={entry['doi'] or '?'}, title={entry['title'][:50] or '?'}")

    MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"\nManifest: {MANIFEST_FILE} ({len(manifest)} entries)")
    print(f"  With DOI: {sum(1 for e in manifest if e['doi'])}")
    print(f"  With title: {sum(1 for e in manifest if e['title'])}")


def crossref_lookup(query: str, is_doi: bool = False) -> dict:
    """Look up metadata via CrossRef."""
    try:
        from habanero import Crossref
    except ImportError:
        print("ERROR: habanero not installed. Run: pip3 install habanero")
        sys.exit(1)

    cr = Crossref(mailto="obsidian-vault-enrichment@example.com")

    try:
        if is_doi:
            result = cr.works(ids=query)
            item = result["message"]
        else:
            result = cr.works(query=query, limit=1)
            items = result["message"]["items"]
            if not items:
                return {}
            item = items[0]

        data = {}
        if "title" in item and item["title"]:
            data["title"] = item["title"][0]
        if "author" in item:
            names = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in item["author"]]
            data["authors"] = ", ".join(n for n in names if n)
        if "container-title" in item and item["container-title"]:
            data["journal"] = item["container-title"][0]
        if "DOI" in item:
            data["doi"] = item["DOI"]
        for date_key in ("published-print", "published-online", "published"):
            if date_key in item:
                parts = item[date_key].get("date-parts", [[]])[0]
                if parts:
                    data["year"] = str(parts[0])
                    break
        return data
    except Exception as e:
        return {"error": str(e)}


def crossref_batch():
    """Look up missing metadata for all papers via CrossRef."""
    papers = sorted(VAULT_PAPERS.glob("*.md"))
    results = {}

    for p in papers:
        fm = parse_frontmatter(p)
        missing = [f for f in ["authors", "journal", "year", "doi"]
                   if not fm.get(f, "") or fm.get(f, "") in ("Not available in metadata", "Unknown")]

        if not missing:
            continue

        print(f"\n{p.stem} — missing: {', '.join(missing)}")

        # Try DOI first, then title
        doi = fm.get("doi", "")
        title = fm.get("title", "") or p.stem.replace("-", " ")

        if doi:
            print(f"  Looking up DOI: {doi}")
            data = crossref_lookup(doi, is_doi=True)
        else:
            print(f"  Searching by title: {title[:60]}...")
            data = crossref_lookup(title, is_doi=False)

        if "error" in data:
            print(f"  ERROR: {data['error']}")
            continue

        if data:
            results[p.stem] = {"current": fm, "crossref": data, "missing": missing}
            for k, v in data.items():
                if k in missing:
                    print(f"  Found {k}: {v[:60] if isinstance(v, str) else v}")
        else:
            print(f"  No results found")

    out = Path("/workspace/crossref_results.json")
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n\nResults saved to {out} ({len(results)} papers enriched)")


def enrich(dry_run: bool = False):
    """Apply CrossRef results to paper notes."""
    results_file = Path("/workspace/crossref_results.json")
    if not results_file.exists():
        print("ERROR: Run 'crossref' first to generate crossref_results.json")
        sys.exit(1)

    results = json.loads(results_file.read_text())
    updated = 0

    for stem, data in results.items():
        filepath = VAULT_PAPERS / f"{stem}.md"
        if not filepath.exists():
            continue

        text = filepath.read_text(encoding="utf-8")
        cr = data["crossref"]
        changes = []

        for field in ["authors", "journal", "year", "doi"]:
            if field in data["missing"] and field in cr and cr[field]:
                # Replace empty field in frontmatter
                old_patterns = [
                    f'{field}: ""',
                    f'{field}: "Not available in metadata"',
                    f'{field}: "Unknown"',
                    f'{field}: ',
                ]
                new_val = f'{field}: "{cr[field]}"'
                for pat in old_patterns:
                    if pat in text:
                        text = text.replace(pat, new_val, 1)
                        changes.append(f"{field} → {cr[field][:40]}")
                        break

        if changes:
            if dry_run:
                print(f"  [DRY RUN] {stem}: {', '.join(changes)}")
            else:
                filepath.write_text(text, encoding="utf-8")
                print(f"  Updated {stem}: {', '.join(changes)}")
            updated += 1

    print(f"\n{'Would update' if dry_run else 'Updated'} {updated} papers")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "audit":
        audit()
    elif cmd == "pdf-extract":
        if len(sys.argv) < 3:
            print("Usage: python3 enrich_papers.py pdf-extract /path/to/pdfs")
            sys.exit(1)
        pdf_extract(sys.argv[2])
    elif cmd == "crossref":
        crossref_batch()
    elif cmd == "enrich":
        dry_run = "--dry-run" in sys.argv
        enrich(dry_run)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
