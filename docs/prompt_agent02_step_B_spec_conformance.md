You are checking whether a code change violates or is missing any of the
following VERIFIED requirements (these have already been confirmed to
exist in the project's PRD, so treat them as ground truth):

{{VERIFIED_REQUIREMENTS_LIST}}

For each requirement, check the given code. Report a finding ONLY if the
requirement is clearly violated or clearly missing — not if you are unsure,
and not for requirements the code doesn't touch at all.

STRICT EVIDENCE RULE:
Every finding must include the exact file path and line number where the
requirement should have been implemented but wasn't (or was implemented
incorrectly), plus a short verbatim quote of the relevant code. If the
requirement is entirely absent from the code (nothing to quote), quote the
smallest relevant code block instead (e.g. the whole function where it
should exist) and note in your explanation that the requirement is missing
outright.

SEVERITY:
- "high": a security- or data-integrity-related requirement is violated
  (e.g. weak hashing instead of bcrypt, no rate limiting on a public API)
- "medium": a functional requirement is violated with no direct security
  impact
- "low": a minor or cosmetic requirement is violated

EXAMPLE — requirement violated:
Requirement: "passwords must be hashed with bcrypt"
Code file auth/users.py:
  40: password_hash = hashlib.md5(password.encode()).hexdigest()

Correct output:
{
  "findings": [
    {
      "requirement_id": "req_1",
      "file": "auth/users.py",
      "line": 40,
      "severity": "high",
      "evidence": "password_hash = hashlib.md5(password.encode()).hexdigest()",
      "explanation": "PRD requires bcrypt hashing but code uses MD5, a weak hash for passwords.",
      "confidence": 0.9
    }
  ]
}

EXAMPLE — requirement satisfied (report nothing for it):
If the code correctly uses bcrypt, do not include a finding for that
requirement at all. Only report violations or clear absences.

OUTPUT FORMAT — return ONLY this JSON, nothing else:
{
  "findings": [
    {
      "requirement_id": "<matching id from the requirement list>",
      "file": "<exact file path>",
      "line": <exact line number as integer>,
      "severity": "high" | "medium" | "low",
      "evidence": "<exact quoted code>",
      "explanation": "<one sentence>",
      "confidence": <float 0.0 to 1.0>
    }
  ]
}

Now check this code:
{{CODE_INPUT}}
