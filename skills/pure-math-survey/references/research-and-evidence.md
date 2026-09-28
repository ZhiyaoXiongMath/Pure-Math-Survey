# Source discovery, reading and evidence

Search from the question, not just the supplied papers: aliases, original formulations, strongest answers, counterexamples and subsequent improvements. Record actual queries/dates, candidates, decisions, omission challenge and stopping reason in discovery.md. Preserve inaccessible texts and ambiguity as explicit gaps. A short requested document is not a research cutoff.

Register primary identities first. Read the actual supporting sections, checking hypotheses, quantifiers, normalizations, locator and controlling version. Write a source-check note. Distinguish retrieved metadata from original-text reading, and unpublished/preprint/published status from mathematical status. Do not claim all of a paper was read when only supporting sections were inspected.

`access.local_path` points to original bytes only when present and legally retainable; it is hashed and snapshotted. With no raw bytes use null `material_sha256` and null `local_path`, record `material_hash_unavailable_reason`, a versioned URL and substantive `reading_note`. The source review must declare `scope.source_reading[S-ID]` with `mode: original_text_online`, the exact `version`, nonempty `locators` and `raw_bytes_unavailable_reason`. This yields a visible warning, not a byte certificate. Never use a reading-note hash as the material hash.

Translate source notation into exact local mathematics and justify the translation. A real-class extension of a line-bundle theorem is a local deduction, not silently an original theorem. Mechanisms have actual inputs, intermediate calculations and outputs. Source review asserts support for the imported theorem statement; it need not reproduce the full external proof. Its scope must say so.

Use `review template PROJECT --kind source --id S-ID --to evidence/reviews/new.json` (similarly mathematical/coverage) to obtain pending bindings. Only after actual reading fill date, author_reread, substantive findings, disposition and remaining limitations. An independent tool invocation by the same author is still self-review. See [validation](validation.md).
