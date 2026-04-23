# obsidian-claude-template

A starter kit for running an AI-maintained Obsidian knowledge base, with Claude Code as the librarian.

## What this is

This repo is a template for an **AI-maintained personal knowledge base** built on Obsidian and [Claude Code](https://docs.claude.com/en/docs/claude-code). It follows the "LLM Wiki" pattern: the vault is a persistent, compounding artifact — knowledge compiled once and kept current, not re-derived from scratch every query.

There are three layers:

1. **Raw sources** — PDFs, screenshots, web clippings. Immutable; read but never modified.
2. **The wiki** — markdown notes Claude generates, links, and maintains for you.
3. **The schema** — `CLAUDE.md`, the system-layer document that teaches Claude how to file things, link them, mark evidence levels, and keep everything consistent. You and Claude co-evolve it.

The goal is a vault that gets *more useful* over time, not a chat log that you rake through later.

## What's in the box

```
obsidian-claude-template/
├── README.md
├── LICENSE                           # MIT
├── .gitignore                        # Tracks scaffolding, ignores user content
├── CLAUDE.md                         # System-layer schema (Claude reads this)
├── .mcp.json                         # MCP server config (paper search, etc.)
├── .devcontainer/                    # Docker dev environment
│   ├── devcontainer.json             # VS Code dev-container spec
│   ├── Dockerfile                    # Node + Python + poppler + entrez
│   └── init-firewall.sh              # Whitelist-only network egress
├── .claude/
│   ├── settings.json                 # Hook wiring + permissions
│   └── hooks/                        # SessionStart / PreToolUse / PostToolUse scripts
├── scripts/
│   ├── enrich_papers.py              # PDF → frontmatter via PyMuPDF + CrossRef
│   ├── clean_roam.py                 # Roam Research markdown cleanup
│   └── setup-local.sh                # git skip-worktree helper for personal edits
└── ObsidianVault/                    # Vault root (sync your content INTO this)
    ├── CLAUDE.md                     # Vault-local brief (shorter than the system one)
    ├── _Templates/                   # Daily, Paper, Concept, Project, Meeting, Weekly Review
    ├── !TASKS/TASKS.md               # Single source of truth for tasks
    ├── !NEW-ARRIVALS/NEW-ARRIVALS.md # User-facing feed of recent output
    ├── 00_Inbox/                     # Triage queue (Papers/queue.md, claude-backlog.md)
    ├── 01_Research/                  # Raw/, Papers/, Concepts/, Projects/, Summaries/
    ├── 02_Admin/                     # Meetings/, Grants/
    ├── 03_Personal/                  # Home/, Family/, Planning/
    ├── 04_Daily/                     # YYYY-MM-DD.md daily notes
    ├── 05_News/                      # Sanitized news article archive
    ├── 90_Archive/
    ├── index.md                      # Master content catalog
    └── log.md                        # Append-only activity log
```

## Prerequisites

- macOS, Linux, or Windows with WSL2
- **Docker Desktop** + **VS Code** with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (recommended — gets you a sandboxed Linux environment with everything wired up)
- *Or:* Node 20+ and Python 3.10+ on the host if you'd rather run outside the container
- [Obsidian](https://obsidian.md) (free)
- An Anthropic API key set as `ANTHROPIC_API_KEY` in your host shell environment
- *Optional:* iCloud Drive, [Obsidian Sync](https://obsidian.md/sync), or Dropbox if you want the vault to follow you across devices

## Quickstart

1. **Clone the repo:**

   ```bash
   git clone <repo-url> ~/obsidian-claude
   cd ~/obsidian-claude
   ```

2. **Decide how to populate `ObsidianVault/`** — see [Loading your vault](#loading-your-vault) below. You can defer this and use the empty scaffolding for a first pass.

3. **Open in VS Code → "Reopen in Container"** when prompted. The first build takes 2-3 minutes; subsequent starts are seconds.

4. **Open the integrated terminal and run Claude Code:**

   ```bash
   claude --dangerously-skip-permissions
   ```

   The `--dangerously-skip-permissions` flag is OK here because the dev container is already sandboxed by the firewall whitelist (see `.devcontainer/init-firewall.sh`).

5. **Try it out:**

   ```
   /init                                # introduce yourself; Claude scans the repo
   say hi
   take a look at ObsidianVault/ and tell me what's there
   ```

   Claude will read `CLAUDE.md` automatically and use it as its working brief.

## Loading your vault

The template ships with empty folders so the structure is visible from day one. You have three ways to put real content into `ObsidianVault/`:

### Option A: Start fresh

Open `ObsidianVault/` directly in Obsidian. Obsidian will create a `.obsidian/` config folder inside it. Start writing daily notes, drop PDFs in `~/Desktop/ClaudeDropbox/`, and let Claude fill the rest in as you go.

### Option B: Obsidian Sync (paid)

If you already have an Obsidian Sync vault you want to merge with the template:

1. Open `ObsidianVault/` as a new local vault in Obsidian.
2. Settings → Sync → enable, then point it at your existing remote vault.
3. Accept the merge. Your existing content flows in alongside the template scaffolding.
4. Resolve conflicts — most importantly, decide whether you want this template's `CLAUDE.md` or yours (or splice the two together).

### Option C: iCloud, Dropbox, or local symlink

If your vault already lives somewhere on disk (iCloud Drive, Dropbox folder, NAS, etc.), point the dev container at it instead of the in-repo `ObsidianVault/`:

- **Edit `.devcontainer/devcontainer.json`** and change the source of the `ObsidianVault` mount, e.g.:

  ```json
  "source=${localEnv:HOME}/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault,target=/workspace/ObsidianVault,type=bind,consistency=delegated"
  ```

- **Or symlink** before opening in the container:

  ```bash
  rm -rf ObsidianVault
  ln -s "/path/to/your/vault" ObsidianVault
  ```

Either way, the template's templates/scripts/hooks keep working, just against your real vault.

## Keeping your vault content out of git

The repo's `.gitignore` is set up so that **scaffolding is tracked, your content is not.**

Tracked (so updates flow back upstream and new contributors see the structure):

- The directory layout (via `.gitkeep`)
- `_Templates/` — note templates
- `ObsidianVault/CLAUDE.md` — vault-local brief
- `!TASKS/TASKS.md`, `!NEW-ARRIVALS/NEW-ARRIVALS.md`, `index.md`, `log.md` — navigation files
- `00_Inbox/Papers/queue.md`, `00_Inbox/claude-backlog.md` — triage scaffolding

Ignored (so your private notes stay private):

- Everything under `01_Research/Papers/`, `01_Research/Concepts/`, `01_Research/Projects/`, `01_Research/Summaries/` (except `.gitkeep`)
- All of `02_Admin/`, `03_Personal/`, `04_Daily/`, `05_News/`, `90_Archive/`
- PDFs, images, binaries, Obsidian workspace files

The scaffolding files are tracked — but as soon as you start filling them in, you'll want your edits to stay local. After cloning, run:

```bash
bash scripts/setup-local.sh
```

This calls `git update-index --skip-worktree` on the navigation files so your personal edits to `TASKS.md`, `index.md`, `log.md`, etc. won't appear in `git status` or get accidentally committed when you pull template updates.

To undo it later (e.g. to contribute a scaffolding improvement upstream):

```bash
git update-index --no-skip-worktree <path>
```

## Customization

### Edit `CLAUDE.md`

The shipped `CLAUDE.md` includes placeholder lines for **user description**, **recurring habits examples**, **email-style examples**, and **research-theme list**. Replace these with your own; the more concrete the better — Claude leans on examples heavily.

Sections you might delete entirely if they don't apply to you:

- **Patent FTO** — only useful for IP-adjacent research
- **Email drafting** — only useful if you're sending a lot of vendor / admin / cold-outreach mail
- **Google Calendar / Gmail vault-sync** — needs remote agents; safe to leave but no-ops without setup

Sections to definitely keep and adapt:

- **Vault structure**, **conventions**, **evidence levels**, **core operations** (ingest / query / lint / sweep)

### Edit `_Templates/`

The templates in `ObsidianVault/_Templates/` are [Templater](https://silentvoid13.github.io/Templater/)-compatible. Each one has YAML frontmatter and a recommended section layout. Adjust headings, frontmatter fields, and prose to match your note types.

The bilingual JP/EN section headings (e.g. `## 定義 / Definition`) are an example of what works for a researcher mixing two languages — switch to whatever languages you actually work in, or strip the second one.

### Toggle hooks

Open `.claude/settings.json` to enable, disable, or reorder the SessionStart hooks. Each is a shell script in `.claude/hooks/` that runs on session start and prints surfaced items for Claude to act on.

The Google Calendar and Gmail sync hooks (`sync-gcal.sh`, `check-vault-sync-drafts.sh`) are no-ops without the corresponding remote-agent setup, so they're safe to leave but easy to remove if you find them noisy.

## Optional integrations

- **Paper search MCPs** — `.mcp.json` already wires up `pubmed`, `biorxiv`, `papers`, and `latest-science` MCP servers. Useful for any literature work; harmless if unused. They're invoked by name (e.g. `mcp__pubmed__pubmed_search_articles`) and don't cost anything until called.

- **Google Calendar / Gmail vault-sync** — requires (a) setting up [scheduled remote agents](https://claude.ai/code/scheduled) that create Gmail drafts with `[vault-sync]` in the subject and (b) connecting the GCal MCP to your Google account. See the **Google Calendar → Vault sync** and **Gmail sync** sections in `CLAUDE.md` for the full protocol.

- **Patent FTO** — the assignee-search-first methodology in `CLAUDE.md` is useful for IP-adjacent research (running `FP:(CompanyName)` on WIPO Patentscope before believing any single patent claim). Delete the section if irrelevant.

- **PDF processing** — `scripts/enrich_papers.py` handles PyMuPDF metadata extraction + CrossRef DOI lookup. To see what's missing in your existing paper notes:

  ```bash
  python3 scripts/enrich_papers.py audit
  ```

  Then `pdf-extract`, `crossref`, and `enrich` (with `--dry-run` to preview).

## Hooks reference

Each hook lives in `.claude/hooks/` and is wired up in `.claude/settings.json`.

**SessionStart** (run when a Claude Code session begins):

| Hook | What it surfaces |
|---|---|
| `check-papers-drop.sh` | Unprocessed PDFs in `~/Desktop/ClaudeDropbox/` (mounted at `/workspace/drop/`) |
| `check-inbox.sh` | Unprocessed items in `00_Inbox/` (excluding the queue/backlog files) |
| `check-review-markers.sh` | `%%FLAG%%` / `%%WEAK%%` / `%%EXPAND%%` / `%%MERGE%%` / `%%CUT%%` markers across the vault |
| `check-new-arrivals-age.sh` | Sections of `!NEW-ARRIVALS.md` older than 30 days that should be trimmed |
| `check-backlog.sh` | Open items in `00_Inbox/claude-backlog.md` |
| `check-vault-sync-drafts.sh` | Gmail drafts with `[vault-sync]` subject (waiting to be folded into the daily note) |
| `sync-gcal.sh` | Google Calendar events for the next 14 days (waiting to be embedded into TASKS.md and today's daily note) |

**PreToolUse** (run before Claude edits or writes):

| Hook | What it does |
|---|---|
| `guard-vault-safety.sh` | Blocks edits to `_Templates/` and `01_Research/Raw/` (templates are owned by you; raw sources are immutable) |

**PostToolUse** (run after Claude edits or writes):

| Hook | What it does |
|---|---|
| `check-wikilinks.sh` | Warns if any `[[wikilinks]]` introduced by the edit don't resolve to an existing note |

The convention is that on every SessionStart, Claude should ask you what to do with each surfaced item before acting on it (rather than charging ahead).

## Conventions cheat sheet

A compressed reference; the canonical version is in `CLAUDE.md`.

- **Block IDs:** `^ev-YYMMDD-slug` for calendar events, `^todo-YYMMDD-slug` for user-written tasks. Slug is 1-3 lowercase ASCII words separated by hyphens.
- **Embed syntax:** `![[TASKS#^ev-YYMMDD-slug]]` — no bullet prefix, one per line. Daily notes embed tasks rather than copying them, so `TASKS.md` stays the single source of truth.
- **Evidence levels:** mark every non-obvious factual claim as **Confirmed:** (re-verifiable from a primary source), **Inferred:** (reasoned from adjacent confirmed facts), or **Speculative:** (weak / hypothesis only). Never collapse levels silently.
- **Drop folder:** `~/Desktop/ClaudeDropbox/` mounted read-only at `/workspace/drop/`. Drop PDFs, screenshots, anything you want Claude to ingest. Claude never deletes or writes there.
- **Lint:** ask Claude to *"lint the vault"* — runs the consistency checks in `CLAUDE.md` (broken wikilinks, orphan notes, frontmatter gaps, unprocessed inbox, etc.).
- **Sweep:** ask Claude to *"sweep review markers"* — finds and processes `%%FLAG%%` / `%%WEAK%%` / `%%EXPAND%%` / `%%MERGE%%` / `%%CUT%%` markers in your notes.
- **Web fetching:** Claude won't `WebFetch` publisher sites (they hang on the firewall) — it uses paper-search MCPs or `curl --max-time 5` for arbitrary URLs.

## License

MIT — see [LICENSE](LICENSE). Use it for anything; no warranty.

## Credits

Schema and methodology by **[your name here]**. Adapt freely, share what works.
