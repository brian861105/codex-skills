# TypeScript Compiler Baseline (Framework-Agnostic)

Use this baseline to define minimum compiler safety across TypeScript projects.

## Required (`must`)

- `strict: true`
- `noImplicitOverride: true`
- `noUncheckedIndexedAccess: true`
- `exactOptionalPropertyTypes: true`
- `useUnknownInCatchVariables: true`

## Recommended (`should`)

- `noFallthroughCasesInSwitch: true`
- `noImplicitReturns: true`

## Baseline Example

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitOverride": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "useUnknownInCatchVariables": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true
  }
}
```

## Exception and Downgrade Policy

- Default policy is to keep all `must` options enabled.
- Temporary downgrade is allowed only when all conditions hold:
  - A concrete blocker is documented (dependency/tooling/framework constraint).
  - A follow-up task is recorded with owner and target date.
  - Reviewer note explicitly lists disabled options and risk impact.
- Silent downgrades are not allowed.

## Review Guidance

- If the project `tsconfig` is below this baseline, reviewer must log the gap and risk.
- If a change touches type boundaries, API contracts, or error handling, baseline compliance check is mandatory.
