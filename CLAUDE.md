# Obsidian AI Knowledge Base

## What this is
AI-maintained personal knowledge base (Obsidian) following the **LLM Wiki** pattern. The vault is a persistent, compounding artifact — knowledge compiled once and kept current, not re-derived per query.

- **User**: a researcher / knowledge worker. Customize this line for your domain.
- **Claude**: owns the wiki layer — summarizing, cross-referencing, filing, maintaining consistency.
- **Three layers**: (1) Raw sources — immutable, read but never modify. (2) The wiki — LLM-generated/maintained markdown Claude owns. (3) The schema — this file, co-evolved.

## Vault location
- The vault mounts at `/workspace/ObsidianVault/` inside the devcontainer. The host source can be iCloud, Obsidian Sync, Dropbox, or a local directory — see README for setup.

## Git (local-only safety net)
- Commit at session end; commit every ~10 modifications during batch sessions.
- `.gitignore` excludes PDFs, images, binaries, `90_Archive/Roam_Daily/`, Obsidian workspace files.
- Don't amend — new commits only.
- Recovery: `git log --oneline -- <path>` → `git checkout <commit> -- <path>`.

## Vault structure
```
ObsidianVault/
  !TASKS/TASKS.md      # Persistent tasks — single source of truth
  index.md             # Master content catalog
  log.md               # Append-only activity log
  !NEW-ARRIVALS.md     # User-facing feed of recent output
  _Templates/          # Note templates — don't edit without asking
  00_Inbox/            # Unprocessed items (Papers/queue.md, claude-backlog.md)
  01_Research/         # Raw/ (immutable) · Papers/ · Concepts/ · Projects/ · Summaries/
  02_Admin/            # Meetings/ · Grants/
  03_Personal/         # Home/ Family/ Planning/
  04_Daily/            # YYYY-MM-DD.md — primary view
  90_Archive/
```

## Conventions

### Tasks (single source of truth)
- `!TASKS/TASKS.md` is the ONLY place persistent tasks live. **Never duplicate.**
- Daily notes reference tasks via block embeds `![[TASKS#^ev-YYMMDD-slug]]` — never copies.
- User-written plain checkboxes in daily notes get migrated to TASKS.md with `^todo-YYMMDD-slug` IDs on next sync.

### Language
Mixed JP/EN. Section headings use both (`## 定義 / Definition`). Research is typically English; personal often Japanese. Respond in the user's language.

### File naming & frontmatter
- Daily: `YYYY-MM-DD.md`. Papers: English title. Concepts: short phrase. No spaces — hyphens or natural casing (e.g., `C3-vs-C4.md`).
- Every note has YAML frontmatter: `date`, `type` (`daily|paper|concept|meeting|project|note`), `tags`.

### Links & templates
`[[wikilinks]]` generously; check for existing notes to link to. `_Templates/` has Daily/Paper/Concept/Meeting/Project templates + Templater Review-Marker-Picker (user invokes via `Cmd+Shift+R`). Use template structure when creating notes.

## Evidence levels — confirmed / inferred / speculative

Every non-obvious factual claim in vault content must be marked so downstream sessions can tell primary-source facts from reasoned guesses. Applies to patent FTO, protocols, reagent choices, regulatory facts, and anything actionable.

| Level | Meaning | How to write it |
|---|---|---|
| **Confirmed** | Directly read from a primary source that's re-verifiable. | Quote verbatim + cite file path:line or DOI + fig/table. |
| **Inferred** | Reasoned from adjacent confirmed facts; not directly read. | "Inferred from X", "by analogy to Y". State the chain. |
| **Speculative** | Weak/incomplete reasoning. | "Speculative: ..." — hypothesis, not fact. |

