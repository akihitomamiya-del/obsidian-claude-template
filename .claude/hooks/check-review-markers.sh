#!/bin/bash
# Scan vault for %%FLAG:%%, %%WEAK%%, %%EXPAND%%, %%MERGE:%%, %%CUT%% review markers
# Skips: _Templates/, 90_Archive/, and lines inside backticks/code blocks/tables (documentation)
VAULT="/workspace/ObsidianVault"

if [ ! -d "$VAULT" ]; then
  exit 0
fi

# Grep for markers, then filter out documentation lines (backtick-wrapped or table rows)
RESULTS=$(grep -rn '%%FLAG:\|%%WEAK\|%%EXPAND\|%%MERGE:\|%%CUT' \
  "$VAULT" \
  --include='*.md' \
  --exclude-dir=_Templates \
  --exclude-dir=90_Archive \
  --exclude=log.md \
  2>/dev/null | grep -v '`%%' | grep -v '| `%%' | grep -v '^.*:.*|.*%%')

if [ -n "$RESULTS" ]; then
  COUNT=$(echo "$RESULTS" | wc -l)
  echo "Found $COUNT review marker(s) in the vault. The user has left feedback to process — ask if they'd like a sweep:"
  echo "$RESULTS" | while read -r line; do
    FILE=$(echo "$line" | sed "s|$VAULT/||" | cut -d: -f1)
    LINENUM=$(echo "$line" | sed "s|$VAULT/||" | cut -d: -f2)
    MARKER=$(echo "$line" | grep -o '%%[A-Z][A-Z]*:[^%]*%%\|%%[A-Z][A-Z]*%%')
    echo "  - $FILE:$LINENUM $MARKER"
  done
fi

exit 0
