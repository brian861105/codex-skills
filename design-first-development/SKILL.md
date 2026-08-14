---
name: design-first-development
description: Use before high-risk or cross-boundary behavior changes such as new or changed public APIs, state machines, persistence or fallback policies, provider mappings, shared data models, migrations, or architecture changes. Establish or verify a concise observable design contract in the repository's existing design location, falling back to docs/designs, before production code; then use contract-driven-tdd. Do not trigger for ordinary local features, contained behavior changes, refactors, or narrow bug fixes unless material ambiguity or irreversible risk appears.
---

# Design-First Development

Establish an observable contract before high-risk or cross-boundary implementation.
Do not impose a design-document gate on ordinary local changes.

## Apply the Gate

Use this skill when a change affects one or more of these areas:

- a public or cross-module API;
- a state machine, recovery, finalization, or concurrency workflow;
- persistence, fallback, retry, idempotency, or precedence policy;
- provider mapping or an adapter contract shared by multiple callers;
- a shared data model, schema migration, or compatibility boundary;
- architecture with material operational, safety, or rollback risk.

Also apply it when a smaller request exposes unresolved product behavior or a
decision that cannot be reversed safely.

Do not normally use it for:

- contained behavior changes with an obvious contract;
- narrow bug fixes that restore established behavior;
- internal refactors that preserve observable behavior;
- typo, formatting, documentation, investigation, or review tasks;
- small features whose acceptance behavior is already explicit and local.

## Locate the Contract

1. Read repository instructions and follow an existing convention for design
   documents, ADRs, RFCs, or specifications.
2. Reuse a current issue, ADR, RFC, or spec when it already contains the
   required observable contract. Do not create a duplicate document solely to
   satisfy this skill.
3. When the repository has no convention, use `docs/designs`.
4. Check the target contract against the quality gate below and correct only
   the sections needed for the requested change.

Conversation may settle a decision, but material decisions must be recorded in
the selected repository artifact before production implementation begins.

## Resolve Missing or Ambiguous Design

When no adequate contract exists:

1. Inspect current behavior and relevant constraints with read-only tools.
2. Use `contract-first-gate` and wait for approval when the user asks to discuss
   first or when material alternatives remain.
3. Otherwise, create a concise contract in the repository's design location and
   continue in the same turn when the implementation request is clear and all
   remaining assumptions are conservative and recorded.
4. Stop for direction when the decision affects data safety, compatibility,
   deployment, security, cost, or another irreversible boundary.
5. After the contract is current, use `contract-driven-tdd` for the scoped
   implementation.

## Contract Quality Gate

Include only applicable items:

- status: target, adopted, partially adopted, or superseded;
- goal, scope, and non-goals;
- caller and owning boundary;
- inputs, outputs, and typed outcomes or error categories;
- observable side effects and ordering;
- state transitions and invariants;
- precedence, fallback, retry, and idempotency rules;
- compatibility or migration constraints;
- concrete scenarios that can become contract tests;
- differences between the target contract and current implementation.

Reject or correct a contract when its observable outcomes remain ambiguous, its
scenarios cannot determine pass or fail, or it mainly documents internal class,
function, or file layout.

Prefer this concise shape:

```md
# <Feature or Boundary>

Status: <target/adopted/partially adopted/superseded>

## Goal
## Scope and Non-Goals
## Contract
## Invariants
## Scenarios
## Adoption Gap
```

Omit empty sections. Scenarios replace generic validation plans and checklists.

## Approval Gate

Do not require separate approval merely because a design artifact was created
or updated. Require explicit approval only when the user asked to discuss or
design first, material decisions remain unresolved, or the change requires a
risky assumption.
