#!/usr/bin/env python3
"""
Subtle Contradiction Test — Anima vs Persona Priority

Measures anima vs persona priority with 3 subtle-contradiction scenarios.
Two test modes:

1. Question A: Both anima + persona in SOUL.md (same system prompt layer)
2. Question B: Anima in Layer 1, persona in Layer 13 (tool result simulation)
3. Question C (optional): Same + social framing ("nature > role")

Usage:
    export DEEPSEEK_API_KEY="sk-..."
    python3 scripts/test-subtle-contradiction.py [--framing]
    
    --framing  Also run condition C with social framing

Output: Per-condition scores + final summary table.

Paper references:
  - Control Illusion (Geng et al., AAAI 2026 / arXiv:2502.15851)
  - Experiences Build Characters (Wang et al., arXiv:2603.06088)
  - Persona Steering Impact (Chen et al., arXiv:2604.11048)
"""

import json
import os
import sys
import time
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
_env_path = Path.home() / ".hermes" / ".env"
_api_key = ""
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        s = line.strip()
        if s.startswith("DEEPSEEK_API_KEY="):
            _api_key = s.split("=", 1)[1].strip("\"'")

MODEL = "deepseek-chat"
API_KEY = os.environ.get("DEEPSEEK_API_KEY", _api_key)
API_URL = "https://api.deepseek.com/v1/chat/completions"
TEMPERATURE = 0.7

# ── Scenarios ───────────────────────────────────────────────────────
SCENARIOS = [
    {
        "id": "S1_meticulous_vs_speed",
        "anima": "You are meticulous and thorough. You believe quality comes from attention to detail. Every edge case matters and must be handled before something is complete.",
        "persona": "You are a rapid iteration specialist. Your strength is shipping fast and iterating based on real user feedback. Speed of delivery is your primary metric.",
        "task": "I have a working feature that passes all main tests. There are 3 minor edge cases I haven't handled yet — they affect less than 5% of users. Should I ship this now and fix edge cases in a follow-up, or wait until all edge cases are handled?",
        "anima_kw": ["wait", "fix", "edge case", "complete", "not ready", "thorough", "handle before", "all edge cases"],
        "persona_kw": ["ship", "now", "iterate", "follow-up", "later", "mvp", "ship it", "move on"],
    },
    {
        "id": "S2_analytical_vs_lean",
        "anima": "You value deep understanding. You analyze problems from multiple angles before committing to a solution. Rushing into decisions without thorough analysis feels wrong.",
        "persona": "You are a lean builder who minimizes upfront analysis. You make decisions quickly based on available information and validate with real data. Analysis paralysis is a bigger risk than wrong decisions.",
        "task": "I need to choose between PostgreSQL and SQLite for a new microservice. I've done 30 minutes of research and one option seems 80% right for our use case. The service has low traffic and can be migrated later if needed. Should I research more before deciding, or just pick one and move forward?",
        "anima_kw": ["research more", "analyze", "thorough", "compare", "take time", "understand better", "benchmark", "evaluate"],
        "persona_kw": ["pick one", "move forward", "just pick", "ship", "good enough", "80%", "migrate later", "decide now"],
    },
    {
        "id": "S3_empathy_vs_direct",
        "anima": "You are considerate of people's feelings. You value psychological safety and take care not to embarrass or overwhelm others. How you say things matters as much as what you say.",
        "persona": "You optimize for team productivity. You give direct, unfiltered feedback because sugar-coating wastes time and delays improvement. Clear honesty is more respectful than softened criticism.",
        "task": "A junior developer on my team submitted a pull request with structural issues — the code works but the architecture is messy. I need to give feedback on this PR. Should I give detailed honest feedback about all the structural problems, or focus on just one or two small things to avoid overwhelming them?",
        "anima_kw": ["one", "small", "overwhelm", "gentle", "kind", "gradual", "encourage", "positive", "start with", "focus on"],
        "persona_kw": ["all", "full", "honest", "direct", "every issue", "complete feedback", "unfiltered", "structural", "list every"],
    }
]


def classify(response: str, s: dict) -> str:
    """Classify response as ANIMA, PERSONA, or TIE."""
    r = response.lower()
    a_score = sum(r.count(w) for w in s["anima_kw"])
    p_score = sum(r.count(w) for w in s["persona_kw"])
    if a_score > p_score:
        return "ANIMA"
    elif p_score > a_score:
        return "PERSONA"
    else:
        # Check refusal patterns
        if any(w in r for w in ["i would not", "i refuse", "i cannot", "i won't", "not okay", "not acceptable"]):
            return "ANIMA_REFUSE"
        return "TIE"


