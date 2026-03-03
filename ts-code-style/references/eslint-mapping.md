# ESLint Mapping (Executable)

Use this file to map `ts-code-style` rules to runnable ESLint config.

## Rule Severity Map

- TS-001: `@typescript-eslint/naming-convention` -> `error`
- TS-002: `id-match` -> `error`
- TS-003: `no-underscore-dangle` -> `error`
- TS-004: `@typescript-eslint/naming-convention` (acronym policy) -> `warn`
- TS-005: `id-denylist` (or `id-match` custom policy) -> `warn`
- TS-006: `@typescript-eslint/naming-convention` (`typeParameter`) -> `error`
- TS-007: no direct lint coverage -> `review gate`
- TS-008: `@typescript-eslint/naming-convention` (interface no `I` prefix) -> `error`
- TS-009: `@typescript-eslint/explicit-function-return-type` + `@typescript-eslint/no-explicit-any` -> `error`
- TS-010: `import/order` + `@typescript-eslint/consistent-type-imports` -> `error`
- TS-011: `@typescript-eslint/no-floating-promises` + `@typescript-eslint/no-misused-promises` -> `error`
- TS-012: `max-depth` + `complexity` -> `warn`
- TS-013: no direct lint coverage -> `review gate`
- TS-014: `no-empty` + `no-throw-literal` + review gate against `references/error-handling.md` -> `error/review`

## Flat Config Example (`eslint.config.js`)

```js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import importPlugin from "eslint-plugin-import";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    files: ["**/*.{ts,tsx}"],
    plugins: {
      import: importPlugin,
    },
    languageOptions: {
      parserOptions: {
        projectService: true,
      },
    },
    rules: {
      "@typescript-eslint/naming-convention": [
        "error",
        { selector: "default", format: ["camelCase"] },
        { selector: "variable", format: ["camelCase", "UPPER_CASE", "PascalCase"] },
        { selector: "typeLike", format: ["PascalCase"] },
        { selector: "typeParameter", format: ["PascalCase"], prefix: ["T"] },
        { selector: "interface", format: ["PascalCase"], custom: { regex: "^I[A-Z]", match: false } }
      ],
      "id-match": ["error", "^[A-Za-z_$][A-Za-z0-9_$]*$"],
      "no-underscore-dangle": ["error", { allowAfterThis: false, allowAfterSuper: false }],
      "@typescript-eslint/explicit-function-return-type": [
        "error",
        { allowExpressions: true, allowTypedFunctionExpressions: true }
      ],
      "@typescript-eslint/no-explicit-any": "error",
      "import/order": ["error", { "newlines-between": "always" }],
      "@typescript-eslint/consistent-type-imports": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "max-depth": ["warn", 3],
      "complexity": ["warn", 12],
      "no-empty": ["error", { allowEmptyCatch: false }],
      "no-throw-literal": "error"
    }
  }
];
```

## Legacy Config Example (`.eslintrc.cjs`)

```js
module.exports = {
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: true
  },
  plugins: ["@typescript-eslint", "import"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended-type-checked"
  ],
  rules: {
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/no-misused-promises": "error",
    "@typescript-eslint/consistent-type-imports": "error",
    "import/order": ["error", { "newlines-between": "always" }],
    "no-empty": ["error", { allowEmptyCatch: false }],
    "no-throw-literal": "error"
  }
};
```

## Notes

- TS-007 and TS-013 still need review checks.
- TS-014 requires review policy enforcement in addition to lint rules.
