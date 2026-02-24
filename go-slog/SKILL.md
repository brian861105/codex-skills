---
name: go-slog
description: Implement and review structured logging in Go using the standard library log/slog package. Use when adding or refactoring logging in Go services, handlers, CLIs, or background jobs.
---

# Go Slog

## Overview

Use `log/slog` for structured logging in Go. Keep logging consistent, structured, and context-rich.

## Logging Guidelines

- Use `log/slog`; do not add other logging frameworks.
- Prefer structured fields over formatted strings.
- Pass `*slog.Logger` explicitly or attach it to `context.Context` and retrieve it at the call site.
- Use level-appropriate methods: `Debug`, `Info`, `Warn`, `Error`.
- Log errors with fields (e.g., `slog.Any("err", err)`) and include key context like `request_id`, `user_id`, or `component` when available.
- Avoid logging and returning the same error unless the boundary explicitly requires it.

Example patterns:

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
logger.Info("starting server", slog.String("addr", addr))

if err := doThing(ctx); err != nil {
	logger.Error("doThing failed", slog.Any("err", err), slog.String("component", "worker"))
	return fmt.Errorf("doThing: %w", err)
}
```
