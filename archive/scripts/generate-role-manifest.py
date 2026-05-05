#!/usr/bin/env python3
"""Generate role-manifest.sha256 — integrity checksums for all agency-agents roles.

Fetches the agency-agents README at the pinned commit, discovers every role .md file,
downloads each one, and computes SHA256 checksums. The resulting manifest allows
verification that fetched role specifications haven't been tampered with.

Usage:
    python3 scripts/generate-role-manifest.py [--output role-manifest.sha256]

Requires: network access to raw.githubusercontent.com
"""

import hashlib
import re
import sys
import time
import urllib.request
from pathlib import Path

# ── configuration ──────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "role-manifest.sha256"

# Pinned agency-agents commit (from install.sh)
PINNED_COMMIT = "783f6a72bfd7f3135700ac273c619d92821b419a"
README_URL = (
    f"https://raw.githubusercontent.com/msitarzewski/agency-agents/"
    f"{PINNED_COMMIT}/README.md"
)
RAW_BASE = (
    f"https://raw.githubusercontent.com/msitarzewski/agency-agents/"
    f"{PINNED_COMMIT}/"
)

# Timeout per fetch (seconds)
FETCH_TIMEOUT = 15
# Delay between fetches to be polite to GitHub's CDN
FETCH_DELAY = 0.3

# ── helpers ────────────────────────────────────────────────────────────

def fetch_url(url: str) -> str:
    """Fetch URL content, return decoded text."""
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-persona/1.0"})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def sha256_content(content: str) -> str:
    """Compute SHA256 of a string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def parse_role_links(readme_text: str) -> list[tuple[str, str, str]]:
    """Extract role file links from the README markdown tables.

    Matches patterns like: [Role Name](category/filename.md)

    Returns list of (category, filename, role_name) tuples.
    """
    # Pattern: [Role Name](category/filename.md) in table cells
    # Categories have dir structure like: engineering/engineering-backend-architect.md
    #                                    or game-development/unity/unity-architect.md
    pattern = re.compile(
        r'\[([^\]]+)\]\(([a-z][a-z0-9_-]*(?:/[a-z][a-z0-9_-]*)*/[a-z][a-z0-9_-]+\.md)\)'
    )

    roles = []
    seen = set()
    for match in pattern.finditer(readme_text):
        role_name = match.group(1)
        file_path = match.group(2)

        # Skip non-role links (badges, etc.)
        if file_path in seen:
            continue
        seen.add(file_path)

        # Extract category from path
        parts = file_path.split("/")
        category = "/".join(parts[:-1])  # everything except filename
        filename = parts[-1].replace(".md", "")

        roles.append((category, filename, role_name))

    return roles


# ── main ───────────────────────────────────────────────────────────────

def main():
    output = OUTPUT_FILE
    if len(sys.argv) > 1:
        if sys.argv[1] == "--output" and len(sys.argv) > 2:
            output = Path(sys.argv[2])
        else:
            print(f"Usage: {sys.argv[0]} [--output PATH]", file=sys.stderr)
            sys.exit(1)

    print(f"📡 Fetching agency-agents README @ {PINNED_COMMIT[:8]}...")
    try:
        readme = fetch_url(README_URL)
    except Exception as e:
        print(f"❌ Failed to fetch README: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Parsing role links...")
    roles = parse_role_links(readme)
    print(f"   Found {len(roles)} role files")

    if not roles:
        print("❌ No role links found in README — check parse pattern", file=sys.stderr)
        sys.exit(1)

    # Fetch each role and compute checksum
    entries = []
    fetched = 0
    failed = 0

    for category, filename, role_name in roles:
        url = f"{RAW_BASE}{category}/{filename}.md"
        try:
            content = fetch_url(url)
            checksum = sha256_content(content)
            rel_path = f"{category}/{filename}.md"
            entries.append(f"{checksum}  {rel_path}")
            fetched += 1
            print(f"   ✅ {rel_path}")
        except Exception as e:
            print(f"   ❌ {category}/{filename}.md — {e}")
            failed += 1
            # Still add a placeholder so the manifest is complete
            entries.append(f"# FAILED: {category}/{filename}.md — {e}")

        # Be polite to GitHub's CDN
        time.sleep(FETCH_DELAY)

    # Write manifest
    output.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Role Manifest — agency-agents @ {PINNED_COMMIT}\n"
        f"# {fetched} roles verified, {failed} failed\n"
        f"# Generated: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n"
        f"# Format: <SHA256>  <category/filename.md>\n"
        f"# Use to verify: sha256sum -c role-manifest.sha256\n"
        f"#\n"
    )
    with open(output, "w") as f:
        f.write(header)
        for entry in entries:
            f.write(entry + "\n")

    print(f"\n✅ Role manifest written: {output}")
    print(f"   {fetched} verified, {failed} failed, {len(roles)} total")


if __name__ == "__main__":
    main()
