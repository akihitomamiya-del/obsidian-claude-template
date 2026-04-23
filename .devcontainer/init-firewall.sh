#!/bin/bash
set -euo pipefail

# Firewall setup for the Claude Code devcontainer.
# Default-deny outbound; whitelist only the domains needed for the tools you use.
# This keeps Claude's web access narrow and predictable, so accidental fetches
# to arbitrary publisher sites time out fast instead of hanging the session.

# === CORE: needed for any Claude Code session ===
ALLOWED_DOMAINS=(
    # Claude API
    "api.anthropic.com"
    "statsig.anthropic.com"
    "statsig.com"
    "sentry.io"
    # npm (for MCP servers installed via npx)
    "registry.npmjs.org"
    # GitHub (gh CLI, raw content fetches)
    "github.com"
    "api.github.com"
    "raw.githubusercontent.com"
    "objects.githubusercontent.com"
    # VS Code marketplace / updates
    "update.code.visualstudio.com"
    "marketplace.visualstudio.com"
    "vscode.blob.core.windows.net"
    # PyPI (pip install)
    "pypi.org"
    "files.pythonhosted.org"
    # CrossRef API (DOI -> citation metadata; used by scripts/enrich_papers.py)
    "api.crossref.org"
    # Google APIs (used by various MCP servers)
    "www.googleapis.com"
)

# === LITERATURE / PAPER-SEARCH MCPS ===
# Comment this block out if you don't use the paper-search MCP servers in .mcp.json.
ALLOWED_DOMAINS+=(
    # PubMed E-utilities
    "eutils.ncbi.nlm.nih.gov"
    # bioRxiv / medRxiv API
    "api.biorxiv.org"
    # Semantic Scholar API (paper-search-mcp fallback)
    "api.semanticscholar.org"
    # OpenAlex API (latest-science-mcp, citation data)
    "api.openalex.org"
)

# === SEQUENCING DATA (opt-in) ===
# Uncomment if you use sra-toolkit (prefetch / fasterq-dump / fastq-dump).
# ALLOWED_DOMAINS+=(
#     "locate.ncbi.nlm.nih.gov"
#     "sra-downloadb.be-md.ncbi.nlm.nih.gov"
#     "trace.ncbi.nlm.nih.gov"
#     "sra-pub-run-odp.s3.amazonaws.com"
#     "ftp.sra.ebi.ac.uk"
# )

# === ADD YOUR OWN DOMAINS HERE ===
# ALLOWED_DOMAINS+=(
#     "example.com"
# )

# Create ipset for allowed IPs
ipset create allowed_ips hash:ip -exist
ipset flush allowed_ips

# Resolve and add allowed domains
for domain in "${ALLOWED_DOMAINS[@]}"; do
    ips=$(dig +short "$domain" 2>/dev/null | grep -E '^[0-9]+\.' || true)
    for ip in $ips; do
        ipset add allowed_ips "$ip" -exist
    done
done

# Set up iptables rules
iptables -F OUTPUT 2>/dev/null || true

# Allow loopback
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow DNS
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Allow Docker DNS (127.0.0.11)
iptables -A OUTPUT -d 127.0.0.11 -j ACCEPT

# Allow private networks (for local services)
iptables -A OUTPUT -d 10.0.0.0/8 -j ACCEPT
iptables -A OUTPUT -d 172.16.0.0/12 -j ACCEPT
iptables -A OUTPUT -d 192.168.0.0/16 -j ACCEPT

# Allow whitelisted IPs
iptables -A OUTPUT -m set --match-set allowed_ips dst -j ACCEPT

# Drop everything else
iptables -A OUTPUT -j DROP

echo "Firewall initialized. Testing..."

# Verify: blocked site should fail
if curl -sf --max-time 3 https://example.com > /dev/null 2>&1; then
    echo "WARNING: Firewall may not be working (example.com accessible)"
else
    echo "OK: Blocked sites are inaccessible"
fi

# Verify: API should work
if curl -sf --max-time 5 https://api.anthropic.com > /dev/null 2>&1; then
    echo "OK: Claude API is accessible"
else
    echo "NOTE: Claude API check returned non-200 (may still work with auth)"
fi

echo "Firewall setup complete."
