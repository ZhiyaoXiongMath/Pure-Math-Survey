# Conservative v1 migration

Use `python scripts/survey.py migrate --from OLD --output NEW --json`; NEW must not exist and must not contain/be contained by OLD. The importer atomically writes a new project and checks the old file hashes. Every original file remains byte-for-byte in legacy/original. Historical cutoffs and PASS assertions remain historical and do not confer v2 readiness.

The importer gathers actual manifests, scope/architecture, BibTeX and bibliographic identity, publication mapping, canonical components and inline theorem/lemma/proposition/corollary/definition spans. It writes candidate nodes with supplied_manuscript/unassessed, identity records with metadata_only, pending coverage and draft mapped output plans. It records wrapper/label removal as separate byte diffs, source locations, ambiguity and unreconciled material. Method/frontier/audit material that cannot be faithfully parsed remains readable original input explicitly listed for manual migration; no claims of semantic conversion.

V concise maps to minimal/integrated; V standard to thematic/integrated; I–IV to thematic with matching view, retaining depth provenance. This is only initial configuration: review the old user's promised core before changing selection. New lecture plans require a request.

The TeX candidate parser is intentionally conservative and is not a full macro expander. Statements depending on surrounding definitions, custom environments or nonliteral inputs need manual reconstruction. Language, explicit user page limits and legacy depth are preserved where present; missing/ambiguous fields are reported rather than invented.

Read MIGRATION_REPORT.json and MIGRATION_REPORT.md in the new project. Resolve IDs/versions/quantifiers, link real definitions and proof inputs, read original literature, review mathematics and coverage, then freeze a new snapshot. The imported draft cannot be released until those steps and independent-output reading/build/page checks have actually occurred. Never edit legacy originals to make a new audit pass.
