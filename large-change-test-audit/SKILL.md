---
name: large-change-test-audit
description: Independently audit unit-test changes in implementations exceeding the user or repository changed-line threshold, defaulting to 1,000 additions plus deletions. Audit a coherent slice before delivery or merge preparation.
---

# Large Change Test Audit

## Scope and Timing

Resolve the threshold from the user's task instruction, then repository policy,
then a default of 1,000 additions plus deletions. Measure only the task's diff;
exclude clearly mechanical generated, vendored, and lock-file changes and record
the exclusions. Never raise the threshold merely to avoid review.

When the measured total exceeds the threshold, or is reasonably expected to,
schedule an independent audit of the next coherent implementation slice. Finish
that slice and its focused tests before review; crossing the threshold midway
through an edit does not require an immediate stop. Complete the audit and
resolve findings before delivering the implementation or preparing it for merge.

## Independent Review

Spawn a read-only subagent with the user's request, settled contract, threshold
and scope calculation, relevant production diff, all added/modified unit tests,
nearby tests, and available focused test output. Supply raw artifacts rather
than the main agent's conclusions. Keep implementation ownership with the main
agent and continue independent authorized work while review runs.

Ask the reviewer to:

- Classify changed tests as keep, remove, split, or rewrite, citing evidence for
  changes and grouping unproblematic tests where useful.
- Check required behavior and credible regressions, duplicate coverage,
  unrelated assertions, implementation coupling, and false-positive fixtures.
- Identify missing coverage; if no tests changed, assess whether that is justified.
- Cite exact files and lines for actionable findings.

Verify findings, apply justified changes, explain rejected recommendations, and
run the smallest affected test set. Repeat review only for material later changes
to the tested behavior or a substantial new test area.

## Unavailable Reviewer

Never describe self-review as independent. If subagents are unavailable,
continue useful authorized implementation and focused verification. Before
final delivery or merge preparation, request an explicit waiver to substitute a
labeled self-audit; honor an existing waiver for the task without asking again.
Without a waiver, report the independent review as pending rather than complete.
A waiver does not waive tests or resolution of findings.

Report the threshold/source, measured scope and exclusions, review independence,
actionable findings and resolutions, and focused verification results concisely.
