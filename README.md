# TrustGate — Muavia's Checker Modules

**Owner**: M. Muavia | **Role**: AI/ML Engineer — Security Reviewer + Spec-Conformance subagents

This repository contains Muavia's deliverables for the TrustGate hackathon project.

## What's in here

| Folder/File | Description |
|---|---|
| `backend/checkers/security_reviewer/` | Security Reviewer subagent — finds hardcoded secrets, SQL injection, missing auth, unsafe deserialization, debug mode |
| `backend/checkers/spec_conformance/` | Spec-Conformance subagent — compares code against PRD requirements using Bob's document understanding |
| `runs/` | One JSON file per checker run (CONTRACT.md format) |
| `PRD.pdf` | Product Requirements Document (source for Spec-Conformance) |
| `policy.pdf` | Security policy document |
| `CONTRACT.md` | Shared JSON contract all checkers follow |
| `BOB_USAGE.md` | Bob session log with screenshots |

## Branches tested

| Branch | Checker | Findings |
|---|---|---|
| `issue-02-hardcoded-key` | Security Reviewer | 1 high — hardcoded API key |
| `issue-03-sql-injection` | Security Reviewer | 1 high — f-string SQL injection |
| `issue-04-missing-auth` | Security Reviewer | 1 high — missing admin auth check |
| `issue-05-unsafe-deserialize` | Security Reviewer | 1 high — pickle.loads on request data |
| `issue-08-no-rate-limit` | Spec-Conformance | 1 high — no rate limiting (FR-3) |
| `issue-09-weak-hash` | Spec-Conformance | 2 high — MD5 instead of bcrypt (FR-2) + no rate limit (FR-3) |
| `issue-10-debug-enabled` | Security Reviewer | 1 high — DEBUG=True in production |
| `clean-01`, `clean-02`, `clean-03` | Both | 0 findings (false-positive rate = 0%) |

## Prompts used

### Step A — PRD Requirement Extraction
Used with IBM Bob Agent mode + document understanding on `PRD.pdf`:
```
You are reading a PRD to extract specific, testable engineering requirements.
Only extract a requirement if it is specific enough to verify mechanically.
For each requirement, quote the exact sentence/phrase under 15 words.
OUTPUT FORMAT: { "requirements": [ { "requirement_id", "quote", "plain_description" } ] }
```

### Step B — Code vs Requirements Check
Used with IBM Bob Agent mode on each branch:
```
You are checking whether code violates any of the following VERIFIED requirements.
For each requirement, check the given code. Report a finding ONLY if clearly violated.
Every finding must include exact file path, line number, and verbatim evidence quote.
OUTPUT FORMAT: { "findings": [ { "requirement_id", "file", "line", "severity",
                                  "evidence", "explanation", "confidence" } ] }
```

### Security Reviewer prompt
```
You are a security code reviewer. Examine the given diff/files for:
- hardcoded secrets, API keys, or passwords
- SQL queries built by string concatenation/f-strings from user input
- missing authentication/authorization checks on sensitive endpoints
- unsafe deserialization (e.g. pickle.loads on untrusted input)
- debug mode enabled in production configuration

For each issue, report ONLY: file, line, severity (high/medium/low),
a short quoted evidence snippet, and a one-sentence explanation.
If you cannot cite file, line, and an exact quote, do not report it.
Return JSON matching the shared schema.
```

## Setup

```bash
git clone https://github.com/Muavia-Ateeq/trustgate_demo.git
cd trustgate_demo
pip install -r requirements.txt
python backend/checkers/security_reviewer/checker.py
python backend/checkers/spec_conformance/checker.py
```