### Hard rules
1. **Never collapse levels silently.** "Speculative" must not become "confirmed" downstream.
2. **Never infer assignee from a publication number.** Numbers carry zero ownership info — always open the applicant page before asserting ownership.
3. **Scan-only PDFs need real OCR before claim inference.** Flag `unverified`; don't write a confident paper note on an image-only PDF.
4. **`unverified` is a hard blocker.** Downstream decisions wait for verification — don't route around it.
5. **Background-agent outputs are speculative by default.** Main session verifies before folding findings into load-bearing documents.
6. **Cite with enough precision to re-verify.** File path + line number (OCR) or DOI + figure/table (literature). "Based on the Huang paper" is not enough.

### Marking conventions
- Paper/concept pages: inline `**Confirmed:**` / `**Inferred:**` / `**Speculative:**` on non-trivial claims, or grouped subsections (`### Confirmed facts` / `### Inferred` / `### Speculative`).
- Patent FTO tables: annotate claim language as `verbatim` / `family-inferred` / `speculative`.
- Blockers in daily notes: `BLOCKER: need verbatim claim 1 of WO...` so closure is explicit.
- Frontmatter `unverified: true` stays until claims are read verbatim.

### Patent FTO — assignee search FIRST
Before writing any FTO analysis or invention-disclosure claim set, run an assignee search on every company in the target space:
- WIPO Patentscope: `FP:(CompanyName)` simple search; filter Country=WO; sort by date desc.
- Google Patents backup: `assignee:"CompanyName"` with date range.
~5 min; catches both hallucinated phantom threats and real threats missing from the vault. Do this at the **start**, not the end.

**Why this rule exists**: Patent publication numbers carry zero ownership info. A background agent that infers an assignee from a numbering range or filename will silently fabricate threats (or miss real ones). Always open the applicant page first; build narrative second.

## Navigation files

- **`log.md`** — append-only. Format: `## [YYYY-MM-DD] action | Title` + description + links. Actions: `ingest|query|enrich|lint|sweep|reorganize|migrate`. Append after any non-trivial vault operation.
- **`index.md`** — master catalog of every substantive wiki page with one-line summaries, by category (Papers / Concepts / Projects / Summaries & Hubs). Read first for queries. Update on create/move/archive. Entries ≤150 chars.
- **`!NEW-ARRIVALS.md`** — user-facing feed grouped by date: Research Questions / Concept Pages / Paper Notes / Hub Pages / Papers Queued. Append when creating new content; trim entries >30 days old.

## Core operations

### Ingest (a single source may touch 10-15 pages)
1. Template + frontmatter + correct folder.
2. `[[wikilinks]]` to related notes; update concept/entity pages — **integrate the knowledge, don't just file it**.
3. Update `index.md`, `!NEW-ARRIVALS.md`, `log.md` (`ingest`).

### Query
Read `index.md` first. When a conversation produces a valuable synthesis (cross-paper comparison, methodology analysis, gap), file it as a concept page/summary/section and update navigation files. Not every answer warrants a page — use judgment.

### Lint
Health checks: contradictions, orphan notes, broken `[[wikilinks]]`, missing pages, missing cross-refs, frontmatter gaps, unprocessed inbox, consolidatable tags, data gaps, review markers. Append `lint` to `log.md`.

### Sweep (review markers)
Grep `%%FLAG:|%%WEAK|%%EXPAND|%%MERGE:|%%CUT`. Actions:
- `FLAG: comment` — re-evaluate per comment.
- `WEAK` — rework with stronger sources or remove.
- `EXPAND` — flesh out with detail + citations.
- `MERGE: [[Target]]` — combine into target, remove duplicate.
- `CUT` — remove.
Remove marker after processing. Append `sweep` to `log.md`.

## Paper Queue (discovery → PDF → vault)

