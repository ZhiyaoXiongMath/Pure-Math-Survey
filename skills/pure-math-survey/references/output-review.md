# Manuscript review and build evidence

Principal statements must be literal inputs inside the actual document body. Comments, preamble content, uncalled macro definitions and literal false branches do not establish visible use. Input paths follow the compiler's manuscript working directory; dynamic filenames, escaping paths and cycles are rejected.

An output_semantic review records the seven checks whole_manuscript, canonical_use, conditions_quantifiers, selection, attribution, proof_obligations and readability. It includes real path/line_start/line_end principal and proof locations. Principal locations must contain the corresponding canonical input. Existing line numbers do not establish mathematical correctness: perform the actual rereading.

Review templates remain pending and cannot overwrite existing records. Each candidate review is checked independently; a valid new review can supersede an incomplete one. Future dates are rejected. Independent review records need an actual reviewer identity; filling that field alone does not establish independence.

Each build and render stores immutable bytes under outputs/ID/history/. The previous build is preserved before a new attempt. A failed attempt remains failed even when an earlier PDF exists. The latest-build pointer identifies an attempt; it is not an acceptance record. A changed PDF or page image requires a fresh visual review.

Authoring materials are regenerated from the selected snapshot before verification. Changed, missing or additional material produces MATERIALS_CHANGED. Explicit reprepare restores copies and preserves authored manuscript and outline files. Keep editable author notes outside materials/.

## New-policy substantive readings

A schema-2.2.0 output review binds the actual plan's editorial_policy. The seven existing
whole-manuscript checks still apply; checking their names alone is not new-policy review.
For each of the following mode_findings provide outcome, a concrete mathematical finding
and actual manuscript path/line_start/line_end locations:

- Common: fast_path, reader_calibration, points, connections, limits, display_rhythm, statement_context.
- Minimal: results_first (early within the local unit under r3; global first section only under historical r2/rc1 or rc2), point_use, decisive_connections.
- Thematic: question_structure, approach_mechanisms, comparison_basis, synthesis.
- Lecture: motivation, worked_derivations, hypothesis_use, imported_inputs, model_boundary.
- Paper: contribution_position, prior_art, proof_closure, attribution.

Reconstruct the target, inputs, decisive operations and conditions from the fast passages,
then follow the actual promised details. For each exact required_steps item, record its
own proof_step_findings entry and location. The principal statement_reviews repeat the
isolated full-claim reading against the exact canonical SHA, in addition to principal
input locations. Check adjoining prose for a quantifier or hypothesis change.

Paper original-principal contribution_reviews include actual dated prior-art searches
against snapshot-bound sources, closest prior results, provenance and authorization,
precise difference, full proof closure and remaining caveats. No checked box, fabricated
search, classic theorem or synthetic fixture demonstrates originality. Any actual gap
requires revision/draft status. A draft cannot be formally packaged even with a removed
notice, accepted old review or successful PDF build.

Templates only create pending fields. The checker can reject absent findings, stale hashes,
wrong policies, missing steps and invalid locations; it cannot verify that an eloquent
assertion is true. Distinguish author_reread from independent_review and from real target-reader
feedback. Running another prompt is not independence. Formula density and typeset line
counts are not a semantic score. Inspect actual pages, including justified long statements.

For rc2 and r3 Paper, record prior_result_checks separately from prior_art_searches.
Check each explicit comparison pair against the actual statements; report its
unknowns, quantifiers, domain/parameters, regularity, normalization, conclusion
and actual difference. Locate the manuscript discussion. A hash or accepted
mechanical check does not establish correctness or novelty.

## Current view and design readings

A 2.2.0 output reading binds the exact `scope.view` and contains located
`mode_findings.view_focus` and `exposition_design` findings. The former names
nonempty available `node_ids` and explains the emphasized quantities or steps;
the latter judges whether the concrete capabilities, outline and main text agree.
Both use substantive manuscript body locations. An outline paragraph can help
explain the design, but cannot stand in for a proof location. A fresh hash after
a view edit does not replace either reading. Ordinary proof-step findings must
point to the computation/argument, not merely the imported theorem statement.

Called locally defined environments are checked for execution-changing controls
in their begin/end definitions, just like called local commands. For example,
a `setbox` wrapper cannot certify the enclosed text as literal proof evidence.
An unused definition or an empty begin/end wrapper does not hide body content.
This remains a bounded source model, not a general TeX interpreter or pixel
visibility proof.

## r3 task findings and actual final pages

In article `mode_findings`, retain all inherited checks and add the existing-shaped
`outcome`, `finding`, `locations` entries:

- `obligation_coverage`: reconstruct necessary transformations from target/reader/materials
  before comparing the author's list; record omissions and fixes, then locate evidence.
