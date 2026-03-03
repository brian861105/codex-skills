---
name: error-handling-typescript
description: Thin wrapper for TypeScript error-handling guidance. Use when users ask specifically about TS error handling; source of truth lives in ts-code-style/references/error-handling.md.
---

# Error Handling (TypeScript)

This is a thin wrapper skill for focused error-handling tasks.

## Source of Truth

- Primary policy lives in:
  - `../ts-code-style/references/error-handling.md`

## How to Use with `$ts-code-style`

- Prefer `$ts-code-style` as the main entry point.
- When failure-semantic triggers are hit, apply the rules in `../ts-code-style/references/error-handling.md` (MUST).
- Use this skill directly when the user asks specifically about TypeScript error handling.

## Trigger Conditions (MUST)

- Add or modify `try/catch` logic.
- Add or modify `throw` logic or custom `Error` classes.
- Add or modify async failure branches (`reject`, `.catch`, `Promise.all` fail paths).
- Change error propagation contracts in boundary layers (`api`, `service`, `repository`, `adapter`).
