#!/bin/bash
# Block writes to protected vault locations:
#   - _Templates/ (user-managed, don't edit without asking)
#   - 01_Research/Raw/ (immutable source material)
# Reads stdin for JSON with tool_input.file_path

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

VAULT="/workspace/ObsidianVault"

case "$FILE_PATH" in
  "$VAULT/_Templates/"*)
    echo "Blocked: _Templates/ is user-managed. Ask the user before editing template files." >&2
    exit 2
    ;;
  "$VAULT/01_Research/Raw/"*)
    echo "Blocked: 01_Research/Raw/ contains immutable source material. Claude should never modify raw sources." >&2
    exit 2
    ;;
esac

exit 0