- `fast_route_reconstruction`: save actual reasoning with long interiors hidden, not headings.
- `slow_step_reproduction`: save a concrete derivation/construction and any missing inputs.
- `condition_transfer`: change a decisive assumption and identify the first failure;
  distinguish a verified counterexample from this route's non-applicability.

Locations remain real executed substantive manuscript body positions (F1). A present
field or plausible assertion is not mathematical/understanding acceptance. Knowledge-only
uses existing knowledge-review scope/findings with actual nodes/routes, revision/hash
and precise subsections; no manuscript is created to obtain article locations. Keep the
knowledge binding/reader contract separate from article evidence. This uses existing
record shapes, not a newly promised typed route database or new CLI.

### Knowledge-only coverage record

Use the existing `review template PROJECT --kind coverage --id QUESTION --json`
command. It creates a pending review, not an accepted reading. Knowledge and
snapshots remain schema `2.0.0`; this policy-bearing review uses `schema_version:
"2.2.0"`, `kind: "coverage"` and the following existing scope fields:

```json
{
  "editorial_policy": "four-modes-2026-10-12-r3",
  "question_ids": ["Q-density"],
  "node_ids": ["Q-density", "N-density", "N-radial-change", "N-zero-boundary"],
  "checks": ["obligation_coverage", "fast_route_reconstruction",
             "slow_step_reproduction", "condition_transfer"]
}
```

This is a scope example, not a review ready for acceptance. Replace its IDs with
the actual question and all coverage-declared answer, mechanism and boundary
nodes; bind any additionally reviewed node too. Keep `findings` as a list of
strings, each beginning with its exact check name and a colon. For example, an
actual reading could report the following forms, only after doing the work:

- `obligation_coverage: Reconstructing the radial substitution exposed the missing Jacobian; the corrected derivation now supplies it.` Link target: `knowledge/nodes/N-radial-change.md#radial-jacobian`.
- `fast_route_reconstruction: With the calculation hidden, I recovered the density from the stated symmetry and normalization; the support condition was missing from my first answer.` Link target: `knowledge/route.md#density-fast-route`.
- `slow_step_reproduction: I evaluated the normalization integral from the declared change of variables and found the stated constant.` Link target: `knowledge/nodes/N-density.md#normalization`.
- `condition_transfer: At the zero parameter the change of variables loses invertibility; this defeats this derivation and does not by itself disprove the claimed limit.` Link target: `knowledge/nodes/N-zero-boundary.md#zero-parameter`.

In each saved finding string, append a real Markdown link: concatenate
`[descriptive label]` and `(knowledge/path.md#subsection)` without an intervening
space. The paths above describe example project inputs, not installed resources.

These illustrative sentences are not evidence about a real project. Save the
actual attempted answer/calculation, first failed step, repair and remaining
uncertainty, rather than copying the sentences or changing a pending template to
accepted. Preserve blocking unchecked items and use the actual reviewer mode/date.

Every link is project-root-relative and resolves to an existing subsection. Use
an ordinary ATX heading or put an explicit stable anchor on its own unindented
line, outside frontmatter, comments, code and raw HTML blocks:

```markdown
<a id="radial-jacobian">

## Radial Jacobian
```

The existing `inputs` list uses `{"path": "knowledge/route.md", "sha256":
"ACTUAL_64_HEX_SHA256"}` entries. The shown hash is a placeholder, never a valid
binding: compute each digest from the exact saved bytes. Include the route,
overview, scoped node files and required project, coverage, scope and source
inputs. The template supplies required coverage inputs; add every other cited
route/node and source used by the reading. A revision string in
`scope.evidence_basis` can aid provenance but cannot replace these file hashes.
Missing links/anchors, unbound inputs or changed bytes invalidate the binding;
passing those checks still does not establish mathematical truth or learning.

For every page of the actual final PDF inspect the active 2–3 normal typeset-line target,
usefulness of displays, local symbol definitions, hidden transformations and fragmentation.
Record actual page/block/equation and corresponding source, finding, impact, repair or
specific exception reason/alternatives, final PDF hash and reinspection scope. Complete
statements/necessary continuous proofs can be long with justification; no blanket waiver.
Never measure TeX wrapping or add decorative formulas/forced breaks/shrunk typography.
Scanners identify candidates only. Rebuild after changes; old observations may be reused
only for verified identical page images and do not grant the new output semantic binding.
New visual records bind the actual final PDF/build/render inputs and all pages.

F2 view/design, F3 explicit comparison pairs plus primary prior support, and F4 draft/design
safety remain on both rc2 and r3. Old accepted fields gain no new r3 responsibilities;
`RECORDED_VALID` cannot authorize current release. Paper remains prominently draft unless
actual authorization, originality positioning and complete proofs are reviewed. Software,
mathematics, exposition attempts, PDF checks and real-reader feedback remain five reports.
