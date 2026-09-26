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

---

## M. Muavia

### Task 1: PRD requirements extraction — Step A (Spec-Conformance)
- **Bob feature used**: Agent mode (document understanding)
- **Files**: `PRD.pdf`
- **Prompt type**: Step A — extract specific, testable requirements with exact quotes
- **Result**: Bob extracted 8 verified requirements from PRD.pdf, each with an exact quote under 15 words and a plain description. Requirements include bcrypt password hashing (FR-2), rate limiting (FR-3), admin auth (FR-4), parameterized queries (NFR-3), no hardcoded secrets (NFR-1), debug mode disabled (NFR-2).
- **Output**: `runs/spec_001.json`, `runs/spec_002.json`
- **Screenshot**: `screenshots/muavia_01.png`

### Task 2: Spec-Conformance check on issue-08-no-rate-limit — Step B
- **Bob feature used**: Agent mode (code review against verified requirements)
- **Files**: `app/routes.py` (branch: `issue-08-no-rate-limit`)
- **Prompt type**: Step B — check code against verified requirements, cite exact file/line/evidence
- **Result**: Bob found 1 high-severity violation — FR-3 rate limiting entirely absent from all routes. Evidence: `def get_products(db): return db.query("SELECT * FROM products")` at line 3.
- **Output**: `runs/spec_001.json`
- **Screenshot**: `screenshots/muavia_01.png`

### Task 3: Spec-Conformance check on issue-09-weak-hash — Step B
- **Bob feature used**: Agent mode (document understanding + code review)
- **Files**: `app/auth.py`, `app/routes.py` (branch: `issue-09-weak-hash`)
- **Prompt type**: Step B — check code against verified requirements
- **Result**: Bob found 2 high-severity violations — FR-2 bcrypt requirement violated (MD5 used at `auth.py` line 4: `return hashlib.md5(password.encode()).hexdigest()`) and FR-3 rate limiting absent.
- **Output**: `runs/spec_002.json`
- **Screenshot**: `screenshots/muavia_02.png`

### Task 4: Security Reviewer — hardcoded key, SQL injection, missing auth, unsafe deserialize, debug mode
- **Bob feature used**: Agent mode (security review subagent)
- **Branches checked**: `issue-02-hardcoded-key`, `issue-03-sql-injection`, `issue-04-missing-auth`, `issue-05-unsafe-deserialize`, `issue-10-debug-enabled`
- **Result**:
  - issue-02: `API_KEY = "sk-live-abc123hardcodedsecret"` at `config.py:5` — hardcoded secret (high)
  - issue-03: f-string SQL at `routes.py:16` — SQL injection (high)
  - issue-04: `admin_delete_product_v2` at `routes.py:15` — missing auth check (high)
  - issue-05: `pickle.loads(request_data)` at `routes.py:18` — unsafe deserialization (high)
  - issue-10: `DEBUG = True` at `config.py:1` — debug mode in production (high)
- **Output**: `runs/sec_001.json` through `runs/sec_005.json`
- **Screenshot**: `screenshots/muavia_03.png`, `screenshots/muavia_04.png`

### Task 5: False-positive verification on clean branches
- **Bob feature used**: Agent mode (security review + spec conformance)
- **Branches checked**: `clean-01`, `clean-02`, `clean-03`
- **Result**: 0 findings on all 3 clean branches for both Security Reviewer and Spec-Conformance checkers. False-positive rate = 0%.
- **Output**: `runs/sec_clean_01.json`, `runs/sec_clean_02.json`, `runs/sec_clean_03.json`, `runs/spec_clean_01.json`, `runs/spec_clean_02.json`, `runs/spec_clean_03.json`
- **Screenshot**: `screenshots/muavia_05.png`

**Note on document understanding**: Bob's document understanding feature was used to ingest `PRD.pdf` directly in the Spec-Conformance prompts. The Step A prompt instructed Bob to read the PDF and extract only mechanically-verifiable requirements with exact quotes. This avoids hallucinated requirements — if Bob cannot quote it from the document, it is not extracted. One limitation encountered: Bob occasionally flagged vague aspirational statements as requirements; the strict "under 15 words exact quote" rule eliminated these false extractions.