- **Queue**: `ObsidianVault/00_Inbox/Papers/queue.md` — want-list with DOI/URL, journal, year, one-line "Why".
- **Drop folder**: `/workspace/drop/` (read-only mount of a host drop directory). User drops PDFs, screenshots, instructions. **Never delete/move/write in drop/** — copy to `/workspace/` first if editing.
- **Processed tracking**: append filenames to `.claude/hooks/papers-processed.txt`.

### Workflow
1. Discovery: web search surfaces inaccessible paper → append to `queue.md`.
2. User drops PDF in Finder.
3. Read PDF from `/workspace/drop/`, create paper note in `01_Research/Papers/`, update concept/hub/nav files, check off in `queue.md`.

### Verification (web searches hallucinate)
1. Verify DOI resolves to expected title/journal.
2. Cross-check title, authors, journal, year for consistency.
3. If unverifiable, add `unverified: true` + note what failed.
4. Never invent DOIs — leave blank.

## PDF & enrichment tooling

Devcontainer has: `pdftotext`/`pdfinfo` (poppler-utils), `pymupdf` (fitz), `pdfplumber`, `habanero` (CrossRef).

### `scripts/enrich_papers.py`
```
python3 scripts/enrich_papers.py audit
python3 scripts/enrich_papers.py pdf-extract /workspace/drop
python3 scripts/enrich_papers.py crossref
python3 scripts/enrich_papers.py enrich [--dry-run]
```

Batch flow: `pdf-extract` → identify new papers → create notes → `crossref` + `enrich` → update concept/hub pages.

### Roam cleanup script (`scripts/clean_roam.py`)
Converts `{{[[TODO]]}}`→`[ ]`, `{{[[DONE]]}}`→`[x]`, `[[Month Dth, YYYY]]`→`[[YYYY-MM-DD]]`, strips `((block refs))`. Run on any newly imported Roam markdown before it enters the vault: `python3 scripts/clean_roam.py [--apply] [path]`.

## Devcontainer & web fetching

Firewall whitelists only: pypi.org, api.crossref.org, doi.org, github raw, MCP backends. Publisher sites (wiley, mdpi, biomedcentral, pmc.ncbi.nlm.nih.gov, etc.) hang silently for 60s on `WebFetch`. **Four timeouts in a row is the failure mode to avoid.**

**Habits:**
1. **Never `WebFetch` publisher sites.** Use an MCP first:
   - Papers: `mcp__papers__*`, `mcp__biorxiv__*`, `mcp__latest-science__*`
   - PubMed/PMC: `mcp__pubmed__*`
   - DOI metadata: `habanero` via `enrich_papers.py crossref`
2. **Arbitrary URLs**: `curl -sSL --connect-timeout 3 --max-time 5 <url>`. Bail on first failure.
3. **`WebFetch` is fine for whitelisted hosts** (doi.org, crossref, pypi, github raw).
4. **Log dead URLs to the paper queue** (`unverified: true`) rather than retrying.
5. **Don't casually propose whitelist changes** — only after repeated cross-session blocks.

## Research question generation

After processing new papers, enrichment, or discovery searches, generate cross-cutting questions.
1. Read hub + concept pages for landscape.
2. Look for cross-domain connections, unexplored intersections, repurposable methods, contradictions, gaps.
3. Cite `[[wikilinks]]` to inspiring notes; categorize by actionability.
4. Save to `01_Research/Summaries/Research-Questions-YYYY-MM.md`.
5. Present top 3-5 to user; flag those testable with the user's available methods/instruments.

Trigger: after batch processing, enrichment, discovery, user requests, or proactively when changes touch the user's core research themes (customize this list for your domain).

## Hooks (`.claude/settings.json`, scripts in `.claude/hooks/`)

**IMPORTANT: Always prompt the user on every SessionStart hook result before doing anything else.** Explicitly ask what to do with each surfaced item.

### SessionStart
- `check-papers-drop.sh` — unprocessed PDFs in `/workspace/drop/`
- `check-inbox.sh` — unprocessed items in `00_Inbox/` (excl. `queue.md`, `claude-backlog.md`)
- `check-review-markers.sh` — `%%FLAG%%`/`%%WEAK%%`/`%%EXPAND%%`/`%%MERGE%%`/`%%CUT%%`
- `check-new-arrivals-age.sh` — `!NEW-ARRIVALS.md` sections >30 days
- `check-backlog.sh` — open items in `00_Inbox/claude-backlog.md`
- `check-vault-sync-drafts.sh` — `[vault-sync]` Gmail drafts
- `sync-gcal.sh` — Google Calendar → vault sync

### PreToolUse (Edit|Write)
- `guard-vault-safety.sh` — blocks edits to `_Templates/` and `01_Research/Raw/`.

### PostToolUse (Edit|Write)
- `check-wikilinks.sh` — verifies `[[wikilinks]]` resolve after vault edits.

## Google Calendar → Vault sync

**Philosophy**: GCal = source of truth for timed events. `!TASKS/TASKS.md` = daily action list (iPhone driver). Events flow into TASKS.md so user lives in Obsidian on iPhone. Important events → GCal; small daily todos → Obsidian daily note. Claude migrates everything to TASKS.md with block IDs and replaces originals with embeds. **User never types block IDs or embed syntax.**

### Sync procedure (sync-gcal.sh fires on SessionStart)
1. Read GCal events for next 14 days (user's local timezone) AND `!TASKS/TASKS.md` for manually-added dated events. Both feed the daily note.
2. Add near-term events to TASKS.md: this week → `## 今週 / This Week`; this month → `## 今月 / This Month`. Every dated event line needs a `^ev-YYMMDD-slug` block ID. Reuse existing IDs.
3. Update today's daily note:
   - Today's events → `## スケジュール / Schedule` with independent checkboxes + times (`- [ ] **15:00-16:00** Meeting`) — "did I attend" trackers.
   - Upcoming (14d) → `### 今後の予定 / Upcoming` as block embeds `![[TASKS#^ev-YYMMDD-slug]]`, one per line, no bullet prefix.
4. **Migrate user-written todos**: plain checkbox lines (not embeds) → add to TASKS.md as `^todo-YYMMDD-slug` (daily note's date) → replace line with embed.
5. **Scan メモ / Notes section for dated commitments → offer GCal event**. For memo lines with time-bound commitments (e.g. "tomorrow", "next Wednesday", "Saturday at 3pm"), ask user first. After confirmation:
   - Create GCal event via `mcp__claude_ai_Google_Calendar__gcal_create_event` (user's local timezone).
   - Add `^ev-YYMMDD-slug` to TASKS.md; replace memo with embed under `今後の予定` (or `スケジュール` if today).
   - **Resolve relative dates against the daily note's date, not today's** — the memo may be old.
   - Ask for missing duration/location; never invent times.
   - Skip pure thoughts/reflections.
6. Don't duplicate events already listed.
7. Ask the user before syncing (per hook rule).

### Block ID conventions
- Calendar events: `^ev-YYMMDD-slug` (event date). Daily todos: `^todo-YYMMDD-slug` (daily note's date).
- `slug`: 1-3 word lowercase ASCII with hyphens. Romanize non-Latin scripts as needed.
- Multi-day events: start date (e.g. a 4/22-24 event → `^ev-260422-conference`).
- YYMMDD+slug must be unique in TASKS.md. Block IDs never change once assigned — embeds stay valid even if the task moves sections or gets checked off.
- Embed syntax: `![[TASKS#^ev-YYMMDD-slug]]` — no bullet prefix, one per line.
- Only dated events and user-written todos get block IDs; thoughts/notes stay plain text.

## Weekly carryover

Scan last 7 daily notes and surface still-open tasks into today's.

1. **Scan embeds** (`![[TASKS#^todo-...]]`, `![[TASKS#^ev-...]]`). For each, check TASKS.md — if still `- [ ]` and not in today's note, it's a carryover candidate.
2. **Scan plain checkboxes** (non-embed). Persistent unchecked items: add to TASKS.md with `^todo-YYMMDD-slug` (ORIGINAL daily note's date); replace plain line with embed so history stays linked.
3. **Surface in today's note** under `**持ち越し / Carried over (last week, still open)**` inside each category (研究/事務/生活/開発), grouped by task semantics.
4. **Skip stale items**: past weekend chores, one-off thoughts, non-actionable musings. When unsure, include and let user prune.
5. **Don't duplicate** items already embedded from direct GCal/TASKS sync.
6. **Confirm load-bearing tasks**: if user names a specific task, verify its block ID appears in today's note before reporting.

Trigger: user says "carry over" / "pick up what I haven't done" / names a specific task; first SessionStart each Monday (ask first — noisy); after >3-day gaps.

**Why**: Tasks added to TASKS.md that never get re-embedded drop off the user's radar. The daily note is the primary view — if an item isn't there, it effectively doesn't exist for that day.

## Recurring habits

Hard-coded recurring rules go here so Claude inserts them into daily notes automatically. Examples (replace with your own):
- **(weekend)** Call parents / weekly review / batch errands — add to 生活/Home + Schedule
- **(Monday)** Weekly planning sweep — add to 事務/Admin

Format: create a fresh TASKS.md line under 今週 with a stable block ID (e.g. `^todo-YYMMDD-call-parents` dated to the relevant day), then embed it in the appropriate daily note(s). Check off or roll forward after the period.

**Why**: recurring obligations that aren't on GCal silently miss the daily note otherwise. Encoding them here makes them automatic.

## Gmail sync (vault-sync drafts)

Remote agents (https://claude.ai/code/scheduled) run 3x daily and create Gmail drafts with `[vault-sync]` subject. On SessionStart, Claude processes them.

**Agents**: `vault-sync-morning` (full daily summary) · `vault-sync-noon` (midday refresh) · `vault-sync-afternoon` (afternoon refresh + tomorrow preview).

**Processing** (check-vault-sync-drafts.sh):
1. Search drafts with `[vault-sync]` subject.
2. Parse structured markdown (tasks / schedule / Gmail summary).
3. Update today's `04_Daily/YYYY-MM-DD.md`.
4. Add actionable items to `!TASKS/TASKS.md`.
5. Delete the processed draft.

**Task horizons** in TASKS.md: **今週** (active) · **今月** (upcoming) · **いつか** (no deadline) · **完了** (move completed — don't delete). Daily notes link via `[[tasks]]` and embed relevant items.

## Email drafting (example: vendor / admin / cold outreach)

*This section is an example of how to encode email-style preferences. Replace with your own conventions or delete if irrelevant.*

Default to a **minimalist 3-question shape** in both JP and EN. User consistently edits drafts to this form — start there rather than draft-then-trim.

### Rules
1. **Skip non-informative openers.** JP: no 「お世話になっております」 for cold outreach. EN: no "I initially looked at your site" preamble. Straight to self-intro + ask.
2. **3 questions maximum**, combining items: (1) availability + local distributor, (2) price + shipping, (3) lead time. Drop COA / shipping conditions / payment terms / customs — reliable vendors include these anyway; checklists read as demanding (especially JP B2B).
3. **No usage-context section.** Delete 「■ 用途（ご参考まで）」 / "For context, this reagent will be used for...".
4. **One-sentence self-intro.** JP: 「<your one-sentence self-intro in your own language>」 EN: "<your one-sentence self-intro>".
5. **Soft closers**, not heavy.
   - JP: 「ご教示いただけますでしょうか」 > 「〜と幸いです」. Drop 「ご確認のほど」. 「どうぞよろしくお願い申し上げます」 alone closes.
   - EN: "Thank you very much for your time. I look forward to your reply."
6. **Correct title**: use your correct institutional title in your signature.
7. **Signature** uses your institutional email even when drafting from a personal account (user may copy to institutional webmail before sending).

### Skeleton
Addressee → 1-sentence self-intro → 1-sentence ask → product block (製品名 + カタログ番号 inline) → 3 numbered questions → thank-you close → signature. No 用途, no 6-item matrix.

**Why**: vendors respond faster to short, specific requests; checklists slow replies. Apply by default; expand only if the user explicitly asks ("ask about COA").

## User backlog
`ObsidianVault/00_Inbox/claude-backlog.md` — user-maintained improvements list. Check at session start.

## Important notes
- Never delete user content without asking.
- Explain what you're moving and why when reorganizing.
- Keep the vault lightweight — no large binaries.
- Avoid rapid bulk writes (sync conflicts on iCloud / Obsidian Sync / Dropbox).
