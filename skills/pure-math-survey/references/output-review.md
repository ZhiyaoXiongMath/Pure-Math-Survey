# Manuscript review and build evidence

Principal statements must be literal inputs inside the actual document body. Comments, preamble content, uncalled macro definitions and literal false branches do not establish visible use. Input paths follow the compiler's manuscript working directory; dynamic filenames, escaping paths and cycles are rejected.

An output_semantic review records the seven checks whole_manuscript, canonical_use, conditions_quantifiers, selection, attribution, proof_obligations and readability. It includes real path/line_start/line_end principal and proof locations. Principal locations must contain the corresponding canonical input. Existing line numbers do not establish mathematical correctness: perform the actual rereading.

Review templates remain pending and cannot overwrite existing records. Each candidate review is checked independently; a valid new review can supersede an incomplete one. Future dates are rejected. Independent review records need an actual reviewer identity; filling that field alone does not establish independence.

Each build and render stores immutable bytes under outputs/ID/history/. The previous build is preserved before a new attempt. A failed attempt remains failed even when an earlier PDF exists. The latest-build pointer identifies an attempt; it is not an acceptance record. A changed PDF or page image requires a fresh visual review.

Authoring materials are regenerated from the selected snapshot before verification. Changed, missing or additional material produces MATERIALS_CHANGED. Explicit reprepare restores copies and preserves authored manuscript and outline files. Keep editable author notes outside materials/.
