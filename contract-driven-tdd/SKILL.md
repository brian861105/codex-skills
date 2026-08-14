---
name: contract-driven-tdd
description: Use when implementing or changing an application port, cross-module contract, public API behavior, state machine, persistence or fallback policy, provider adapter, recovery/finalization workflow, or shared data model. Start from an approved design contract, turn its scenarios into fake-backed executable tests before production implementation, and deliver one observable vertical slice at a time. Also use when the user explicitly requests Contract-Driven TDD, contract tests, SDD-to-TDD implementation, or agent-friendly contract-first development.
---

# Contract-Driven TDD

Implement observable contracts without making tests mirror internal structure.

## Preconditions

1. Read repository instructions and locate the relevant contract using the
   repository's existing design-document, ADR, RFC, issue, or specification
   convention. Use `docs/designs` only when no convention exists.
2. Check that the selected artifact defines the boundary, inputs, outputs, typed outcomes, side
   effects, ordering, invariants, and concrete scenarios that apply.
3. Check its status and adoption gap against current code.
4. If the contract is missing or ambiguous, use `design-first-development`
   before editing production code.
5. If the user asked to discuss first or a material decision remains, use
   `contract-first-gate` and wait for approval.

Do not treat an implementation checklist, validation plan, historical code
description, or existing test suite as the contract.

## Workflow

### 1. Select One Vertical Slice

Choose the smallest goal-aligned behavior that crosses the real application
boundary and exercises the contract's highest current risk. Determine risk from:

- the contract goal and primary failure mode;
- the adoption gap in current code;
- data loss, incorrect state, unavailable reads, or irreversible side effects;
- uncertainty at a boundary shared by multiple adapters or callers.

Do not select a slice merely because it is scenario 1, easiest to implement,
closest to an existing file, or limited to input validation. An input-validation
slice is first only when invalid input is a primary contract risk and belongs to
that boundary.

State:

- the contract scenario;
- why it is the highest-value current risk;
- the port or public boundary under test;
- the observable result and side effects;
- what remains outside this slice.

Do not split a slice by repository file or internal helper unless that is itself
the contract boundary.

When several slices are similarly small, prefer the one that proves the
contract's central value. For example, a fallback store whose goal is continued
reads during cache failure should first prove `cache failure + durable hit`,
not malformed-key rejection.

### 2. Build the Contract Harness

Test through the contract-facing interface. Prefer:

- in-memory fakes for external stores, providers, clocks, and queues;
- recorded calls when ordering or suppression is observable;
- deterministic inputs and outcomes;
- typed values and errors rather than serialized implementation details.

Use a reusable contract suite when multiple adapters implement the same port.
Each adapter may also have narrow integration tests for serialization, SQL,
Redis, or provider mapping.

Do not require a live database, Redis, network service, or timing race to prove
application behavior when a fake can express the contract.

### 3. Establish Red

Write the scenario test before changing production implementation. Run the
narrowest relevant test command and confirm that it fails for the missing
behavior.

The failure must demonstrate the contract gap, not a broken fixture, compiler
typo, or unavailable external service.

For behavior that already exists:

- first add a passing characterization only when coverage is missing;
- then add a failing scenario for the requested behavioral delta.

If no meaningful failing scenario can be produced, explain why before editing
production code. Do not create a fake failure merely to claim TDD.

### 4. Implement the Minimum Behavior

Change only enough production code to satisfy the selected scenario while
preserving established contracts. Keep provider, database, Redis, and transport
details behind the application port.

Run the focused scenario until green. Then run nearby contract and adapter tests
in proportion to the affected boundary. Follow repository-specific test
instructions; avoid blanket suites when they require unavailable infrastructure.

### 5. Refactor Without Changing the Contract

Remove duplication and improve names only after green. Use
`test-scope-hygiene` when test names or assertions cover more than one behavior.

Do not encode private call graphs, helper names, or struct layout into contract
tests unless those details are explicitly public behavior.

### 6. Close the Slice

Before reporting completion:

- map every changed behavior to an approved scenario;
- verify expected side effects, ordering, and negative behavior;
- confirm errors retain the categories required by the contract;
- update the contract status or adoption gap when implementation coverage
  materially changed;
- remove stale prose that describes superseded behavior.

Report the scenario implemented, focused tests run, and remaining adoption gaps.
Do not add generic `Validation`, `Validation Plan`, or review-checklist sections
to design documents.

## Scenario Style

Write scenarios as observable cause and effect:

```text
Given <boundary state and dependency outcomes>
When <caller invokes the contract>
Then <returned outcome>
And <observable side effects or calls>
And <forbidden side effects do not occur>
```

Cover only behavior relevant to the change. Typical contract dimensions are:

- success, absence, and typed failure;
- fallback and precedence;
- partial success;
- retry and idempotency;
- state transition and terminal-state protection;
- concurrency generation or stale-result rejection;
- call ordering and suppressed calls.

Do not create tests for every dimension when the contract does not require it.

## Agent Handoff

When delegating implementation, give the agent:

- the approved contract path;
- the selected scenarios;
- the contract-facing port;
- the focused test command;
- explicit scope and non-goals.

Ask the agent to return evidence of red, green, and any contract ambiguity. Do
not ask it to infer product behavior from existing implementation alone.
