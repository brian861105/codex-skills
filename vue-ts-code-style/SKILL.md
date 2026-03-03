---
name: vue-ts-code-style
description: Vue-specific code style conventions for Vue 3.4+ in the /html workspace. Covers Vue SFC structure, Composition API patterns, Pinia usage, testing style, and logging conventions with lint mappings.
---

# Vue Code Style (`/html`)

This skill applies only to Vue code under `/html` in this repository.
For framework-agnostic TypeScript rules, combine with `$ts-code-style`.

## Baseline

- Framework: Vue 3.4+ with `<script setup lang="ts">`
- Linting: `eslint`, `@typescript-eslint`, `eslint-plugin-vue`
- Formatting: `prettier`
- Style source: `claude.md` and `LOGGING_CONVENTION.md`

## Category Map

1. Vue SFC and Composition API patterns
2. Pinia and reactivity boundaries
3. Logging conventions (must-level)
4. Testing style for Vitest + Vue Test Utils

## Apply Flow

1. Detect file type and runtime context:
   - `.vue` SFC -> Vue rules
   - Vue runtime behavior updates (store/watch/lifecycle) -> Vue rules first
   - Logging updates -> Logging rules are mandatory
   - Tests (`*.spec.ts`) -> Testing rules
2. If a recommendation is generic TypeScript (naming, imports, boundary typing, promise handling), use `$ts-code-style`.
3. If failure-semantic triggers are hit (`try/catch`, `throw`/custom `Error`, async failure branches, or boundary error-propagation contract changes), MUST apply `../ts-code-style/references/error-handling.md`.
4. Enforce `must` rules first, then `should`, then `prefer`.
5. For every recommendation, cite:
   - Rule ID
   - Intent
   - Lint mapping
   - A minimal bad/good example

## Rule Priority

- `must`: Required for consistency and safety in `/html`.
- `should`: Strong recommendation; deviate only with explicit rationale.
- `prefer`: Optimization for readability/maintainability.

## Review Checklist

- Scope check: change is inside `/html` Vue+TS code.
- Vue SFC keeps predictable setup order and typed `props`/`emits`.
- Pinia state reactivity is preserved (`storeToRefs` when destructuring state).
- Logging is English, structured, module-prefixed, and level-correct.
- Tests follow clear naming and AAA structure with async/error branches covered.
- Failure-semantic trigger changes in Vue TS code explicitly apply `../ts-code-style/references/error-handling.md`.

## References

- Vue rules: `references/vue-rules.md`
- Logging rules: `references/logging-rules.md`
- Testing rules: `references/testing-rules.md`
