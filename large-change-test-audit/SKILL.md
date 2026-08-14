---
name: large-change-test-audit
description: Run an independent subagent audit of unit-test changes when an implementation exceeds its applicable changed-line threshold. Resolve the threshold from an explicit user instruction, then repository instructions, then a default of 1,000 additions plus deletions. Use for large features, refactors, migrations, or other broad code changes; exclude clearly mechanical generated, vendored, and lock-file updates. Verify that every added or modified unit test is necessary, relevant, non-redundant, and behavior-focused. If an independent reviewer is unavailable, require an explicit user waiver before continuing with a clearly labeled self-audit.
---

# Large Change Test Audit

Apply an independent unit-test review gate to large changes. Keep implementation
ownership with the main agent; use the reviewer only to audit test scope and
necessity.

## Resolve and Measure the Threshold

1. Resolve the changed-line threshold in this order:
   - an explicit threshold from the user for the current task;
   - a threshold in repository instructions;
   - the default threshold of 1,000 lines.
2. Measure the current in-scope diff using additions plus deletions.
3. Exclude generated files, vendored code, and lock files only when their
   changes are clearly mechanical. Record every exclusion.
4. Trigger the gate when the measured total is greater than the resolved
   threshold or when the planned implementation is reasonably expected to
   cross it.

Do not raise the threshold after inspecting the diff merely to avoid review.
If the change crosses the threshold unexpectedly, stop further implementation
and run the audit immediately.

## Run an Independent Audit

Spawn at least one read-only subagent before continuing the large change. Give
the reviewer raw task artifacts rather than the main agent's conclusions:

- the user's request and any approved design or contract;
- the resolved threshold, its source, the diff summary, and exclusions;
- the relevant production-code diff;
- all added or modified unit tests and nearby existing tests;
- focused test output when available.

Ask for an evidence-based audit that:

1. Classifies every added or modified unit test as keep, remove, split, or
   rewrite.
2. Verifies that each test covers behavior required by the task or a credible
   regression.
3. Identifies duplicate coverage, unrelated assertions,
   implementation-detail coupling, and tests that can pass without proving
   their stated behavior.
4. Identifies required unit-test coverage that is missing.
5. Cites exact files and lines and explains each recommendation.

If no unit tests changed, ask whether that omission is justified and which
focused tests, if any, are required.

## Handle an Unavailable Reviewer

Never silently replace independent review with self-review.

When subagents are unavailable:

1. Tell the user that the independent audit cannot run.
2. Ask whether to stop or explicitly waive independence for this task.
3. Continue only after an explicit waiver.
4. Perform the same evidence-based audit as a labeled self-audit and state that
   it was not independent.

A waiver changes the reviewer requirement only. It does not waive focused tests
or permission to ignore audit findings.

## Resolve the Audit

1. Verify the findings against the code and task.
2. Apply justified test removals, splits, rewrites, or additions.
3. Record why any recommendation was rejected.
4. Run the smallest relevant test set after resolving the audit.
5. Re-run the audit if later edits materially change the tested behavior or add
   a substantial new test area.

## Report the Gate

In the final handoff, state:

- the resolved threshold and its source;
- the measured changed-line total and exclusions;
- whether the audit was independent or ran under an explicit self-audit waiver;
- which tests were kept, removed, split, rewritten, or added;
- any rejected recommendation and its reason;
- the focused test commands and results.
