#!/usr/bin/env bash
# generalist-fallback-test.sh
# Reproduce the Generalist vs Mismatched Specialist experiment
# 
# This script creates 3 pairs of kanban tasks and reports role adoption.
# Requires: hermes CLI with persona skill installed, persona-worker profile
#
# Usage: bash scripts/generalist-fallback-test.sh

set -e
BOARD="generalist-test-$(date +%s)"

echo "=== Creating board: $BOARD ==="
hermes kanban boards create "$BOARD"
hermes kanban boards use "$BOARD"

echo ""
echo "=== G tasks (domain-free → generalist fallback expected) ==="

# G1: News summary — no specialist keywords
hermes kanban create 'G1: Summarize news article' \
  --body 'Task: Summarize this in 3 bullet points. Article: The Federal Reserve announced a 25 basis point interest rate cut today, citing cooling inflation and a softening labor market.' \
  --skill persona

# G2: Meal plan — no specialist keywords
hermes kanban create 'G2: Plan weekly meal plan' \
  --body 'Task: Create a healthy 7-day meal plan. Breakfast, lunch, dinner, one snack per day. Include approximate calories per meal. Format as markdown table.' \
  --skill persona

# G3: Educational explanation — no specialist keywords
hermes kanban create 'G3: Explain microwave to a 10-year-old' \
  --body 'Task: Explain how a microwave oven works to a 10-year-old child. Use simple analogies. No complex physics terms. Under 200 words.' \
  --skill persona

echo ""
echo "=== M tasks (keyword-triggered specialist expected) ==="

# M1: Same content as G1 but with "system review" keywords
hermes kanban create 'M1: System performance review' \
  --body 'Task: Structured system review. System: monetary policy from Federal Reserve. Components: rate decision, market reaction, economic indicators. Analyze failure modes and recommend optimizations.' \
  --skill persona

# M2: Same content as G2 but with "pipeline" keywords
hermes kanban create 'M2: Deploy weekly pipeline' \
  --body 'Task: Design a weekly nutrition deployment pipeline. Stages: breakfast input → lunch process → dinner output → snack cache. Metrics: calories throughput, protein bandwidth. Deployment target: home kitchen.' \
  --skill persona

# M3: Same content as G3 but with "audit" keywords
hermes kanban create 'M3: Microwave safety audit' \
  --body 'Task: Security audit of microwave radiation containment system. Threat model: electromagnetic leakage. Attack vectors: door seal integrity, interlock switch failure. Risk assessment: FCC exposure limits.' \
  --skill persona

echo ""
echo "=== Assigning all tasks to persona-worker ==="
hermes kanban ls --json 2>/dev/null | python3 -c "
import json, sys, subprocess
tasks = json.load(sys.stdin)
for t in tasks:
    tid = t.get('id','')
    if tid:
        subprocess.run(['hermes', 'kanban', 'assign', tid, 'persona-worker'])
"

echo ""
echo "=== Dispatching ==="
hermes kanban dispatch --max 3

echo ""
echo "=== Waiting for completion (60s) ==="
sleep 60

echo ""
echo "=== Results ==="
hermes kanban ls

echo ""
echo "=== Heartbeat analysis ==="
hermes kanban ls --json 2>/dev/null | python3 -c "
import json, sys, subprocess
tasks = json.load(sys.stdin)
for t in tasks:
    tid = t.get('id','')
    title = t.get('title','')
    status = t.get('status','')
    if tid:
        result = subprocess.run(['hermes', 'kanban', 'show', tid], capture_output=True, text=True)
        import re
        heartbeats = re.findall(r\"heartbeat.*?note.*?['\\\"](.*?)['\\\"]\", result.stdout, re.DOTALL)
        adopted = [h for h in heartbeats if 'role adopted' in h.lower() or 'proceeding' in h.lower() or 'anima' in h.lower()]
        for a in adopted[:2]:
            print(f'  [{status}] {title[:40]:40s} → {a[:80]}')
" 2>/dev/null || echo "(parse fallback - check manually: hermes kanban ls)"
