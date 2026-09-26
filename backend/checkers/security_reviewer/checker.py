"""
Security Reviewer subagent checker.
Owned by: M. Muavia

Role prompt used with IBM Bob (Agent mode):
    You are a security code reviewer. Examine the given diff/files for:
    - hardcoded secrets, API keys, or passwords
    - SQL queries built by string concatenation/f-strings from user input
    - missing authentication/authorization checks on sensitive endpoints
    - unsafe deserialization (e.g. pickle.loads on untrusted input)
    - debug mode enabled in production configuration

    For each issue, report ONLY: file, line, severity (high/medium/low),
    a short quoted evidence snippet, and a one-sentence explanation.
    If you cannot cite file, line, and an exact quote, do not report it.
    Return JSON matching the shared schema (CONTRACT.md).
"""

import json
import datetime
import time


def run(pr_branch: str, run_id: str, findings: list, bob_session: str = "") -> dict:
    """
    Entry point called by the orchestrator.

    Args:
        pr_branch:   Name of the branch/PR being reviewed.
        run_id:      Unique run identifier (e.g. 'sec_001').
        findings:    List of finding dicts produced by Bob (file, line, severity,
                     evidence, explanation, confidence).
        bob_session: Path to Bob screenshot proving agent usage.

    Returns:
        dict matching the runs/*.json contract, also written to runs/{run_id}.json
    """
    started = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
    start_ts = time.time()

    # Evidence rule: drop any finding missing file, line, or evidence
    clean_findings = [
        f for f in findings
        if f.get("file") and f.get("line") and f.get("evidence")
    ]

    result = {
        "run_id": run_id,
        "agent": "security_reviewer",
        "member": "m-muavia",
        "pr": pr_branch,
        "started_at": started.isoformat(),
        "duration_sec": round(time.time() - start_ts, 1),
        "bob_session": bob_session,
        "findings": clean_findings,
        "status": "success",
    }

    out_path = f"runs/{run_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return result
