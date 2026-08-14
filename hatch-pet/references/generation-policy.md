# Hatch-Pet Generation Policy

Use this reference for brand-only requests, transparency and effects policy, and
time-budget convergence decisions.

## Contents

- [Brand Discovery](#brand-discovery)
- [Transparency And Effects](#transparency-and-effects)
- [Time Budget And Convergence](#time-budget-and-convergence)

## Brand Discovery

If the user provides a brand, company, product, or prospect name rather than a concrete avatar description or reference image, run a lightweight discovery subagent before preparing the pet run. The discovery worker must use web search and prefer official sources such as the brand site, product pages, docs, about pages, press pages, or brand pages. Use reputable secondary sources only when official pages are too thin. Keep the search narrow: enough to extract visual and personality cues, not a market-research brief.

Skip discovery when the user already provides a concrete mascot/avatar description or reference images, unless the user explicitly asks for brand research.

Discovery worker responsibilities:

- search the web for 2-4 relevant sources, preferring official pages
- write an adaptive markdown brief rather than a rigid field dump
- cover identity/category, audience/use context, visual system, personality/tone, product/domain motifs, mascot translation cues, avoidances, and evidence/confidence
- mark mascot guidance that is inferred from sources as inference
- avoid copying logos, readable marks, UI screenshots, slogans, or text
- end with a compact `Generation handoff` section containing only `brand_name`, `brand_brief`, `avatar_seed`, `avoid`, and `brand_sources`
- do not generate images, prepare run folders, or edit unrelated files

Use this discovery worker prompt:

```text
Research a brand for hatch-pet mascot creation.

Brand/product/prospect: <brand name>
User context: <short user request>
Output file: <absolute path to brand-discovery.md>

Use web search. Prefer official brand, product, docs, about, press, or brand pages. Use reputable secondary sources only if official sources are too thin. Write an adaptive markdown brief to the output file. Headings may flex by brand, but the brief must cover:
- identity/category: canonical name, product type, what it does
- audience/use context: who it serves and where it appears
- visual system: palette, shapes, line quality, materials, typography feel, iconography, patterns
- personality/tone: emotional traits, energy, formality, playfulness
- product/domain motifs: objects, workflows, verbs, metaphors, environments
- mascot translation cues: candidate forms, signature traits, props, what must read at pet size
- avoidances: logos/text, trademark-sensitive elements, misleading cues, competitor confusion, poor mascot fits
- evidence/confidence: source URLs plus notes where evidence is weak or inferred

Do not copy logos, readable marks, UI screenshots, slogans, or text. Clearly label mascot guidance that is inferred rather than directly sourced.

End the brief with a `Generation handoff` section containing exactly:
- brand_name=<canonical brand/product name>
- brand_brief=<one sentence, max 45 words, covering palette/tone/domain motifs/personality>
- avatar_seed=<short mascot-safe visual idea, no logo copying>
- avoid=<short comma-separated list>
- brand_sources=<comma-separated source URLs>

Return exactly:
brand_discovery_file=<absolute output file path>
brand_name=<canonical brand/product name>
brand_brief=<same compact sentence from Generation handoff>
avatar_seed=<same short seed from Generation handoff>
avoid=<same short avoid list from Generation handoff>
brand_sources=<same comma-separated URLs from Generation handoff>
```

The parent should save the markdown brief before preparing the run, then pass it to `prepare_pet_run.py` as `--brand-discovery-file` together with `--brand-name`, `--brand-brief`, repeated `--brand-source`, and a concise `--pet-notes` value based on `avatar_seed` when the user did not provide a better avatar description. Keep the full brief for review; only the compact handoff fields should shape prompts. If web search is unavailable and the user gave only a bare brand name, ask for brand cues before generating.

## Transparency And Effects

Pet rows are processed into transparent `192x208` cells, so every generated pixel must either belong to the pet sprite or be cleanly removable chroma-key background. Prefer pose, expression, and silhouette changes over decorative effects.

The deterministic raster pipeline owns the transparency and chroma-cleanup invariants. Its final edge-local spill-suppression step selects every translucent silhouette-boundary pixel plus opaque boundary pixels whose chroma points toward the known key, then extends clean interior RGB outward through that band in linear light. It preserves alpha exactly, clears hidden RGB under fully transparent pixels, and reports the algorithm and parameters used. The cleanup report plus atlas validator are authoritative for chroma contamination. Once the final report has `ok: true` and atlas validation passes, do not regenerate imagery or add another chroma-cleanup pass.

Fully transparent pixels are allowed outside the sprite silhouette, in unused cells, and in intentional negative-space openings that are part of the pet's design, such as loops or holes in a ribbon body. Reject any generated or repaired cell with accidental 100%-transparent holes inside a filled body, including horizontal bands, seam rows, scanline-like gaps, sliced-tile boundaries, or "see-through" interior stripes. Inspect suspect cells on a high-contrast background or alpha mask before accepting them; ordinary atlas validation is not enough when the hole is inside the silhouette.

Allowed effects must satisfy all of these conditions:

- The effect is state-relevant and helps explain the animation.
- The effect is physically attached to, touching, or overlapping the pet silhouette, not floating nearby.
- The effect is inside the same frame slot as the pet and does not create a separate sprite component.
- The effect is opaque, hard-edged enough for clean extraction, and uses non-chroma-key colors.
- The effect is small enough to remain readable at `192x208` without clutter.

Avoid these by default because they usually break transparent-background cleanup or component extraction:

- wave marks, motion arcs, speed lines, action streaks, afterimages, blur, or smears
- detached stars, loose sparkles, floating punctuation, floating icons, falling tear drops, separated smoke clouds, or loose dust
- cast shadows, contact shadows, drop shadows, oval floor shadows, floor patches, landing marks, impact bursts, glow, halo, aura, or soft transparent effects
- text, labels, frame numbers, visible grids, guide marks, speech bubbles, thought bubbles, UI panels, code snippets, checkerboard transparency, white backgrounds, black backgrounds, or scenery
- chroma-key-adjacent colors in the pet, prop, effects, highlights, or shadows
- stray pixels, disconnected outline bits, speckle/noise, cropped body parts, overlapping poses, or any pose that crosses into a neighboring frame slot

State-specific guidance:

- `idle`: keep this calm and low-distraction. Use only subtle breathing, a tiny blink, a slight head or body bob, a very small material sway, or another quiet persona-preserving motion. The loop must still contain visible micro-variation; do not accept six effectively identical copies. Do not show waving, walking, running, jumping, talking, working, reviewing, emotional reactions, large gestures, item interactions, or new props.
- `waving`: show the wave through paw, hand, wing, or limb pose only. Do not draw wave marks, motion arcs, lines, sparkles, symbols, or floating effects around the gesture.
- `jumping`: show vertical motion through body position only. Do not draw shadows, dust, landing marks, impact bursts, bounce pads, or floor cues.
- `failed`: tears, attached smoke puffs, or attached stars are allowed if they obey the allowed-effects rules; do not use red X marks, floating symbols, detached smoke, detached stars, or separate tear droplets.
- `waiting`: show that Codex needs approval, help, or user input through an expectant asking pose. Keep it distinct from ordinary idle and review.
- `running`: show active task work, processing, thinking, scanning, typing, or focused effort. Do not show literal foot-running, jogging, sprinting, treadmill motion, raised knees, long steps, pumping arms, directional travel, speed lines, dust clouds, floor shadows, motion trails, or detached motion effects.
- `review`: show focus through lean, blink, eyes, head tilt, or paw/hand position. Do not add magnifying glasses, papers, code, UI, punctuation, symbols, or other new props unless they already exist in the base pet identity.
- `running-right` and `running-left`: show directional drag movement through body, limb, and prop movement only. `running-right` must face and travel right; `running-left` must face and travel left. Their cadence must visibly alternate across the loop rather than repeating one nearly static stride. Do not draw speed lines, dust clouds, floor shadows, motion trails, or detached motion effects.

## Time Budget And Convergence

Aim to complete a normal pet run within 30 minutes while preserving every mandatory acceptance criterion. Treat this as a planning target and an incentive to maximize validated progress per minute, not as permission to weaken QA or package a failing pet.

At the start of the run, allocate an approximate budget:

- preparation: 2 minutes
- base image: 3 minutes
- standard rows: 10 minutes
- look directions: 8 minutes
- final QA and packaging: 5 minutes
- buffer: 2 minutes

Run independent generation jobs concurrently up to the worker limit, start deterministic checks as soon as each dependency is ready, and record actual stage plus repair time. Prefer character and prop constructions that naturally satisfy cell geometry, transparency, component connectivity, and direction semantics; identify likely conflicts such as open interior gaps, detached parts, thin connectors, asymmetric props, or ambiguous faces before row generation.

After every failed attempt:

1. Classify the failure as visual semantics, identity, source-edge geometry, component connectivity, extraction, chroma, continuity, or final visual QA.
2. State the concrete evidence and the root condition the next action will change.
3. Use a deterministic correction for deterministic failures before regenerating imagery.
4. Regenerate only when the source visual is genuinely wrong, and preserve every property that already passed.
5. Compare the new result with the previous one. A repair counts as progress only when it reduces the number or severity of failures without breaking a previously passing gate.

If the same root failure recurs twice, stop varying the prompt and change strategy: strengthen the cardinal pose families or row-level direction instructions, simplify the pose or prop construction, change the deterministic extraction method, or redesign the problematic visual feature. If a repair merely moves a failure to another cell or gate, treat that as a cycle and change strategy immediately.

Use elapsed-time checkpoints:

- At 15 minutes, verify the run is on pace and that the remaining dependency path is bounded.
- At 25 minutes, prioritize the shortest quality-preserving path through remaining blockers and avoid optional polish.
- At 30 minutes, continue only when the remaining work is clearly converging and bounded, such as final validation, one targeted repair, or packaging.
- Keep recording elapsed time, retries, validation failures, and QA cost throughout the run, but do not pause or stop solely because elapsed time crosses 45 or 60 minutes. Continue until the pet passes, the user cancels, or a genuine external blocker prevents further progress.

Never use the time target to skip blind direction QA, labeled semantics, continuity review, atlas validation, despill validation, final visual QA, or any other acceptance criterion.
