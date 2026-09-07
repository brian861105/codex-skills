---
name: contract-driven-tdd
description: Implement contract scenarios with deterministic tests before production changes at public or cross-module APIs, state machines, persistence policies, provider adapters, and shared models. Also use when explicitly requested.
---

# Contract-Driven TDD

## Establish the Boundary

Locate the current contract using repository conventions. It must define the
relevant inputs, outcomes, side effects, invariants, and observable scenarios.
Check its adoption gap against the code. If missing or ambiguous, use
`design-first-development`; it also handles discussion-first approval. Do not
require fresh approval for decisions already settled in the task.

An implementation checklist, historical code description, or existing test
suite alone does not establish the desired contract.

## Implement a Slice

1. Select the smallest observable slice covering the contract's highest current
   risk. For a fallback store intended to survive cache failure, prove
   `cache failure + durable hit` before incidental input validation. Do not split
   work by internal files or helpers unless they are the public boundary.
2. Test through the contract-facing interface using deterministic inputs and
   in-memory fakes for external stores, providers, clocks, and queues where they
   can express the behavior. Record calls only when ordering or suppression is
   observable. Reuse a contract suite across adapters implementing the same port;
   retain focused integration coverage for real SQL, serialization, or mapping.
3. Write and run the scenario before changing production code. Confirm that red
   demonstrates the missing behavior, rather than a broken fixture, compiler
   typo, or unavailable service. For existing behavior, add characterization only
   where coverage is missing, then test the requested delta. If no meaningful
   failing scenario exists, explain why; never manufacture a failure.
4. Implement the minimum behavior, keep infrastructure details behind the port,
   and run the focused test until green. Refactor while preserving the contract.
5. Continue the authorized slices until the requested outcome is complete.

Follow the repository's test execution and merge-gate policy as the single
source of truth. Without a repository policy, use the smallest relevant tests
and broaden only for an affected boundary or unresolved risk. Fake-backed tests
do not replace verification of SQL or another real adapter when that is changed.

## Scenario and Test Quality

Write scenarios as cause and effect: given boundary state and dependency
outcomes, when the caller invokes the contract, then assert the result and
required or forbidden side effects. Cover only dimensions relevant to this
change, such as absence/failure, partial success, retries, idempotency, stale
results, terminal-state protection, or call ordering.

Keep test names, fixtures, and assertions aligned with the named behavior. Avoid
private call-graph or layout assertions unless they are public behavior. Follow
the user's general test-quality rules when refining fixtures and assertions.

## Close the Work

Map changed behavior to the settled scenarios, verify required side effects and
error categories, and update status/adoption gaps when materially changed.
Report focused test evidence and remaining gaps without adding generic
validation sections to design documents.

If delegating implementation, provide the contract path, selected scenarios,
public boundary, focused test command, and scope. Request red/green evidence and
any unresolved contract ambiguity; delegation itself is not required here.
