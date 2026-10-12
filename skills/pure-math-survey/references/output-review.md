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
- Minimal: results_first, point_use, decisive_connections.
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

For rc2 Paper, record prior_result_checks separately from prior_art_searches.
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
