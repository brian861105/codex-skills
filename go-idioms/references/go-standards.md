# Go Standards (Authoritative Summary)

## Overview

This reference consolidates guidance from Effective Go, Go Code Review Comments, the Uber Go Style Guide, and the Google Go Style Guide (Guide/Decisions/Best Practices). Effective Go is older and not updated for modern tooling and ecosystem changes, but its language-level idioms still matter. Prefer clarity and simplicity; optimize for readers and maintainers.

## Naming & Packages

- Use short, lowercase package names; avoid underscores and mixedCaps.
- Package names should describe what the package provides; avoid stutter (e.g., `bytes.Buffer`, `bufio.Reader`).
- Exported names are MixedCaps; unexported are mixedCaps.
- Avoid `Get` prefixes for getters; use `Owner()` not `GetOwner()`.
- Use MixedCaps for multiword identifiers; avoid underscores.
- Favor clear, consistent names over clever abbreviations; single-letter names only in tight scopes or conventional cases (e.g., `i`, `r`, `w`).

## Error Handling

- Return errors explicitly; do not use `panic` for normal error handling.
- Wrap with context using `%w` when propagating errors.
- Error strings should be lowercase and not end with punctuation.
- Avoid logging and returning the same error unless the boundary requires logging.
- Use sentinel or typed errors when callers need to branch on error kinds; check via `errors.Is`/`errors.As`.

## Concurrency

- Make goroutine lifetimes explicit; avoid goroutine leaks and “fire-and-forget” unless properly managed.
- Favor simple concurrency primitives; document exit conditions for goroutines.
- Use `sync.WaitGroup` or channels to coordinate goroutines and cleanup.
- Prefer unbuffered or size-1 channels unless you can justify a larger buffer.

## Formatting & Comments

- Always use `gofmt` (and `goimports` where applicable).
- Use line comments for most documentation; block comments sparingly.
- Doc comments should explain the “why” and usage intent; avoid restating the obvious.
- Keep comment line length readable on narrow screens; wrap long comments.
- Keep code straightforward; use whitespace and helper functions to improve readability.

## API Design

- Prefer small, focused interfaces; accept interfaces, return concrete types.
- Avoid embedding types in public structs if it exposes implementation details.
- Avoid `init()` for non-trivial setup; prefer explicit constructors and wiring.
- Exit/terminate only in `main`; library code should return errors instead.
- Avoid mutable globals; prefer dependency injection.

## Testing

- Use table-driven tests for multiple cases.
- Add runnable Examples for packages when helpful; examples double as documentation.
- Write tests with clear failure messages; keep tests close to the code they cover.

## Performance

- Preallocate slices/maps when size is known.
- Avoid repeated string/byte conversions in hot paths.
- Prefer `strconv` over `fmt` for numeric conversions in performance-sensitive code.
- Use `defer` for cleanup unless proven to be a bottleneck.

## Links

- Effective Go: https://go.dev/doc/effective_go
- Go Code Review Comments: https://go.dev/wiki/CodeReviewComments
- Uber Go Style Guide: https://github.com/uber-go/guide/blob/master/style.md
- Google Go Style Guide (Guide): https://google.github.io/styleguide/go/guide
- Google Go Style Decisions: https://google.github.io/styleguide/go/decisions
- Google Go Best Practices: https://google.github.io/styleguide/go/best-practices