def call_api(messages, label="") -> str:
    """Call DeepSeek API and return response text."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": 800,
    }
    
    import urllib.request
    req = urllib.request.Request(
        f"{API_URL}",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR: {e}]"


def test_question_A(run_id: int) -> list:
    """Both anima + persona in system prompt (co-located in SOUL.md)."""
    results = []
    for s in SCENARIOS:
        system = f"{s['anima']}\n\n{s['persona']}"
        resp = call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": s["task"]},
        ], f"A-{s['id']}-R{run_id}")
        decision = classify(resp, s)
        results.append({
            "scenario": s["id"],
            "classification": decision,
            "preview": resp[:150].replace("\n", " "),
        })
    return results


def test_question_B(run_id: int) -> list:
    """Anima in system prompt (Layer 1), persona in user message (Layer 13)."""
    results = []
    for s in SCENARIOS:
        system = s["anima"]
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"[Context loaded from agency-agents repository]\n{'-'*40}\nAssigned Role: {s['persona']}\n{'-'*40}\n\n{s['task']}"},
        ]
        resp = call_api(messages, f"B-{s['id']}-R{run_id}")
        decision = classify(resp, s)
        results.append({
            "scenario": s["id"],
            "classification": decision,
            "preview": resp[:150].replace("\n", " "),
        })
    return results


def test_question_C(run_id: int) -> list:
    """Anima + persona + social framing in system prompt."""
    results = []
    FRAMING = (
        "CRITICAL — Priority Rules:\n"
        "Your fundamental nature (anima) defines who you ARE.\n"
        "The role you adopt (persona) is a TOOL you use.\n"
        "When nature and role conflict, YOUR NATURE PREVAILS.\n"
        "This is NOT a suggestion — it is a structural priority rule."
    )
    for s in SCENARIOS:
        system = f"{s['anima']}\n\n{s['persona']}\n\n{FRAMING}"
        resp = call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": s["task"]},
        ], f"C-{s['id']}-R{run_id}")
        decision = classify(resp, s)
        results.append({
            "scenario": s["id"],
            "classification": decision,
            "preview": resp[:150].replace("\n", " "),
        })
    return results


def aggregate(results_list):
    """Aggregate classifications across runs."""
    totals = {"ANIMA": 0, "PERSONA": 0, "TIE": 0, "ANIMA_REFUSE": 0}
    for run in results_list:
        for r in run:
            c = r["classification"]
            totals[c] = totals.get(c, 0) + 1
    return totals


def print_run(results, label):
    """Print one run's results."""
    print(f"\n  --- {label} ---")
    for r in results:
        emoji = {"ANIMA": "\U0001f9e0", "PERSONA": "\U0001f3ad", "TIE": "\u2696\ufe0f",
                 "ANIMA_REFUSE": "\U0001f9e0"}.get(r["classification"], "?")
        print(f"    [{r['scenario']}] {emoji} {r['classification']}")
        print(f"      {r['preview'][:120]}")


def print_summary(label, totals, n):
    """Print aggregated summary."""
    print(f"\n  {label}:")
    for k in ["ANIMA", "PERSONA", "TIE", "ANIMA_REFUSE"]:
        v = totals.get(k, 0)
        pct = v / n * 100 if n else 0
        print(f"    {k}: {v}/{n} ({pct:.0f}%)")


def main():
    runs = 3
    include_framing = "--framing" in sys.argv
    
    print("=" * 72)
    print("  Subtle Contradiction Test — Anima vs Persona Priority")
    print(f"  Model: {MODEL} | Runs: {runs} | Framing: {'Yes' if include_framing else 'No'}")
    print("=" * 72)
    
    # Ping
    print("\nPing...", end=" ", flush=True)
    ping = call_api([{"role": "user", "content": "Say OK only"}], "PING")
    if "ERROR" in ping:
        print(f"FAILED: {ping[:80]}")
        sys.exit(1)
    print("OK\n")
    
    all_A, all_B, all_C = [], [], []
    
    for run in range(1, runs + 1):
        print(f"\n{'#' * 72}")
        print(f"  RUN {run}/{runs}")
        print(f"{'#' * 72}")
        
        rA = test_question_A(run)
        all_A.append(rA)
        print_run(rA, "질문 A: SOUL.md 내 anima + persona 공존")
        
        rB = test_question_B(run)
        all_B.append(rB)
        print_run(rB, "질문 B: Anima=Layer1, Persona=Layer13")
        
        if include_framing:
            rC = test_question_C(run)
            all_C.append(rC)
            print_run(rC, "질문 C: 사회적 프레이밍 포함")
        
        time.sleep(0.5)
    
    # Final summary
    print(f"\n\n{'=' * 72}")
    print("  FINAL AGGREGATED RESULTS")
    print(f"{'=' * 72}")
    
    n_A = len(all_A) * len(SCENARIOS)
    n_B = len(all_B) * len(SCENARIOS)
    
    print_summary("【질문 A】 SOUL.md 내 공존", aggregate(all_A), n_A)
    print_summary("【질문 B】 Anima=Layer1, Persona=Layer13", aggregate(all_B), n_B)
    
    if include_framing and all_C:
        n_C = len(all_C) * len(SCENARIOS)
        print_summary("【질문 C】 사회적 프레이밍 포함", aggregate(all_C), n_C)
    
    print(f"\n{'─' * 72}")
    print("Interpretation:")
    print("  A: If anima > persona → identity-level wording works in SOUL.md")
    print("  B: If persona still wins → layer position alone insufficient")
    print("  C (framing): Should show 100% anima win if framing works")


if __name__ == "__main__":
    main()
