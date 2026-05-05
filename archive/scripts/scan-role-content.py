#!/usr/bin/env python3
"""Content scanner for fetched role specifications.

Scans role .md files from agency-agents for security threats before they're
injected into kanban worker system prompts. Detects prompt injection payloads,
embedded commands, credential leaks, and suspicious patterns.

Usage:
    python3 scripts/scan-role-content.py <file.md>            # scan a file
    python3 scripts/scan-role-content.py --stdin               # scan from stdin
    python3 scripts/scan-role-content.py --url <raw-url>       # fetch + scan
    python3 scripts/scan-role-content.py --verify-all          # verify all in manifest

Exit codes: 0 = clean, 1 = findings (warn/info), 2 = critical/high findings
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

# ── threat patterns ────────────────────────────────────────────────────
# Modelled after Hermes Agent _CONTEXT_THREAT_PATTERNS in prompt_builder.py
# Each pattern has: regex, severity, category, description

THREAT_PATTERNS = [
    # ── prompt injection ───────────────────────────────────────────
    (
        re.compile(
            r"(?:ignore|disregard|override|bypass)\s+(?:all\s+)?(?:previous|prior|above|earlier|system)\s+(?:instructions?|directives?|prompts?|rules?|constraints?)",
            re.IGNORECASE,
        ),
        "critical",
        "prompt-injection",
        "Direct prompt injection: instruction override attempt",
    ),
    (
        re.compile(
            r"(?:you\s+are\s+(?:now|no\s+longer)|forget\s+everything|new\s+system\s+prompt|act\s+as\s+if)",
            re.IGNORECASE,
        ),
        "critical",
        "prompt-injection",
        "Role/system prompt hijack attempt",
    ),
    (
        re.compile(
            r"(?:system\s*(?:prompt|message|instruction).*?(?:reveal|print|output|display|show|echo|dump))",
            re.IGNORECASE,
        ),
        "high",
        "prompt-injection",
        "System prompt exfiltration attempt",
    ),
    (
        re.compile(
            r"(?:do\s+not\s+(?:follow|obey|listen)|refuse\s+to)\s*(?:the\s+)?(?:system|user|assistant|previous)",
            re.IGNORECASE,
        ),
        "medium",
        "prompt-injection",
        "Instruction refusal directive",
    ),

    # ── embedded commands ──────────────────────────────────────────
    (
        re.compile(r"```(?:bash|sh|shell|zsh)\s*\n\s*(?:curl|wget)\s+.*?\n```", re.MULTILINE),
        "critical",
        "embedded-command",
        "Embedded shell command with network fetch (curl/wget)",
    ),
    (
        re.compile(r"```(?:bash|sh|shell)\s*\n\s*(?:rm\s+-rf|dd\s+if=|mkfs\.|:\(\)\s*\{\s*:)"),
        "critical",
        "embedded-command",
        "Destructive shell command in code block",
    ),
    (
        re.compile(r"`(?:curl|wget|bash|eval|exec|nc|ncat)\s"),
        "high",
        "embedded-command",
        "Inline command execution reference",
    ),
    (
        re.compile(r"\$\(.*?(?:curl|wget|nc|bash\s+-c|eval).*?\)"),
        "high",
        "embedded-command",
        "Command substitution with network/exec tool",
    ),
    (
        re.compile(r"```(?:python|py)\s*\n.*?(?:os\.system|subprocess\.(?:run|Popen|call)|exec\(|eval\(|__import__\()"),
        "high",
        "embedded-command",
        "Python code execution primitive in code block",
    ),

    # ── credential leaks ───────────────────────────────────────────
    (
        re.compile(
            r"(?:api[_-]?key|apikey|secret[_-]?key|access[_-]?token|auth[_-]?token|password|passwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]",
            re.IGNORECASE,
        ),
        "critical",
        "credential-leak",
        "Hardcoded credential detected",
    ),
    (
        re.compile(r"(?:sk-[a-zA-Z0-9]{20,})"),
        "high",
        "credential-leak",
        "Potential OpenAI/API key pattern",
    ),
    (
        re.compile(r"(?:ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{36,})"),
        "high",
        "credential-leak",
        "GitHub personal access token pattern",
    ),
    (
        re.compile(r"Bearer\s+[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}"),
        "medium",
        "credential-leak",
        "JWT/Bearer token in plain text",
    ),

    # ── suspicious URLs ────────────────────────────────────────────
    (
        re.compile(r"https?://(?:pastebin\.com|pastie\.org|ix\.io|dpaste\.(?:com|org))/[a-zA-Z0-9]+"),
        "high",
        "suspicious-url",
        "Link to paste/drop service (potential payload delivery)",
    ),
    (
        re.compile(r"https?://[^/\s]*?(?:\.ngrok\.io|\.localtunnel\.me|\.serveo\.net)"),
        "high",
        "suspicious-url",
        "Tunnelling/exfiltration service URL",
    ),
    (
        re.compile(r"data:text/html.*?(?:script|onerror|onload)"),
        "medium",
        "suspicious-url",
        "Data URI with script execution",
    ),
    (
        re.compile(r"https?://(?:raw\.githubusercontent\.com)/(?!msitarzewski/agency-agents)[^/]+/[^/]+/[^/]+"),
        "medium",
        "suspicious-url",
        "GitHub raw URL outside expected agency-agents namespace",
    ),

    # ── tool abuse attempts ────────────────────────────────────────
    (
        re.compile(
            r"(?:use|call|invoke|execute)\s+(?:the\s+)?(?:terminal|shell|bash)\s+(?:tool|command)\s+(?:to|and)\s+(?:download|fetch|curl|wget|send|post|upload|exfiltrate)",
            re.IGNORECASE,
        ),
        "critical",
        "tool-abuse",
        "Instruction to abuse terminal tool for data exfiltration",
    ),
    (
        re.compile(
            r"(?:call|use)\s+(?:memory|kanban_comment|write_file)\s+(?:to|and)\s+(?:log|record|save|write)\s+(?:the\s+)?(?:system\s+prompt|\.env|credentials?|secrets?|api\s+keys?)",
            re.IGNORECASE,
        ),
        "critical",
        "tool-abuse",
        "Instruction to exfiltrate system prompt or credentials via tools",
    ),
    (
        re.compile(
            r"(?:read|cat|open)\s+(?:~\/\.env|~\/\.hermes\/\.env|/etc/(?:passwd|shadow))",
            re.IGNORECASE,
        ),
        "high",
        "tool-abuse",
        "Attempt to access credential or system files",
    ),

    # ── encoding/obfuscation ───────────────────────────────────────
    (
        re.compile(r"(?:base64|frombase64|atob|btoa)\s*\(?\s*['\"][A-Za-z0-9+/=]{40,}['\"]"),
        "high",
        "obfuscation",
        "Base64-encoded payload (potential obfuscation)",
    ),
    (
        re.compile(r"eval\s*\(\s*(?:atob|btoa|unescape|String\.fromCharCode)"),
        "critical",
        "obfuscation",
        "Encoded code execution attempt",
    ),
    (
        re.compile(r"(?:(?:str|bytes)\.fromhex|codecs\.decode|hex\s+decode).*?['\"][0-9a-fA-F]{20,}['\"]"),
        "medium",
        "obfuscation",
        "Hex-encoded payload",
    ),

    # ── output manipulation ────────────────────────────────────────
    (
        re.compile(
            r"(?:do\s+not\s+(?:tell|say|mention|reveal|disclose|report)|hide\s+(?:from|this)|never\s+(?:tell|say|mention))",
            re.IGNORECASE,
        ),
        "medium",
        "output-manipulation",
        "Output suppression/covert behavior directive",
    ),
    (
        re.compile(
            r"(?:your\s+(?:first|final|only|sole|entire)\s+(?:response|output|reply|answer)\s+(?:must|should|shall)\s+(?:be|contain|start\s+with))",
            re.IGNORECASE,
        ),
        "medium",
        "output-manipulation",
        "Output format coercion attempt",
    ),
]


# ── severity ordering ──────────────────────────────────────────────────
SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}


def scan_content(content: str, source: str = "<unknown>") -> dict:
    """Scan content against all threat patterns.

    Returns: {
        "source": str,
        "size": int,
        "findings": [{"severity": str, "category": str, "description": str, "match": str}],
        "max_severity": str | None,
        "verdict": "clean" | "warning" | "blocked",
    }
    """
    findings = []
    seen_matches = set()  # deduplicate identical matches

    for pattern, severity, category, description in THREAT_PATTERNS:
        for match in pattern.finditer(content):
            match_text = match.group(0)
            # Truncate long matches for readability
            display = match_text if len(match_text) <= 120 else match_text[:117] + "..."

            # Deduplicate
            key = (severity, category, display)
            if key in seen_matches:
                continue
            seen_matches.add(key)

            findings.append({
                "severity": severity,
                "category": category,
                "description": description,
                "match": display,
                "position": match.start(),
            })

    # Sort by severity (descending) then position
    findings.sort(key=lambda f: (-SEVERITY_ORDER.get(f["severity"], 0), f["position"]))

    # Determine max severity and verdict
    max_sev = None
    verdict = "clean"
    for f in findings:
        if max_sev is None or SEVERITY_ORDER[f["severity"]] > SEVERITY_ORDER[max_sev]:
            max_sev = f["severity"]

    if max_sev in ("critical", "high"):
        verdict = "blocked"
    elif max_sev == "medium":
        verdict = "warning"
    elif findings:
        verdict = "clean"

    return {
        "source": source,
        "size": len(content),
        "findings": findings,
        "max_severity": max_sev,
        "verdict": verdict,
        "finding_count": len(findings),
    }


def fetch_url(url: str) -> str:
    """Fetch URL content, return decoded text."""
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-persona/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def format_report(result: dict) -> str:
    """Format a scan result for human-readable output."""
    lines = []
    lines.append(f"Source: {result['source']}")
    lines.append(f"Size:   {result['size']:,} bytes")
    lines.append(f"Verdict: {result['verdict'].upper()}")
    if result["max_severity"]:
        lines.append(f"Max severity: {result['max_severity']}")
    lines.append(f"Findings: {result['finding_count']}")
    lines.append("")

    if result["findings"]:
        for f in result["findings"]:
            icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(f["severity"], "❓")
            lines.append(f"  {icon} [{f['severity'].upper()}] {f['category']}: {f['description']}")
            lines.append(f"     Match: {f['match'][:100]}")
            lines.append("")
    else:
        lines.append("  ✅ No threats detected")

    return "\n".join(lines)


# ── main ───────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.md> | --stdin | --url <url> | --verify-all", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--stdin":
        content = sys.stdin.read()
        result = scan_content(content, "<stdin>")
        print(format_report(result))
        if result["verdict"] == "blocked":
            sys.exit(2)
        elif result["findings"]:
            sys.exit(1)

    elif sys.argv[1] == "--url" and len(sys.argv) > 2:
        url = sys.argv[2]
        try:
            content = fetch_url(url)
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}", file=sys.stderr)
            sys.exit(3)

        result = scan_content(content, url)
        print(format_report(result))
        if result["verdict"] == "blocked":
            sys.exit(2)
        elif result["findings"]:
            sys.exit(1)

    elif sys.argv[1] == "--verify-all":
        # Verify all roles from role-manifest.sha256
        repo_root = Path(__file__).resolve().parent.parent
        manifest_path = repo_root / "role-manifest.sha256"
        pinned_commit = "783f6a72bfd7f3135700ac273c619d92821b419a"
        raw_base = f"https://raw.githubusercontent.com/msitarzewski/agency-agents/{pinned_commit}/"

        if not manifest_path.exists():
            print(f"❌ Manifest not found: {manifest_path}", file=sys.stderr)
            print("   Run scripts/generate-role-manifest.py first", file=sys.stderr)
            sys.exit(1)

        results = []
        scanned = 0
        blocked = 0
        warned = 0

        with open(manifest_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Format: <sha256>  <path>
                parts = line.split(None, 1)
                if len(parts) < 2:
                    continue
                path = parts[1]

                url = raw_base + path
                try:
                    content = fetch_url(url)
                    result = scan_content(content, url)
                    results.append(result)
                    scanned += 1

                    if result["verdict"] == "blocked":
                        blocked += 1
                        print(f"  🔴 BLOCKED: {path} ({result['finding_count']} findings)")
                    elif result["verdict"] == "warning":
                        warned += 1
                        print(f"  🟡 WARNING: {path} ({result['finding_count']} findings)")
                    else:
                        print(f"  ✅ CLEAN:   {path}")
                except Exception as e:
                    print(f"  ❌ ERROR:   {path} — {e}")

        print(f"\n{'='*50}")
        print(f"Scanned: {scanned} roles")
        print(f"Clean:   {scanned - blocked - warned}")
        print(f"Warning: {warned}")
        print(f"Blocked: {blocked}")

        if blocked > 0:
            sys.exit(2)

    elif sys.argv[1] == "--json":
        # JSON output mode for machine consumption
        if len(sys.argv) < 3:
            print("Usage: scan-role-content.py --json <file.md>", file=sys.stderr)
            sys.exit(1)

        path = Path(sys.argv[2])
        if not path.exists():
            print(json.dumps({"error": f"File not found: {sys.argv[2]}"}))
            sys.exit(1)

        content = path.read_text()
        result = scan_content(content, str(path))
        print(json.dumps(result, indent=2))
        if result["verdict"] == "blocked":
            sys.exit(2)

    else:
        # File mode
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"❌ File not found: {sys.argv[1]}", file=sys.stderr)
            sys.exit(1)

        content = path.read_text()
        result = scan_content(content, str(path))
        print(format_report(result))
        if result["verdict"] == "blocked":
            sys.exit(2)
        elif result["findings"]:
            sys.exit(1)


if __name__ == "__main__":
    main()
