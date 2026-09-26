# TrustGate — M. Muavia's Checker Modules

**Owner**: M. Muavia | **Role**: AI/ML Engineer — Security Reviewer + Spec-Conformance subagents

## Repo structure

```
backend/checkers/security_reviewer/checker.py   ← Agent 1
backend/checkers/spec_conformance/checker.py    ← Agent 2
docs/prompt_agent01_security_reviewer.md        ← Agent 1 prompt
docs/prompt_agent02_step_A_spec_conformance.md  ← Agent 2 Step A (PRD extract)
docs/prompt_agent02_step_B_spec_conformance.md  ← Agent 2 Step B (code check)
runs/                                           ← 13 JSON run records
screenshots/                                    ← Bob session screenshots
BOB_USAGE.md                                    ← Bob usage log
```

## Branches tested

| Branch | Checker | Finding |
|---|---|---|
| `issue-02-hardcoded-key` | security_reviewer | hardcoded session key — high |
| `issue-03-sql-injection` | security_reviewer | f-string SQL injection — high |
| `issue-04-missing-auth` | security_reviewer | IDOR missing ownership check — high |
| `issue-10-debug-enabled` | security_reviewer | Flask DEBUG=True — high |
| `issue-08-no-rate-limit` | spec_conformance | rate limiting absent — medium |
| `issue-09-weak-hash` | spec_conformance | MD5 instead of PBKDF2 — high |
| `clean-01/02/03` | both | 0 findings (false-positive rate = 0%) |
