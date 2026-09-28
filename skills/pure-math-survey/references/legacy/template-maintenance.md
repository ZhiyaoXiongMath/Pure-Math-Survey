# Historical v1 reference

This is retained legacy documentation. Native v2 follows ../records-and-delivery.md and the current SKILL.md.

# Templates and example builds

The ten templates are instructional scaffolds. Their insertion text is not finished exposition and their slots are not quotas. Use the pair for the selected Part: the mathematical tasks stay the same, while standard expands the decisive proof interiors. Titles and dates use inline insertion text; never put the paragraph-producing `\placeholder` macro inside `\title` or `\date`. Drafting instructions belong in comments, not before the abstract.

## Review template behavior

Read each template by its Part's purpose. Check first definitions, principal answers, body results, necessary proof inputs, consumers, and visible proof/import boundaries. Inspect actual conditions and conclusion formulas when filling the template. An immediately repeated introduction theorem, a detached lemma, or an appended generic depth chapter does not demonstrate a mathematical body.

Compare each concise/standard pair for the same question, material assumptions, selected results and essential mechanisms. Change depth at the point of use. Permit a legitimate model account without a separate lemma, a context-only section with a reason, and a settled account without a Problem. No section, result, proof or length ratio is prescribed.

## Build the supplied material

Run `python scripts/validate_assets.py`, then `python scripts/build_checks.py --output /absolute/empty/directory`. The output is external to the skill. The runner compiles the ten templates, the elementary example, the v6 source with its original preamble and with the current shared style, and the compact example in current and frozen style modes. It reports compilation and source-shape findings separately; it neither completes the reader review nor certifies examples.

`stage_compact_sample` selects explicit dependencies. The `compact-current` target uses `assets/templates/math-review.sty`; `compact-frozen` uses the style next to the retained compact source. The report records the mode and style hash. Modify and build copies, not the retained originals. Render the outputs and inspect pages separately.

For script or template changes, use external development tests to cover dependency isolation, literal input expansion, canonical recalls, optional Problems, stale source evidence, missing/misattached proofs, imported-result locators, principal-answer coverage, and legitimate result-free sections. These tests are not needed to use an installed skill. Normal project creation, building, validation and archive verification depend only on files supplied here and the documented tools.

## Evidence limits

`--inventory` reports actual environments, reference sites and the source digest. It is not an approval. Content-first reading must identify mathematical claims that the syntax inventory misses. A wrapper around an unchanged essay can satisfy superficial syntax and still fail that reading. Review all affected pages after repairs. Source verification, author rereading, independent review, compilation and reproduction are distinct activities.
