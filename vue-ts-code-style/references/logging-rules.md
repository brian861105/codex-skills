# Logging Rules (`/html`) - Core Must Rules

Source baseline: `/html/LOGGING_CONVENTION.md`.

## Rule LOG-001 (must): Log messages in English

- Intent: keep team-wide consistency and searchable logs.
- ESLint mapping:
  - no direct lint rule; enforce in review.
- Applies to: all `console.*` messages.

Bad:

```ts
console.log('[Report] 儲存成功', { caseId });
```

Good:

```ts
console.log('[Report] Case saved:', { caseId });
```

## Rule LOG-002 (must): Use `[Module]` prefix

- Intent: identify origin quickly in shared consoles.
- ESLint mapping:
  - no direct lint rule; enforce in review.
- Applies to: all logs.

Bad:

```ts
console.error('Failed to save case:', { caseId, error });
```

Good:

```ts
console.error('[Report] Failed to save case:', { caseId, error: error.message });
```

## Rule LOG-003 (must): Use structured payloads, no string concatenation

- Intent: improve machine parsing and debugging quality.
- ESLint mapping:
  - can be guarded by `no-restricted-syntax` policy in local lint config.
- Applies to: all logs with context values.

Bad:

```ts
console.log('[Report] Saved case ' + caseId + ' with title ' + title);
```

Good:

```ts
console.log('[Report] Case saved:', { caseId, title });
```

## Rule LOG-004 (must): Match action verb and status

- Intent: keep lifecycle logs coherent (`Loading/Loaded`, `Saving/Saved`, `Failed to ...`).
- ESLint mapping:
  - no direct lint rule; enforce with review checklist.
- Applies to: stateful operations.

Bad:

```ts
console.log('[Report] Updated case:', { caseId }); // actually starting operation
```

Good:

```ts
console.log('[Report] Updating case:', { caseId });
```

## Rule LOG-005 (must): Correct log level

- Intent: prevent alert fatigue and missing incidents.
- ESLint mapping:
  - `no-console` with allowed methods pattern (`log`, `warn`, `error`) if desired.
- Applies to: all logs.

Bad:

```ts
console.log('[Network] Failed to load cases:', { error: err.message });
```

Good:

```ts
console.error('[Network] Failed to load cases:', { error: err.message });
```

## Rule LOG-006 (must): Never log secrets or full sensitive payloads

- Intent: avoid accidental data leaks.
- ESLint mapping:
  - optionally via custom `no-restricted-properties` patterns.
- Applies to: auth, profile, and evidence flows.

Bad:

```ts
console.log('[Network] Request:', { token, requestBody });
```

Good:

```ts
console.log('[Network] Request started:', { endpoint, requestId });
```

## Rule LOG-007 (should): Avoid noisy logs inside tight loops

- Intent: keep runtime overhead and noise under control.
- ESLint mapping:
  - no direct lint rule; enforce in review.
- Applies to: iterations, high-frequency watchers, repeated updates.

Bad:

```ts
items.forEach(item => {
  console.log('[Report] Item checked:', { id: item.id });
});
```

Good:

```ts
console.log('[Report] Items checked:', { count: items.length });
```
