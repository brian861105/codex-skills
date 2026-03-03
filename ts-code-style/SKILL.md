---
name: ts-code-style
description: Framework-agnostic TypeScript code style conventions. Covers naming, type boundaries, imports, async safety, and review checkpoints. Use when writing, reviewing, or refactoring TypeScript code across frameworks.
---

# TypeScript Code Style

This skill is framework-agnostic and can be applied to TypeScript codebases across Vue, React, Angular, and Node services.

## Baseline

- Language: TypeScript-first authoring
- Linting: `eslint`, `@typescript-eslint`
- Formatting: `prettier`
- Naming source: `ts.dev/style/#identifiers`
- Executable lint mapping: `references/eslint-mapping.md`

## TypeScript Compiler Baseline

- Use `references/tsconfig-baseline.md` as the minimum compiler safety baseline.
- `must` compiler options are required unless a documented exception is approved.

## Category Map

1. Naming and symbol conventions
2. Explicit type boundaries
3. Import and type import consistency
4. Async safety and promise handling

## Apply Flow

1. Detect TypeScript scope:
   - `.ts`, `.tsx`, shared helpers, composables/hooks, stores/services
2. If a change touches type safety, API boundaries, or error behavior, check `references/tsconfig-baseline.md`.
3. If lint setup or rule enforcement is in scope, apply `references/eslint-mapping.md`.
4. Enforce `must` rules first, then `should`, then `prefer`.
5. For every recommendation, cite:
   - Rule ID
   - Intent
   - Lint mapping
   - A minimal bad/good example
6. If any failure-semantic trigger is hit, MUST apply `references/error-handling.md`.

## Error-handling Integration Contract

- MUST apply `references/error-handling.md` when change scope includes any trigger from `Integration Triggers (MUST)`.
- If no trigger is hit, `$ts-code-style` can be used alone.
- Review gate: missing `references/error-handling.md` application on triggered changes is a policy violation.
- Optional shortcut: `$error-handling-typescript` is allowed as a thin wrapper, but rule source remains `references/error-handling.md`.

## Integration Triggers (MUST)

- Add or modify `try/catch` logic.
- Add or modify `throw` logic or custom `Error` classes.
- Add or modify async failure branches (`reject`, `.catch`, `Promise.all` fail paths).
- Change error propagation contracts in boundary layers (`api`, `service`, `repository`, `adapter`).

## Exception Policy

- Default is zero exceptions for MUST integration triggers.
- Exception is allowed only when all conditions hold:
  - Change is strictly non-behavioral (rename, reorder, comment, type-only annotation) with no runtime failure-path change.
  - Reviewer records rationale explicitly in the review note.
  - Follow-up task exists when deferred failure-semantics cleanup is required.
- Verbal-only waiver is not accepted.

## Rule Priority

- `must`: Required for consistency and safety.
- `should`: Strong recommendation; deviate only with explicit rationale.
- `prefer`: Optimization for readability and maintainability.

## Review Checklist

- Naming follows camelCase/PascalCase/UPPER_SNAKE_CASE conventions.
- Naming follows ts.dev identifier rules (`_` usage, `$` usage, abbreviation casing, generic type parameter naming, no `I` prefix for interfaces).
- Public/shared functions and boundaries use explicit return and input types.
- Imports are stable and type imports are explicit.
- Async paths do not leave floating promises.
- Failure-semantic triggers are checked; if hit, `references/error-handling.md` is explicitly applied.
- Compiler baseline in `references/tsconfig-baseline.md` is checked; if current project is below baseline, risk is recorded in review notes.
- Control flow avoids unnecessary nesting and keeps branches testable.

## References

- TypeScript rules: `references/ts-rules.md`
- Error handling rules: `references/error-handling.md`
- TypeScript compiler baseline: `references/tsconfig-baseline.md`
- ESLint executable mapping: `references/eslint-mapping.md`
