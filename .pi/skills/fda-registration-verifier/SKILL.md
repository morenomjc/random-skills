---
name: fda-registration-verifier
description: Verifies Philippine FDA registration details by registration number or product name using the public FDA verification API. Use when the user gives an FDA registration number, product name, or asks to check FDA registration status.
---

# FDA Registration Verifier

## Purpose
Check a Philippine FDA registration by querying the public verification API once per lookup.

## Usage
Run the local helper with the user input:

```bash
bash .pi/skills/fda-registration-verifier/scripts/lookup.sh "FR-4000014622603"
bash .pi/skills/fda-registration-verifier/scripts/lookup.sh "ASHWAGANDHA + MAGNESIUM FOOD SUPPLEMENT"
```

## Rules
- Use only one request per user lookup.
- Do not spam, loop, or retry aggressively.
- Show a brief checking indicator while fetching, then print the result.
- If the request fails, report the failure and stop.
- Accept either a registration number or product name.
- Summarize the returned record(s) clearly and cite the matching fields.

## Output
Print the query and match count, then each matching record with:
- registration / account code
- product name
- brand name
- company name
- validity date
- cancellation status
