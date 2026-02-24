---
name: error-handling-typescript
description: Apply TypeScript error handling patterns including custom errors, Result-style returns, and robust async error handling. Use when implementing TS features or reviewing error handling.
---

# Error Handling (TypeScript)

## Overview

Use explicit error types, avoid silent failures, and handle async errors with clear boundaries.

## Core Guidelines

- Throw typed/custom errors for meaningful failure modes.
- Avoid empty `catch` blocks and avoid logging + rethrowing unless the boundary requires it.
- Use Result-style returns for expected failures when appropriate.
- In async code, prefer `try/catch` around awaited operations with targeted handling.

## Patterns

1. Custom error classes
- Include `code`, `status`, and context fields when useful.

2. Result type pattern
- Return `{ ok: true, value }` or `{ ok: false, error }` for expected failures.

## Examples

```typescript
class NotFoundError extends Error {
  constructor(resource: string, id: string) {
    super(`${resource} not found`);
    this.name = "NotFoundError";
  }
}

async function getUser(id: string): Promise<User> {
  const user = await repo.findUser(id);
  if (!user) {
    throw new NotFoundError("User", id);
  }
  return user;
}
```

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

function parseJSON<T>(input: string): Result<T, SyntaxError> {
  try {
    return { ok: true, value: JSON.parse(input) as T };
  } catch (err) {
    return { ok: false, error: err as SyntaxError };
  }
}
```
