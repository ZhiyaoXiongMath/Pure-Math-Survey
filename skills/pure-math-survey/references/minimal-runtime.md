# Minimal runtime: shared lean knowledge

This is the runtime contract for **2.4.1-dev.3**, KB/output schema `3.0.0`, policy `minimal-transition-pr03`, and project `runtime_contract: minimal-lean-2.4.1`. Run in the current session with its current model. Only `minimal` and its fixed `integrated` view are supported. Knowledge-only and TeX-only are task/delivery choices, not extra writing profiles. The final rules.v22 layout is still PR04 work.

## Source and mathematical content

Fix the source version or actual supplied file identity; keep an unavailable version null instead of inventing it. Read the introduction, necessary concepts, relevant statements and only those proof passages needed to identify the main modules and their connections. Record real source IDs and locators. Report unresolved statements or missing connections directly. Do not turn the task into an automatic whole-field search or invent source reading, originality, completeness, mathematical certification or permission to redistribute source bytes.

Store one formal LaTeX statement per mathematical unit, with its objects, assumptions, quantifiers and conclusion. Define important concepts and then use their names. Explain a module's method, useful output and next consumer briefly. Sources determine the mathematics; the manuscript reuses the same canonical statements. No paired full fast/slow texts, internal reproof, proof promises, reviewer roles, review JSON, approval gates or mandatory child chats are part of this runtime.

## Knowledge storage

A fresh project contains `project.json`, `scope.md`, and the following KB resources:

| Resource | Content |
| --- | --- |
| `knowledge/sources/S-*.json` | Source identity, title, authors, version, citation key, optional URL and actual access information. |
| `knowledge/conventions.tex` | Shared macros and notation; no hidden mathematical assumptions. |
| `knowledge/nodes/N-*.md` | One authoritative mathematical unit in Markdown with JSON frontmatter. |
| `knowledge/routes.json` | Explicit input-to-output connections between units. |
| `knowledge/index.md` | Short generated navigation; no second mathematical exposition. |

A source record requires `schema_version`, `id`, `title`, `authors`, `version` and `citation_key`. `version` may be null; `url` and `access` are optional. Retained original bytes use the actual `access.local_path` and `access.material_sha256`; hashes must match. Reading access and source-byte redistribution are separate facts. Keep private originals outside the project, and never relabel original bytes as notes to bypass the existing packaging checks.

A node requires `schema_version`, `id`, `kind`, `title`, `role`, `sources`, `definition_refs`, `source_status` and `importance`. Kinds are `definition`, `result`, `method`, `example`; roles are `principal`, `ingredient`, `bridge`, `context`, `boundary`. Type, role and importance express different facts. Each source entry identifies `source_id` and a real `locator`, with an optional controlling version. `definition_refs` lists the actual definition units needed to interpret the statement. `source_status` is `stated`, `extracted`, `imported` or `unresolved`; none of these certifies a proof.

`importance` has `level` (1–5 or null), `status` (`proposed`, `human_supplied`, `unassigned`) and a short `reason`. Unknown importance does not block work; proposed importance is not a human training label. Definitions, results and formal examples use one label-free `## Canonical statement` followed by a `latex` fenced block. A method unit may include an independently meaningful formal statement. Without a canonical statement it contains a brief method/use explanation and cannot serve as a route target or a full principal result. Do not repeat assumptions and conclusions in metadata or hand-copy a second statement into the manuscript.

`routes.json` has `schema_version: "3.0.0"` and a `routes` list. A route contains `id` (`R-...`), `premise_sets`, `target`, `mapping`, `source_locator` and `status`. Each premise set has `nodes` and `additional_inputs`. Nodes inside one set are jointly needed; different sets are alternatives. For example, `{A,B}+H -> C` and `{D}+K -> C` must not become a claim that A, B and D are all required. `mapping` briefly explains which output supplies which next input. A supported `source_locator` contains `source_id` and `locator`; an unresolved connection may use null and must not be presented as established. Route statuses are `stated`, `extracted`, `unresolved`. A principal does not mechanically require its own route; actually recorded unresolved routes or units remain visible limitations and make the run incomplete.

