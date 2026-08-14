---
name: contract-first-gate
description: "Use when the user says 先討論, asks to discuss or compare approaches before implementation, or explicitly wants an interface or contract agreed first. Clarify observable behavior, compare material options, produce a concise contract, and wait for explicit approval before editing implementation code."
---

# Contract First Gate

Establish the decision and observable contract before implementation. Do not
turn this step into an implementation checklist.

## Workflow

1. Inspect existing behavior and relevant design documents with read-only tools
   when evidence is needed.
2. Clarify the goal, observable behavior, boundaries, invariants, and material
   unknowns.
3. Compare 2-3 feasible options only when a real design choice exists. Do not
   manufacture alternatives for a settled or mechanical decision.
4. Recommend one option and state the accepted tradeoff.
5. Produce a concise contract. Include only fields relevant to the decision.
6. Use pseudocode or a logic diagram only when sequence, state, or concurrency
   would otherwise remain ambiguous.
7. Ask: `Approve this contract and continue?`
8. Do not edit implementation or test code until the user explicitly approves.
   After approval:
   - use `contract-driven-tdd` for behavior-changing implementation;
   - use the normal implementation workflow for documentation-only or
     non-behavioral work.

## Feasibility Comparison

Use this only when alternatives materially differ.

Use this section before the contract:

```md
## Feasibility Comparison
### Option A - <name>
- Why it can work (Evidence):
- Pros:
- Cons:
- Risks:

### Option B - <name>
- Why it can work (Evidence):
- Pros:
- Cons:
- Risks:

## Recommendation
- Suggested Option:
- Reason:
- Tradeoff accepted:
```

Evidence can include: constraints match, prior system behavior, API contract fit, performance expectation, operational simplicity.

## Contract Requirements

Describe externally observable behavior, not the intended class or function
layout. Cover the applicable items:

- goal, scope, and non-goals;
- caller and owning boundary;
- inputs and outputs;
- typed outcomes or error categories;
- side effects and their ordering;
- state transitions and invariants;
- precedence, fallback, retry, or idempotency rules;
- compatibility constraints;
- unresolved questions.

Express acceptance as scenarios that can later become contract tests. Do not
add generic `Validation`, `Validation Plan`, visibility checklist, or
implementation-task sections.

Use this compact shape:

```md
## Requirement Summary
- Goal:
- Constraints:

## Feasibility Comparison
- Options with evidence, pros, cons, risks
- Recommendation

## Contract
- In Scope:
- Out of Scope:
- Boundary:
- Inputs / Outputs:
- Outcomes / Errors:
- Side Effects / Ordering:
- Invariants:
- Contract Scenarios:

## Plan Artifact (only if needed)
- Pseudocode or Logic Diagram:

## Risks and Open Questions
- Risk:
- Question:

## Approval Gate
Approve this contract and continue? (yes/no)
```

## Approval Signals

- `yes`
- `approved`
- `go implement`
- `開始實作`
- `可以寫 code`

If unclear, ask once: `Please confirm whether this contract is approved.`

## Resource

- Use [contract-template.md](references/contract-template.md).
