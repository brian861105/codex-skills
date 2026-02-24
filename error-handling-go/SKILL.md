---
name: error-handling-go
description: Apply Go-specific error handling patterns including wrapping, sentinel errors, errors.Is/As checks, and consistent error messages. Use when implementing Go features, designing Go APIs, or reviewing Go error handling.
---

# Error Handling (Go)

## Overview

Use explicit error returns, wrap with context, and keep messages consistent. Prefer typed/sentinel errors for comparisons and `errors.Is/As` for checks.

## Core Guidelines

- Return errors explicitly and handle them immediately.
- Wrap with context using `fmt.Errorf("...: %w", err)`.
- Use `errors.Is` for sentinel errors and `errors.As` for typed errors.
- Keep error messages lowercase and without trailing punctuation.
- Avoid logging and returning the same error unless the boundary explicitly requires logging.
- Prefer standard library patterns over custom error frameworks.

## Patterns

1. Sentinel errors
- Define package-level sentinel errors for common conditions.
- Compare with `errors.Is` instead of direct equality if wrapping is involved.

2. Typed errors
- Use struct error types when callers need structured data.
- Check with `errors.As`.

3. Context propagation
- Add context at each layer boundary and preserve the original error.

## Examples

```go
var (
	ErrNotFound = errors.New("not found")
)

func loadUser(id string) (*User, error) {
	user, err := db.QueryUser(id)
	if err != nil {
		return nil, fmt.Errorf("query user: %w", err)
	}
	if user == nil {
		return nil, ErrNotFound
	}
	return user, nil
}

func handle(id string) error {
	_, err := loadUser(id)
	if err != nil {
		if errors.Is(err, ErrNotFound) {
			return err
		}
		return fmt.Errorf("handle user: %w", err)
	}
	return nil
}
```
