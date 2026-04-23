#!/bin/bash
# Check claude-backlog.md for open items (checkboxes or plain text under ## Open)
BACKLOG="/workspace/ObsidianVault/00_Inbox/claude-backlog.md"

if [ ! -f "$BACKLOG" ]; then
  exit 0
fi

# Extract everything between ## Open and ## Done
OPEN_SECTION=$(sed -n '/^## Open/,/^## Done/p' "$BACKLOG" | sed '1d;$d' | grep -v '^$' | grep -v '^---')

if [ -n "$OPEN_SECTION" ]; then
  COUNT=$(echo "$OPEN_SECTION" | wc -l)
  echo "claude-backlog.md has $COUNT open item(s). Review and address if relevant:"
  echo "$OPEN_SECTION"
fi

exit 0
