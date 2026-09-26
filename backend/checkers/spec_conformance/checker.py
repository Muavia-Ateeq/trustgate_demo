"""
Spec-Conformance subagent checker.
Owned by: M. Muavia

Role prompt used with IBM Bob (Agent mode + document understanding):
    You will be given a Product Requirements Document (PDF) and a code diff.
    Read the PDF carefully. Identify specific, testable requirements
    (e.g. "passwords must be hashed with bcrypt", "API must be rate-limited").
    Compare each requirement against the code. Report ONLY requirements that are
    clearly violated or clearly missing, with: the requirement text (quoted,
    under 15 words), the file/line where it should be implemented, severity,
    and a one-sentence explanation. Do not report requirements you are unsure
    about. Return JSON matching the shared schema (CONTRACT.md).

Step A — Extract verified requirements from PRD:
    Only extract a requirement if it is specific enough to verify mechanically.
    For each requirement, quote the exact sentence/phrase under 15 words.
    Output format: { "requirements": [ { "requirement_id", "quote", "plain_description" } ] }

Step B — Check code against verified requirements:
    For each requirement, check the given code. Report a finding ONLY if the
    requirement is clearly violated or clearly missing — not if unsure.
    Every finding must include exact file path, line number, and verbatim evidence quote.
    Output format: { "findings": [ { "requirement_id", "file", "line", "severity",
                                     "evidence", "explanation", "confidence" } ] }
"""

import json
import datetime
import time


def run(pr_branch: str, run_id: str, findings: list, bob_session: str = "") -> dict:
    """
    Entry point called by the orchestrator.

    Args:
        pr_branch:   Name of the branch/PR being reviewed.
        run_id:      Unique run identifier (e.g. 'spec_001').
        findings:    List of finding dicts from Bob's Step B output
                     (requirement_id, file, line, severity, evidence, explanation, confidence).
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
        "agent": "spec_conformance",
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
