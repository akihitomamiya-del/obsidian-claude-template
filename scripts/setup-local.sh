#!/bin/bash
# setup-local.sh — one-time setup after cloning.
#
# The template ships scaffolding versions of several navigation files
# (TASKS.md, index.md, log.md, etc.). Once you start adding your own content
# to them, you almost certainly want those edits to stay local — not show up
# as unstaged changes in `git status`, and not get accidentally committed.
#
# `git update-index --skip-worktree <file>` tells git to pretend the file is
# unchanged: your local edits won't appear in `git status` or `git diff`, and
# they won't be included in commits. The file remains tracked in the repo.
#
# Reverse it later with: git update-index --no-skip-worktree <file>

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FILES=(
    "ObsidianVault/CLAUDE.md"
    "ObsidianVault/00_Home.md"
    "ObsidianVault/AI Workflow Guide.md"
    "ObsidianVault/index.md"
    "ObsidianVault/log.md"
    "ObsidianVault/!TASKS/TASKS.md"
    "ObsidianVault/!NEW-ARRIVALS/NEW-ARRIVALS.md"
    "ObsidianVault/00_Inbox/Papers/queue.md"
    "ObsidianVault/00_Inbox/claude-backlog.md"
)

echo "Marking navigation templates as skip-worktree (local edits stay local):"
for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        git update-index --skip-worktree "$f"
        echo "  skip-worktree  $f"
    else
        echo "  MISSING        $f  (skipped)"
    fi
done

echo ""
echo "Done. To check status:    git ls-files -v | grep '^S'"
echo "To revert a single file:  git update-index --no-skip-worktree <path>"
