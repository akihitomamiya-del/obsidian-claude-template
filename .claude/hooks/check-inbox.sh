#!/bin/bash
# Check for unprocessed items in 00_Inbox/ (excluding queue.md and dotfiles)
INBOX_DIR="/workspace/ObsidianVault/00_Inbox"

if [ ! -d "$INBOX_DIR" ]; then
  exit 0
fi

ITEMS=$(find "$INBOX_DIR" -type f \
  ! -name '.*' \
  ! -name 'queue.md' \
  ! -name 'claude-backlog.md' \
  ! -name '.DS_Store' \
  -not -path '*/.*' \
  2>/dev/null)

COUNT=$(echo "$ITEMS" | grep -c '[^[:space:]]')

if [ "$COUNT" -gt 0 ]; then
  echo "00_Inbox/ has $COUNT unprocessed item(s). Ask the user if they'd like you to triage them:"
  echo "$ITEMS" | while read -r f; do
    echo "  - $(echo "$f" | sed 's|/workspace/ObsidianVault/00_Inbox/||')"
  done
fi

exit 0
