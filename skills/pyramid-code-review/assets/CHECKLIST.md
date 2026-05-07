# Pyramid Code Review Checklist

Attribution: Adapted from "The Code Review Pyramid" by Gunnar Morling — https://www.morling.dev/blog/the-code-review-pyramid/

## API Semantics
- Is API as small as possible, as large as needed?
- Is there one way of doing one thing, not multiple ones?
- Is it consistent and following principle of least surprise?
- Clean split of API/internals, without internals leaking into API?
- Any breaking changes to user-facing parts (API classes, config, metrics, log formats)?
- Is a new API generally useful and not overly specific?

## Implementation Semantics
- Does it satisfy original requirements?
- Is it logically correct?
- Is unnecessary complexity avoided?
- Is it robust (concurrency, error handling, retries/timeouts)?
- Is it performant enough?
- Is it secure (e.g. injection, authz/authn, secret handling)?
- Is it observable (metrics, logging, tracing)?
- Do new dependencies pull their weight? Is license acceptable?

## Documentation
- Are new features reasonably documented?
- Are right doc types covered (README, API docs, user guide, reference docs)?
- Are docs understandable and free of major typos/grammar issues?

## Tests
- Are all tests passing?
- Are new features reasonably tested?
- Are corner cases tested?
- Are unit tests used where possible and integration tests where needed?
- Are NFR tests covered where relevant (e.g. performance)?

## Code Style
- Is project formatting style applied?
- Does naming follow conventions?
- Is it DRY?
- Is code readable (method/function length, structure, intent)?

## Priority guidance
- Focus review effort first on API + implementation semantics.
- Documentation and tests next.
- Code style last; automate via linters/formatters where possible.
