#!/bin/bash
# After editing a vault file, check that any [[wikilinks]] in the file resolve to real files
# Reads stdin for JSON with tool_input.file_path

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

VAULT="/workspace/ObsidianVault"

# Only run for vault files
case "$FILE_PATH" in
  "$VAULT/"*) ;;
  *) exit 0 ;;
esac

if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Extract all [[wikilinks]] from the file (strip display text after |)
LINKS=$(grep -oP '\[\[\K[^\]|]+' "$FILE_PATH" 2>/dev/null | sort -u)

if [ -z "$LINKS" ]; then
  exit 0
fi

BROKEN=""
while IFS= read -r link; do
  # Skip links with anchors (Page#section) — check the page part
  PAGE=$(echo "$link" | cut -d'#' -f1)
  [ -z "$PAGE" ] && continue

  # Search for the file anywhere in the vault
  FOUND=$(find "$VAULT" -name "$PAGE.md" -o -name "$PAGE" 2>/dev/null | head -1)
  if [ -z "$FOUND" ]; then
    BROKEN="$BROKEN\n  - [[$link]]"
  fi
done <<< "$LINKS"

if [ -n "$BROKEN" ]; then
  RELATIVE=$(echo "$FILE_PATH" | sed "s|$VAULT/||")
  echo "Broken wikilinks found in $RELATIVE:$BROKEN"
  echo "Consider creating these pages or fixing the links."
fi

exit 0
