# BOB_USAGE.md

This document records how each team member used IBM Bob during the TrustGate build.

## Bilal Rafique

### Task 1: Base codebase security review
- **Bob feature used**: Agent mode (code review)
- **Files**: `app/routes.py`, `app/config.py`, `app/auth.py`
- **Result**: Bob identified a hardcoded SECRET_KEY in `config.py` (line 4) and an unused `import hashlib` in `auth.py` (line 1). Bob also confirmed `routes.py` had no SQL injection in the base branch.
- **Screenshot**: `screenshots/bilal_01.png`, `screenshots/bilal_02.png`

### Task 2: SQL injection detection on buggy branch
- **Bob feature used**: Agent mode (security review)
- **File**: `app/routes.py` (branch: `issue-03-sql-injection`)
- **Result**: Bob detected an f-string SQL injection at line 16 with the exact evidence quote:
  `query = f"SELECT * FROM orders WHERE user_id = {user['id']}"`
- **Screenshot**: `screenshots/bilal_03.png`

### Task 3: Benchmark script review
- **Bob feature used**: Agent mode (code review)
- **File**: `bench/run_benchmark.py`
- **Result**: Bob reviewed the benchmark loop logic and ground-truth comparison.

---

## Other Members

(Add your sections below)