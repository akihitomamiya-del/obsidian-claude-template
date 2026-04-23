#!/bin/bash
# Check for unprocessed PDFs in drop folder
PAPERS_DIR="/workspace/drop"
MANIFEST="/workspace/.claude/hooks/papers-processed.txt"

if [ ! -d "$PAPERS_DIR" ]; then
  exit 0  # mount not available, skip silently
fi

# Create manifest if it doesn't exist
touch "$MANIFEST"

# Find PDFs not yet in the manifest
UNPROCESSED=()
while IFS= read -r pdf; do
  name=$(basename "$pdf")
  if ! grep -qxF "$name" "$MANIFEST"; then
    UNPROCESSED+=("$name")
  fi
done < <(find "$PAPERS_DIR" -maxdepth 1 -name '*.pdf' 2>/dev/null)

if [ ${#UNPROCESSED[@]} -gt 0 ]; then
  echo "drop/ has ${#UNPROCESSED[@]} PDF(s) waiting to be processed. Ask the user if they'd like you to process them."
  printf '%s\n' "${UNPROCESSED[@]}"
fi

exit 0
