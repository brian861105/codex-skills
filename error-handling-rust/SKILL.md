---
name: error-handling-rust
description: Apply Rust error handling patterns using Result/Option, thiserror for libraries, anyhow for applications, and contextual error propagation. Use when implementing Rust features or reviewing error handling.
---

# Error Handling (Rust)

## Overview

Use `Result`/`Option` explicitly, propagate with `?`, and choose `thiserror` for libraries and `anyhow` for applications.

## Core Guidelines

- Prefer `Result<T, E>` over panics in production paths.
- Use `?` to propagate errors and attach context where it helps debugging.
- Use `thiserror` for typed errors in libraries.
- Use `anyhow` for application-level errors and ergonomics.
- Avoid `unwrap()`/`expect()` outside of tests or truly unreachable code.

## Patterns

1. Typed errors (libraries)
- Define enum error types and derive `thiserror::Error`.
- Convert underlying errors with `#[from]`.

2. Context propagation (apps)
- Use `anyhow::Context` for readable failure chains.

## Examples

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
    #[error("parse error: {0}")]
    Parse(#[from] std::num::ParseIntError),
}

fn read_number(path: &str) -> Result<i32, AppError> {
    let contents = std::fs::read_to_string(path)?;
    let number = contents.trim().parse()?;
    Ok(number)
}
```

```rust
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<String> {
    std::fs::read_to_string(path).context("read config file")
}
```
