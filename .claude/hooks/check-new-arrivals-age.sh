#!/bin/bash
# Check if !NEW-ARRIVALS.md has entries older than 30 days
ARRIVALS="/workspace/ObsidianVault/!NEW-ARRIVALS.md"

if [ ! -f "$ARRIVALS" ]; then
  exit 0
fi

CUTOFF=$(date -d "30 days ago" +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d 2>/dev/null)

if [ -z "$CUTOFF" ]; then
  exit 0
fi

OLD_DATES=$(grep -oP '^## \K\d{4}-\d{2}-\d{2}' "$ARRIVALS" 2>/dev/null | while read -r d; do
  if [ "$d" \< "$CUTOFF" ]; then
    echo "$d"
  fi
done)

if [ -n "$OLD_DATES" ]; then
  COUNT=$(echo "$OLD_DATES" | wc -l)
  echo "!NEW-ARRIVALS.md has $COUNT date section(s) older than 30 days that should be trimmed:"
  echo "$OLD_DATES" | while read -r d; do
    echo "  - $d"
  done
fi

exit 0
