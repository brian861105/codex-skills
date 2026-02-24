---
name: go-idioms
description: Write, review, and refactor Go code using idiomatic Go practices and the repository's Go standards. Use when implementing Go features, fixing Go bugs, adding Go tests, or designing Go APIs in this codebase.
---

# Go Idioms

## Overview

Apply the repository's Go coding standards and idiomatic Go practices. Keep this file concise and load the reference for full guidance.

## Workflow

1. Confirm Go context
- Check `go.mod` for the Go version and module path.
- Match the existing package name in the target directory; never add a duplicate `package` line.

2. Follow Go standards
- Prefer clear, idiomatic Go and standard library solutions.
- Keep error handling consistent (wrap with context, return early).
- Keep exported docs and comments in English unless asked otherwise.
- For testing, readability, and conventions, read `references/go-standards.md`.

3. Reference
- Read `references/go-standards.md` for the full Go standards and project rules.
- For error handling patterns, use `$error-handling-go`.
