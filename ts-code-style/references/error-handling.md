# Error Handling Rules (TypeScript, Framework-Agnostic)

This is the source of truth for TypeScript error-handling policy in this repository.

## Scope

Apply these rules when change scope includes any of the following:

- Add or modify `try/catch` logic.
- Add or modify `throw` logic or custom `Error` classes.
- Add or modify async failure branches (`reject`, `.catch`, `Promise.all` fail paths).
- Change error propagation contracts in boundary layers (`api`, `service`, `repository`, `adapter`).

## Default Decision Policy

- Unexpected failures: `throw` (default, including boundary layers).
- Expected business failures: `Result` is allowed only when the failure is explicit and part of the contract.
- Never use empty `catch`.
- Avoid log + rethrow duplication unless the boundary requires one-time contextual logging.

## Conflict Resolution with TS Style Rules

- Naming/import/typing/style concerns are owned by `ts-rules.md`.
- Failure semantics, error taxonomy, and propagation contracts are owned by this document.

## Patterns

1. Custom error classes
- Include context fields when useful.

2. Result pattern for expected failures
- Return `{ ok: true, value }` or `{ ok: false, error }`.

## Examples

Bad:

```ts
async function getUserProfile(id: string): Promise<UserProfile | null> {
  try {
    return await repo.loadUserProfile(id);
  } catch {
    return null; // swallows failure semantics
  }
}
```

Good:

```ts
class UserProfileLoadError extends Error {
  constructor(public readonly userId: string, public readonly detail: unknown) {
    super('failed to load user profile');
    this.name = 'UserProfileLoadError';
  }
}

async function getUserProfile(id: string): Promise<UserProfile> {
  try {
    return await repo.loadUserProfile(id);
  } catch (error) {
    throw new UserProfileLoadError(id, error); // throw-first default for unexpected failures
  }
}
```

Result example (expected failure):

```ts
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

function parseJSON<T>(input: string): Result<T, SyntaxError> {
  try {
    return { ok: true, value: JSON.parse(input) as T };
  } catch (err) {
    return { ok: false, error: err as SyntaxError };
  }
}
```
