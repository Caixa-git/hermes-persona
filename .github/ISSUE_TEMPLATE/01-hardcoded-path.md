---
title: "Hardcoded path in test_benchmark.py breaks on other machines"
labels: ["bug"]
---

**Description**

`test_benchmark.py` line 186 has a hardcoded absolute path:

```python
repo_path = "/Users/aiadmin/hermes-persona"
```

This causes the "Repository essential files" test to fail on any machine that isn't the original development machine.

**Fix**

Replaced with a dynamic path:

```python
repo_path = os.path.dirname(os.path.abspath(__file__))
```

**Commit**

9c06024 — resolves the issue by using the script's own location as the repo root.

**Verification**

`python3 test_benchmark.py` — 47/47 passed.
