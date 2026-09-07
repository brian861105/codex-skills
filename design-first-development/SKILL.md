---
name: design-first-development
description: Agree on observable behavior when the user asks to discuss first, or record a contract for high-risk and cross-boundary changes. Skip ordinary local changes with an established contract.
---

# Design-First Development

Use for public or cross-module APIs, state machines, recovery/concurrency,
persistence/fallback policies, shared provider mappings, migrations, and
architecture with material compatibility or operational risk. Ordinary local
features, behavior-preserving refactors, narrow fixes, and reviews need no new
design artifact unless they expose an unresolved material decision.

## Discussion and Approval

When the user says 先討論 or explicitly asks to agree before implementation:

- Inspect relevant code and existing decisions with read-only tools.
- Compare feasible options only when they materially differ. Recommend one and
  explain the accepted tradeoff; do not manufacture alternatives.
- State the observable contract and any unresolved decision concisely.
- Wait for explicit approval before editing implementation or tests. An earlier
  approval covering the same scope remains valid; do not ask again.

For an implementation request, proceed when behavior is clear and remaining
assumptions are conservative. Ask only about unresolved decisions whose answers
materially affect the result or require an unauthorized, irreversible action.
Touching deployment, compatibility, security, or cost does not by itself require
another approval. Continue independent authorized work while awaiting input.

## Record the Contract

Reuse the repository's issue, ADR, RFC, or specification when it already covers
the decision. Otherwise use its existing design location, falling back to
`docs/designs`. Record material decisions before production implementation;
avoid duplicate documents or a new artifact for discussion that changes nothing.

Include only applicable information:

- Goal, scope, caller, and owning boundary.
- Inputs, outputs, typed outcomes, side effects, and ordering.
- Invariants, state transitions, precedence, fallback, retry, and idempotency.
- Compatibility or migration constraints.
- Observable scenarios with unambiguous pass/fail outcomes.
- Status (target, adopted, partially adopted, superseded) and adoption gaps.

Describe behavior rather than internal classes or file layout. Use pseudocode
or a diagram only when it resolves sequence, state, or concurrency ambiguity.
Scenarios replace generic validation checklists. Update only changed decisions.

After approval where required, use `contract-driven-tdd` for behavior-changing
implementation at these boundaries. Documentation-only and non-behavioral work
can use the normal workflow.
