# TypeScript Rules (Framework-Agnostic)

Apply these rules to `.ts` and `.tsx` files, plus TypeScript blocks in framework files.
Naming rules TS-001 through TS-008 are aligned with [ts.dev style guide: Identifiers](https://ts.dev/style/#identifiers).
For runnable ESLint settings, use `references/eslint-mapping.md`.

## Rule TS-001 (must): Base naming format by symbol type

- Intent: keep symbols predictable across modules and frameworks.
- ESLint mapping:
  - `camelcase` (or `@typescript-eslint/naming-convention` when configured)
  - `new-cap`
- Applies to: variables, functions, classes, constants.

Bad:

```ts
const user_name = 'brian';
class userprofile {}
const maxRetry = 3;
```

Good:

```ts
const userName = 'brian';
class UserProfile {}
const MAX_RETRY_COUNT = 3;
```

## Rule TS-002 (must): Identifiers use ASCII letters/digits/`_`/`$` only

- Intent: keep naming portable and tooling-friendly.
- ESLint mapping:
  - `id-match` (project-configurable)
- Applies to: all identifiers.

Bad:

```ts
const 使用者名稱 = 'brian';
```

Good:

```ts
const userName = 'brian';
```

## Rule TS-003 (must): No `_` prefix/suffix and no standalone `_`

- Intent: avoid pseudo-privacy markers and ambiguous placeholder names.
- ESLint mapping:
  - `no-underscore-dangle`
  - `@typescript-eslint/naming-convention`
- Applies to: variables, params, methods, fields.

Bad:

```ts
const _name = 'brian';
function parse(_): void {}
```

Good:

```ts
const name = 'brian';
function parse(unusedInput: string): void {}
```

## Rule TS-004 (must): Treat abbreviations as words

- Intent: preserve readability in mixed acronym names.
- ESLint mapping:
  - review convention (`@typescript-eslint/naming-convention` policy)
- Applies to: all identifiers.

Bad:

```ts
function loadHTTPURL(): void {}
```

Good:

```ts
function loadHttpUrl(): void {}
```

## Rule TS-005 (should): Avoid `$` unless framework convention requires it

- Intent: keep naming neutral across frameworks and runtimes.
- ESLint mapping:
  - `id-denylist` / custom `id-match` policy (optional)
- Applies to: variables, properties, functions.

Bad:

```ts
const caseList$ = fetchCases();
```

Good:

```ts
const caseList = fetchCases();
```

## Rule TS-006 (must): Type parameters use `T` or UpperCamelCase

- Intent: make generic intent immediately clear.
- ESLint mapping:
  - `@typescript-eslint/naming-convention` for `typeParameter`
- Applies to: generic type parameters.

Bad:

```ts
function first<itemType>(items: itemType[]): itemType {
  return items[0];
}
```

Good:

```ts
function first<T>(items: T[]): T {
  return items[0];
}
```

## Rule TS-007 (must): Local aliases preserve source symbol format

- Intent: avoid introducing second naming dialects for the same concept.
- ESLint mapping:
  - review convention
- Applies to: destructured aliases and local symbol aliases.

Bad:

```ts
const { UserProfile: user_profile } = models;
```

Good:

```ts
const { UserProfile } = models;
```

## Rule TS-008 (must): Do not prefix interface names with `I`

- Intent: keep names semantic and avoid type-encoding noise.
- ESLint mapping:
  - `@typescript-eslint/naming-convention`
- Applies to: interfaces.

Bad:

```ts
interface IUserProfile {
  id: string;
}
```

Good:

```ts
interface UserProfile {
  id: string;
}
```

## Rule TS-009 (must): Prefer explicit type boundaries

- Intent: keep API and state boundaries self-documenting.
- ESLint mapping:
  - `@typescript-eslint/explicit-function-return-type` (public/shared boundaries)
  - `@typescript-eslint/no-explicit-any`
- Applies to: exported functions, shared helpers, services, stores.

Bad:

```ts
export const parsePayload = (raw: any) => {
  return JSON.parse(raw);
};
```

Good:

```ts
export const parsePayload = (raw: string): unknown => {
  return JSON.parse(raw);
};
```

## Rule TS-010 (must): Stable import ordering and type imports

- Intent: improve readability and reduce merge churn.
- ESLint mapping:
  - `import/order`
  - `@typescript-eslint/consistent-type-imports`
- Applies to: all TypeScript files.

Bad:

```ts
import { buildQuery } from '@/lib/query';
import type { QueryInput } from '@/types/query';
import { readFileSync } from 'node:fs';
```

Good:

```ts
import { readFileSync } from 'node:fs';

import { buildQuery } from '@/lib/query';
import type { QueryInput } from '@/types/query';
```

## Rule TS-011 (must): No floating promises

- Intent: prevent silent async failures.
- ESLint mapping:
  - `@typescript-eslint/no-floating-promises`
  - `@typescript-eslint/no-misused-promises`
- Applies to: event handlers, lifecycle logic, async helpers.

Bad:

```ts
const handleSave = () => {
  saveReport();
};
```

Good:

```ts
const handleSave = async (): Promise<void> => {
  await saveReport();
};
```

## Rule TS-012 (should): Use early return to reduce nesting

- Intent: keep branch logic readable and testable.
- ESLint mapping:
  - `max-depth`
  - `complexity`
- Applies to: service methods, composables/hooks, store actions.

Bad:

```ts
function getCaseTitle(data?: { valid?: boolean; title?: string }): string {
  if (data) {
    if (data.valid) {
      return data.title ?? '';
    }
  }
  return '';
}
```

Good:

```ts
function getCaseTitle(data?: { valid?: boolean; title?: string }): string {
  if (!data?.valid) return '';
  return data.title ?? '';
}
```

## Rule TS-013 (should): Use descriptive names, avoid unclear abbreviations

- Intent: improve readability for readers outside the immediate module.
- ESLint mapping:
  - no direct lint rule; enforce in review
- Applies to: variables, parameters, functions, and types.

Bad:

```ts
const usrCfg = getCfg();
```

Good:

```ts
const userConfig = getConfig();
```

## Rule TS-014 (must): Escalate to error-handling subrules on failure-semantic changes

- Intent: avoid missing error contract regressions when code introduces or changes failure behavior.
- ESLint mapping:
  - no single lint rule fully covers this; enforce as review policy with targeted lint support where available
  - supporting lint examples: `@typescript-eslint/no-floating-promises`, `no-throw-literal`, `no-empty`
- Source of truth:
  - `references/error-handling.md`
- Applies to:
  - Add or modify `try/catch` logic.
  - Add or modify `throw` logic or custom `Error` classes.
  - Add or modify async failure branches (`reject`, `.catch`, `Promise.all` fail paths).
  - Change error propagation contracts in boundary layers (`api`, `service`, `repository`, `adapter`).

Bad:

```ts
async function getUserProfile(id: string): Promise<UserProfile | null> {
  try {
    return await repo.loadUserProfile(id);
  } catch {
    return null; // swallows failure semantics and hides boundary contract
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
    // throw-first default for unexpected failures (see references/error-handling.md)
    throw new UserProfileLoadError(id, error);
  }
}
```
