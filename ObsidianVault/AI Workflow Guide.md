# AI Workflow Guide

This vault is designed to work with **Claude Code** as an AI assistant that reads, writes, and maintains your knowledge base.

---

## Setup

This template ships with a devcontainer that mounts your vault at `/workspace/ObsidianVault` inside the container. See the repo `README.md` for setup options (Obsidian Sync, iCloud, symlink to existing vault, etc.).

To start a session inside the devcontainer:

```bash
claude --dangerously-skip-permissions
```

The dev container is sandboxed by the firewall configured in `.devcontainer/init-firewall.sh`, so `--dangerously-skip-permissions` is safe — only whitelisted hosts are reachable from inside.

---

## What Claude does

Claude follows the schema in `CLAUDE.md` (project root) and the vault-local brief at `ObsidianVault/CLAUDE.md`. The schema covers:

- **Templates** — every new note uses a template from `_Templates/` and gets YAML frontmatter
- **Wikilinks** — every new note connects to existing concepts via `[[wikilinks]]`; back-links go on the target page
- **Single-source-of-truth tasks** — all persistent tasks live in `!TASKS/TASKS.md` with `^block-IDs`; daily notes embed via `![[TASKS#^block-id]]` rather than copying
- **Hooks** — SessionStart hooks surface unprocessed PDFs, inbox items, review markers, and stale arrivals so they're never forgotten
- **Lint & sweep** — ask Claude to "lint the vault" (consistency check) or "sweep review markers" (process `%%FLAG%%` / `%%WEAK%%` / `%%EXPAND%%` / `%%MERGE%%` / `%%CUT%%`)

See `CLAUDE.md` for the full conventions reference and the recurring operations Claude knows how to run.
