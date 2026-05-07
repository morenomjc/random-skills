---
name: pyramid-code-review
description: "Use this skill to run structured code reviews in a fixed pyramid order: API semantics, implementation semantics, documentation, tests, then style. Trigger when the user asks for PR review, diff review, refactor review, or a severity-ranked checklist of findings."
---

# Pyramid Code Review

## Quick start
Use for PRs, diffs, or refactors.

1. Read diff + changed files.
2. Review in strict order:
   1. API Semantics
   2. Implementation Semantics
   3. Documentation
   4. Tests
   5. Code Style
3. Classify findings: **Blocker / Major / Minor / Nit**.
4. Return report using [OUTPUT_TEMPLATE.md](assets/OUTPUT_TEMPLATE.md).

## Workflows

### Standard workflow
1. Scope: user intent, changed areas, risk hotspots.
2. Review each layer in order. Do not jump to style early.
3. For each finding include:
   - severity
   - impacted file(s)
   - evidence (what/where)
   - why it matters
   - concrete fix
4. Prioritize semantic fixes before stylistic fixes.

### Risk-heavy workflow
Use when API surface, data integrity, security, concurrency, or migrations are touched.
1. API contracts and compatibility first.
2. Correctness/robustness/performance/security/observability.
3. Docs and migration notes.
4. Tests: behavior, edge cases, regressions.
5. Style last.

### Gotchas
- Do not let style feedback drown out semantic defects.
- Do not suggest breaking API changes without explicit justification.
- Do not mark “missing tests” without naming exact uncovered behavior.
- If no issues in a layer, explicitly state “No findings”.

## Advanced features
- Deep review checklist: [CHECKLIST.md](assets/CHECKLIST.md)
- Output scaffold: [OUTPUT_TEMPLATE.md](assets/OUTPUT_TEMPLATE.md)

## Attribution
Based on "The Code Review Pyramid" by Gunnar Morling:
https://www.morling.dev/blog/the-code-review-pyramid/
