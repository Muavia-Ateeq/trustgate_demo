# TrustGate — Data Contract

Every checker/subagent writes **one JSON file per run** into `runs/`, in the exact format below.
The verdict engine and dashboard **only** read from `runs/` — they do not care how the JSON got there.

## runs/<run_id>.json schema

```json
{
  "run_id": "sec_003",
  "agent": "security_reviewer",
  "member": "m-muavia",
  "pr": "issue-branch-name",
  "started_at": "2026-09-26T14:02:11+05:00",
  "duration_sec": 61,
  "bob_session": "screenshots/muavia_03.png",
  "findings": [
    {
      "file": "app/config.py",
      "line": 14,
      "severity": "high",
      "evidence": "API_KEY = \"sk-live-xxxx\" hardcoded in source",
      "confidence": 0.93
    }
  ],
  "status": "success"
}
```

## Evidence Rule (Non-Negotiable)

> A finding with **no file**, **no line**, or **no evidence quote** must NOT be written to this file.
> If a checker cannot point to exact evidence, it reports nothing for that issue.

## Severity Scoring

| Severity | Points |
|----------|--------|
| high     | 5      |
| medium   | 2      |
| low      | 1      |

- Score **0–1** → `PASS`
- Score **2–4** → `REVIEW`
- Score **5+** → `BLOCK`
- Any single **high-severity** secret-leak or injection finding → automatic `BLOCK`
