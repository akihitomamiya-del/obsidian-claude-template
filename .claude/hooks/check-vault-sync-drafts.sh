#!/bin/bash
# Check Gmail for [vault-sync] drafts created by remote agents
# This hook just signals Claude to process them — the actual Gmail reading
# and vault updating happens in the conversation via MCP tools.

echo "vault-sync: Check Gmail drafts for [vault-sync] subject lines. If any exist, read them, update today's daily note and tasks.md with their contents, then tell the user what was synced."
exit 0
