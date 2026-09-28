# Native file fields and reproducible operations

Data `schema_version` strings remain exactly `2.0.0`; the software runtime is `2.0.2`. See [2.0.1 integration](integration-2.0.1.md) for stricter output-review fields, actual body locations, build history and foreign-contract imports. JSON has no duplicate keys or nonfinite numbers. Stable IDs use letters/digits/dot/underscore/hyphen, with N- and S- prefixes for nodes and sources; each filename equals its ID. All project-relative paths are POSIX, contain no traversal/absolute prefix and cross no symbolic links.

## Project and knowledge

project.json: schema_version, project_id, title, language, scope_file, knowledge_root; optional nullable literature_cutoff. Knowledge requires overview.md, conventions.tex, discovery.md, coverage.json. There need not be any output.

Node frontmatter is a JSON object between standalone `---` lines, followed by readable Markdown. Required fields: schema_version, id, kind, title, facets (nonempty), question_ids, mathematical_status, origin, sources, links. Kinds: question/definition/result/relation/mechanism/example/application/frontier. Status: unassessed/established/conjectural/open/refuted/not_applicable. Origin: primary_source/supplied_manuscript/local_derivation. Sources link source_id, exact locator and support/provenance role; optional version must match the controlling source. Relations are uses_definition/proof_input/explained_by/explains/compares_with/refutes/specializes.

A formal node has at most one `## Canonical statement`, containing only one fenced latex block. Definitions/results/relations require it. No theorem/definition/document wrapper, label or external input inside. The literal inner UTF-8 bytes, including internal line endings, are exported unchanged. Metadata titles organize knowledge, not obligatory theorem titles.

Source JSON: schema_version, id, kind (primary/supplied_manuscript), title, authors, publication_status, identifiers, version (explicit text/null), access. Access has state metadata_only/full_text_read, checked_at, material_sha256, local_path (explicit null allowed), optional reading_note. Original online reading without PDF bytes has the extra scoped limitation described in [source evidence](research-and-evidence.md). Unresolved version_conflicts block readiness. Optional bibliography.year supplies an explicit calendar year (1900–2099); otherwise export uses an unambiguous calendar year in version text, never the YYMM prefix of an arXiv identifier. An unavailable year is omitted, not guessed.

Coverage JSON: schema_version, questions. Each question has question_id, answer_nodes, mechanism_nodes, boundary_nodes, gaps, assessment pending/adequate/limited, rationale. An empty boundary list is allowed with substantive scope reasoning. Gap dispositions resolved/outside_explicit_scope require reason; other outstanding important gaps block readiness.

## Plan

Required: schema_version, output_id, snapshot_id, profile, view, language, title, audience, reader_goals, question_ids, prerequisites, selections, omissions, proof_obligations, limits, draft. Optional comparison_group and consume_overview (default true).

Selection: node_id; role principal_answer/essential_bridge/boundary/background/frontier; statement_treatment full/explained_reference; proof_treatment complete/sketch/mechanism/citation/none; reason. Omission: node_id/reason. An explicitly scoped prerequisite is either plain reader background or an object with node_id/scope/reason; only the object can mechanically discharge a specific unselected dependency.

Proof obligation: node_id, treatment complete/sketch/mechanism, nonempty required_steps, imported_inputs. An expanded proof selection must have step obligations directly or through selected explaining mechanisms. Imported inputs need explicit selection/prerequisite treatment. limits.max_pages is required and nullable; optional page_review_threshold is also nullable. A comparison group shares snapshot/question/core/boundary only when explicitly requested.

## CLI recipes

```sh
python scripts/survey.py init --output topic --topic topic-id --scope scope-input.md --json
python scripts/survey.py kb validate topic --json
python scripts/survey.py kb index topic --json
python scripts/survey.py kb freeze topic --json
python scripts/survey.py kb verify topic --snapshot KB-FULL_HASH --json
python scripts/survey.py output plan topic --output short --snapshot KB-FULL_HASH --json
python scripts/survey.py kb readiness topic --plan topic/outputs/short/plan.json --json
python scripts/survey.py output prepare topic --plan topic/outputs/short/plan.json --draft --json
python scripts/survey.py output validate topic --output short --stage plan --json
python scripts/survey.py output validate topic --output short --stage structure --json
python scripts/survey.py output build topic --output short --json
python scripts/survey.py output render topic --output short --json
python scripts/survey.py output review-template topic --output short --kind output_semantic --to evidence/semantic-review.json --json
python scripts/survey.py output review-template topic --output short --kind visual --to evidence/render-review.json --json
python scripts/survey.py output validate topic --output short --stage release --json
python scripts/survey.py output package topic --output short --to short.zip --json
python scripts/survey.py kb diff topic --from KB-OLD_FULL_HASH --to KB-NEW_FULL_HASH --json
```

These recipes use placeholder IDs. init produces an empty unverified KB; add real scope-specific knowledge, evidence and coverage before a meaningful plan. Prepare makes no mathematical claims and preserves existing prose. Fill review templates only after the actual recorded work. `--draft` permanently marks that plan draft until an explicit reviewed plan change/reprepare; never remove the flag merely to bypass readiness.
