# Obsidian Vault — Claude Code Instructions

This is an AI-maintained Obsidian knowledge base. The companion file at the workspace root (`/workspace/CLAUDE.md`) contains the full schema; this file is the vault-local brief.

## Quick reference
- **Language**: customize for your workflow (this template was authored in mixed JP/EN — adapt as needed)
- **New files**: Use templates from `_Templates/`, add YAML frontmatter, use `[[wikilinks]]`
- **Inbox**: `00_Inbox/` is the triage queue — process items into correct folders
- **Never delete** user content without confirmation
- **Daily notes**: `04_Daily/YYYY-MM-DD.md`
- **Respond** in the language the user uses
- **Git commits**: Commit at session end, and every ~10 vault modifications during long sessions
- **Daily note schedule**: Today's events → `## スケジュール / Schedule` section (independent checkboxes). Upcoming events → block embeds `![[TASKS#^ev-YYMMDD-slug]]` referencing `!TASKS/TASKS.md`. Every dated event in TASKS.md must have a `^ev-YYMMDD-slug` block ID. User-written daily todos get migrated to TASKS.md with `^todo-YYMMDD-slug` IDs on next sync.

## Research domain (CUSTOMIZE)

Replace this section with your own research themes / project areas. Example structure:

> The vault owner is a [field] researcher. The major themes are:
> 1. **Theme A** — short description. Hub: [[Theme-A-Hub]]
> 2. **Theme B** — short description. Hub: [[Theme-B-Hub]]
> 3. **Theme C** — short description. Hub: [[Theme-C-Hub]]
>
> These hubs in `01_Research/Summaries/` are the best starting points for navigating related pages.

Hub pages live in `01_Research/Summaries/` and serve as navigation entry points for each theme. When you create or update content that fits a theme, update the relevant hub.

## Content characteristics

- **Paper notes** are the user's reading notes and observations, not summaries. Preserve the personal voice.
- **Concept pages** accumulate dated sections (`## Notes from YYYY-MM-DD`) extracted from daily notes. When adding new content from daily notes, append as a new dated section rather than merging into existing text.
- **Project pages** contain plans, methodology decisions, and working state. These are working documents.
- **Meeting pages** are presentation prep or seminar discussion notes.
- **Technical language**: Domain-specific terminology (e.g., field-specific English embedded in another language) should be preserved verbatim — do not translate.

## Link conventions

- Every research page should have a `## Related Pages` section at the bottom with categorized links:
  ```
  ## Related Pages
  **Concepts:** [[page1]], [[page2]]
  **Projects:** [[page3]]
  **Papers:** [[page4]]
  ```
- When creating or editing a page, check whether new `[[wikilinks]]` should be added to connect it to existing pages. Also add a back-link on the target page.
- Hub pages in `01_Research/Summaries/` should be updated when new pages are created that fit a theme.

## Processing PDFs from drop/

Files (papers, screenshots, etc.) are dropped into `~/Desktop/ClaudeDropbox/`, mounted read-only at `/workspace/drop/`.

### When asked to process papers

1. **List** the PDFs in `drop/` (may include subdirectories)
2. **Read** each PDF using the Read tool (up to 20 pages per request; for longer papers, read in chunks: pages 1-15, then 16-30, etc.)
3. **Extract metadata** from the paper:
   - Title, authors, journal, year, DOI
   - Identify which research theme(s) it relates to
4. **Create a paper note** in `01_Research/Papers/` using the template structure from `_Templates/Research Paper.md`:
   - Filename: paper title in English, hyphens for spaces (e.g., `Smith-et-al-2024-topic.md`)
   - Fill in frontmatter: date, type: paper, title, authors, journal, year, doi, tags, status: unread
   - Fill in `## 概要 / Summary` with a concise summary (3-5 sentences)
   - Fill in `## Key Findings` with the main results (bullet points)
   - Fill in `## Methods` with notable techniques
   - Leave `## 関連性 / Relevance to My Work` and `## 疑問点 / Questions` empty — these are for the user's own observations
   - Fill in `## Related` with `[[wikilinks]]` to existing vault pages
5. **Add a `## Related Pages` section** at the bottom linking to relevant concepts, projects, and other papers
6. **Add back-links**: update Related Pages sections on connected vault pages to include the new paper
7. **Update hub pages** in `01_Research/Summaries/` if the paper fits a theme
8. **Report** to the user: for each paper, show the title, where it was filed, and which existing pages it connects to

### Tips
- For non-English papers, keep the note bilingual (original-language title + English section headings)
- If the paper directly relates to an existing concept/project, mention this prominently
- Papers already processed (check `01_Research/Papers/` filenames) should be skipped
- Do NOT modify or delete files in `drop/` (read-only mount). Copy to `/workspace/` first if editing is needed.
