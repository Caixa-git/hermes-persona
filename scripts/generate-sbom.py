#!/usr/bin/env python3
"""Generate CycloneDX 1.4 SBOM for hermes-persona.

Produces sbom.cdx.json listing all repo components and their SHA256 checksums,
plus external dependencies (agency-agents, Hermes Agent).

Usage:
    python3 scripts/generate-sbom.py [--output sbom.cdx.json]
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── configuration ──────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "sbom.cdx.json"

# External dependencies (supply chain)
EXTERNAL_DEPS = [
    {
        "name": "agency-agents",
        "version": "783f6a72bfd7f3135700ac273c619d92821b419a",
        "purl": "pkg:github/msitarzewski/agency-agents@783f6a72bfd7f3135700ac273c619d92821b419a",
        "url": "https://github.com/msitarzewski/agency-agents",
        "description": "172 specialist role definitions across 15 domains — runtime dependency for persona role adoption",
    },
    {
        "name": "hermes-agent",
        "version": "latest",
        "purl": "pkg:github/NousResearch/hermes-agent@latest",
        "url": "https://github.com/NousResearch/hermes-agent",
        "description": "Kanban-based multi-agent orchestration framework — install-time dependency",
    },
]

# Files to exclude from SBOM (generated, git-internal, or SBOM itself)
EXCLUDE_PATTERNS = {
    ".git/",
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "sbom.cdx.json",
    "install.sh.sha256",
    "role-manifest.sha256",
}

# ── helpers ────────────────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def should_exclude(rel_path: str) -> bool:
    """Check if a relative path matches any exclusion pattern."""
    for pat in EXCLUDE_PATTERNS:
        if pat.startswith("*"):
            # Extension pattern
            ext = pat[1:]
            if rel_path.endswith(ext):
                return True
        elif rel_path.startswith(pat) or pat in rel_path:
            return True
    return False


def collect_repo_files(root: Path) -> list[dict]:
    """Walk the repo and collect file metadata."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git and __pycache__
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__"}]

        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            rel = str(fpath.relative_to(root))

            if should_exclude(rel):
                continue

            try:
                checksum = sha256_file(fpath)
            except OSError:
                continue

            files.append({
                "path": rel,
                "sha256": checksum,
                "size": fpath.stat().st_size,
            })

    return files


def build_sbom(files: list[dict]) -> dict:
    """Build a CycloneDX 1.4 SBOM document."""
    now = datetime.now(timezone.utc).isoformat()

    components = []
    for i, f in enumerate(files):
        components.append({
            "type": "file",
            "bom-ref": f"hermes-persona:{f['path']}",
            "name": f["path"],
            "description": f"Repository file: {f['path']}",
            "hashes": [{"alg": "SHA-256", "content": f["sha256"]}],
            "properties": [
                {"name": "cdx:file:path", "value": f["path"]},
                {"name": "cdx:file:size", "value": str(f["size"])},
            ],
        })

    # Add external dependencies
    for dep in EXTERNAL_DEPS:
        components.append({
            "type": "library",
            "bom-ref": f"external:{dep['name']}",
            "name": dep["name"],
            "version": dep["version"],
            "purl": dep["purl"],
            "description": dep["description"],
            "externalReferences": [
                {
                    "type": "website",
                    "url": dep["url"],
                    "comment": "Upstream repository",
                }
            ],
        })

    return {
        "$schema": "http://cyclonedx.org/schema/bom-1.4.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "serialNumber": f"urn:uuid:{_uuid_v4()}",
        "version": 1,
        "metadata": {
            "timestamp": now,
            "tools": [
                {
                    "vendor": "hermes-persona",
                    "name": "generate-sbom.py",
                    "version": "1.0.0",
                }
            ],
            "component": {
                "type": "application",
                "bom-ref": "hermes-persona",
                "name": "hermes-persona",
                "version": "1.0.0",
                "description": (
                    "Persona skill for Hermes Agent — automatic specialist role "
                    "adoption for kanban workers. Zero-configuration, zero-dependency "
                    "installer that patches KANBAN_GUIDANCE in prompt_builder.py."
                ),
                "purl": "pkg:github/Caixa-git/hermes-persona@main",
                "externalReferences": [
                    {
                        "type": "website",
                        "url": "https://github.com/Caixa-git/hermes-persona",
                        "comment": "Public repository",
                    }
                ],
            },
        },
        "components": components,
        "dependencies": [
            {
                "ref": "hermes-persona",
                "dependsOn": [f"external:{d['name']}" for d in EXTERNAL_DEPS],
            }
        ],
    }


def _uuid_v4() -> str:
    """Generate a random UUID v4 (stdlib only, no uuid module needed for reproducibility)."""
    import random
    def hex4():
        return format(random.getrandbits(16), '04x')
    return f"{hex4()}{hex4()}-{hex4()}-4{hex4()[1:]}-{hex4()}-{hex4()}{hex4()}{hex4()}"


# ── main ───────────────────────────────────────────────────────────────

def main():
    output = OUTPUT_FILE
    if len(sys.argv) > 1:
        if sys.argv[1] == "--output" and len(sys.argv) > 2:
            output = Path(sys.argv[2])
        else:
            print(f"Usage: {sys.argv[0]} [--output PATH]", file=sys.stderr)
            sys.exit(1)

    print(f"🔍 Scanning repository: {REPO_ROOT}")
    files = collect_repo_files(REPO_ROOT)
    print(f"   Found {len(files)} files")

    print(f"🔨 Building CycloneDX SBOM...")
    sbom = build_sbom(files)

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        json.dump(sbom, f, indent=2)
        f.write("\n")

    print(f"✅ SBOM written: {output} ({output.stat().st_size:,} bytes)")
    print(f"   Components: {len(files)} repo files + {len(EXTERNAL_DEPS)} external deps = {len(files) + len(EXTERNAL_DEPS)} total")
    print(f"   Schema: CycloneDX 1.4")
    print(f"   Spec: https://cyclonedx.org/specification/overview/")


if __name__ == "__main__":
    main()