`run.json` is a concise machine record of source identities, input hash, output paths and known limitations. After an actual build it records the build state and total pages; separate body-page, time and token measurements remain null when unavailable. There are no mandatory overview, discovery, coverage, review files or snapshots. Old schema 2.x projects remain unsupported even if they carry the same runtime contract; failures leave them unchanged. No automatic migration or mathematical-equivalence deduplication is provided.

## Supported sequence

Use Python 3.10 or later and the actual installed script path. On systems where Python is called `python`, replace `python3` accordingly.

```sh
python3 scripts/survey.py init --output PROJECT --topic TOPIC --scope SCOPE.md
python3 scripts/survey.py kb validate PROJECT
python3 scripts/survey.py kb index PROJECT
```

After init, populate sources, canonical units and routes before validation and index generation. For knowledge-only, stop here with the KB, scope and known gaps; do not prepare an output. To export a unit with its definition dependencies, conventions and source information, use a new destination:

```sh
python3 scripts/survey.py kb export PROJECT --node N-ID --to NEW-DIRECTORY
```

For a requested Minimal, plan directly from the current KB:

```sh
python3 scripts/survey.py output plan PROJECT --output minimal --profile minimal --view integrated
python3 scripts/survey.py output prepare PROJECT --plan PROJECT/outputs/minimal/plan.json
```

Prepare captures exact input bytes and generates statements/materials automatically; no snapshot ID is required. Optional `kb freeze`, `kb verify` and `kb diff` remain reproducibility tools. Preparation preserves captured input bytes, but verify/build/package compare them with the live KB and reject stale inputs after a canonical change. Modify the live KB, then prepare again before continuing. Repeated prepare first saves the previous manuscript, generated inputs and build bytes in `history/preparation`, then refreshes derived generated/material files while preserving authored main text, graph, style and outline. Do not edit generated statements or frozen bytes. Previously packaged archives retain their own inputs.

Preparation creates an unfinished scaffold. Complete **Main Results / Key Mathematical Ingredients / Connecting the Ingredients**, with no abstract. Establish core concepts, give all scoped principal contributions completely, choose useful modules with their conditions and explain their actual composition. Keep automatic numbering without descriptive optional statement titles. Adjacent prose gives source/version/locator information. Diagram relationships must agree with the units and routes.

```sh
python3 scripts/survey.py output validate PROJECT --output minimal --stage structure
python3 scripts/survey.py output build PROJECT --output minimal
python3 scripts/survey.py output validate PROJECT --output minimal --stage package
python3 scripts/survey.py output package PROJECT --output minimal --to OUTPUT.zip
```

The template remains transitional. PR04 will install the original rules.v22 and final 11pt, six-body-page, separate-reference-page layout. Do not claim those features already hold or load development documents and old mode/review instructions during a run.

## Mechanical checks and delivery

Checks cover safe paths, valid schemas and references, concept dependency closure, exact exported bytes, retained source hashes, literal TeX dependencies, actual compile logs/PDF bytes and archive integrity. They do not establish mathematical correctness, complete contribution coverage or reader understanding. `VALID`, `PREPARED`, `BUILT` and `PACKAGEABLE` describe software operations and require no review record.

PDF builds require pdfLaTeX, BibTeX, the style's TeX packages and Poppler's `pdfinfo`; optional rasterization uses `pdftoppm`. Shell escape remains disabled. Retain actual failed attempts. Make at most two local repair rounds for concrete build errors and report remaining failures. For TeX-only, omit build-dependent PDF packaging and state that PDF/page counts were not measured.

Report complete, incomplete or failed according to the requested artifacts actually delivered, together with known gaps and actual build state. Completeness does not mean mathematical certification. Do not invent source reading, PDF inspection, tests, token counts or percentage savings. Old review/readiness commands and unsupported modes are rejected.
