# Paper Processing Scripts

## Quick Start

```bash
# 1. See what's missing in your paper notes
python3 scripts/enrich_papers.py audit

# 2. Extract metadata from PDFs
python3 scripts/enrich_papers.py pdf-extract /workspace/drop

# 3. Fill gaps from CrossRef API
python3 scripts/enrich_papers.py crossref

# 4. Preview and apply fixes
python3 scripts/enrich_papers.py enrich --dry-run
python3 scripts/enrich_papers.py enrich
```

## Commands

### `audit`
Scans all `.md` files in `01_Research/Papers/` and reports missing frontmatter fields (title, authors, journal, year, doi). Lists papers with 3+ gaps as priority targets.

### `pdf-extract <path>`
Walks a directory of PDFs, skips supplements (mmc*, MOESM*, etc.), and extracts metadata using PyMuPDF:
- DOI from XMP metadata or text
- Title, authors, journal, year from XMP and PDF metadata
- Outputs `papers_manifest.json` for downstream use

### `crossref`
For each paper note with missing fields, queries the CrossRef API:
- Uses DOI if available (exact match)
- Falls back to title search
- Saves results to `crossref_results.json`

### `enrich [--dry-run]`
Reads `crossref_results.json` and patches paper note frontmatter. Use `--dry-run` to preview changes without writing.

## Adding New PDFs

When you drop a new batch of PDFs into `drop/`:

1. **Extract metadata**: `python3 scripts/enrich_papers.py pdf-extract /workspace/drop`
2. **Ask Claude** to read the manifest and create paper notes + update concept/hub pages
3. **Fill gaps**: `python3 scripts/enrich_papers.py crossref && python3 scripts/enrich_papers.py enrich`

## Requirements

Installed in devcontainer via Dockerfile:
- `poppler-utils` — pdftotext, pdfinfo
- `pymupdf` — Python PDF parsing
- `pdfplumber` — structured text extraction
- `habanero` — CrossRef API client

Firewall whitelists: `pypi.org`, `files.pythonhosted.org`, `api.crossref.org`
