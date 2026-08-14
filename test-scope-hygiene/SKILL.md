---
name: test-scope-hygiene
description: Review, write, or refactor automated tests so each test name matches exactly the behavior being verified. Use when inspecting tests, fixing misleading names, splitting over-broad tests, reducing unrelated assertions, or improving unit-test clarity. This skill checks individual test hygiene; use contract-driven-tdd to derive a behavior-changing implementation suite from an approved contract.
---

# Test Scope Hygiene

## Overview

Keep each test focused on the behavior promised by its name. Treat mismatches between the test name, setup, action, and assertions as a review finding or refactor target.

Do not use this skill to invent product behavior or replace an approved
contract. When a contract exists, preserve its named scenarios while improving
each test's local clarity.

## Workflow

1. Identify the behavior promised by the test name.
2. Classify every assertion as primary, supporting, or unrelated.
3. Keep primary assertions in the current test.
4. Keep supporting assertions only when they are necessary to prove the named behavior and cannot hide a separate behavior.
5. Move unrelated assertions into separate tests with precise names.
6. Rename a test only when the existing body already has one coherent broader purpose.
7. Prefer splitting over broadening when a test verifies multiple independently useful behaviors.

## Assertion Scope

Use this rule of thumb:

- Primary: directly proves the behavior named by the test.
- Supporting: verifies required preconditions or disambiguates the result.
- Unrelated: verifies a different behavior, even if the same fixture makes it easy to assert.

Flag these patterns:

- Test name says one thing, but assertions cover payload type, terminal status, aliases, and finalization together.
- One receiver, iterator, or stream is consumed multiple times while the test claims each downstream subscriber receives one message.
- Constructor metadata tests also assert deep payload inspection.
- Negative assertions are copied from nearby tests but do not clarify the named behavior.
- A fixture contains multiple signals, causing the test to pass for the wrong reason.

## Refactor Guidance

When fixing tests:

- First choose whether the test should be renamed or split.
- Use one concept per test name.
- Make fixtures minimal for the named behavior.
- Store a received value once, then assert multiple fields on that value.
- Avoid asserting every field just because it is available.
- Preserve important coverage by moving assertions to new tests, not deleting them silently.
- Name new tests after the behavior, not the implementation path.

## Example

For a test named:

```rust
fn test_sportradar_message_inspects_event_and_terminal_status()
```

These are aligned:

```rust
assert!(message.inspection.has_event_payload);
assert!(message.inspection.is_terminal_game_status);
```

These probably deserve separate tests unless the name is broadened deliberately:

```rust
assert!(!message.inspection.has_statistics_payload);
assert!(message.inspection.is_finalization_game_status);
assert!(message.inspection.statistics_game_aliases.is_empty());
```

Possible split:

```rust
fn test_sportradar_event_message_detects_event_payload()
fn test_sportradar_complete_status_is_terminal()
fn test_sportradar_complete_status_is_finalization_status()
fn test_sportradar_event_message_does_not_collect_statistics_aliases()
```

Do not keep all of those assertions in one test unless the test is explicitly a broad integration-style inspection test and the name says so.

## Output Style

When reviewing, report findings with the test name, the mismatched assertions, and the recommended split or rename. When editing, keep behavior-preserving coverage unless the user explicitly asks to remove redundant checks.
