# Minimal runtime: shared lean knowledge

This is the runtime contract for the **2.4.1 release candidate** (not a published tag or Release), KB/output schema `3.0.0`, policy `minimal-rules-v22-lean-2.4.1`, and project `runtime_contract: minimal-lean-2.4.1`. Run in the current session with its current model. Only `minimal` and its fixed `integrated` view are supported. Knowledge-only and TeX-only are task/delivery choices, not extra writing profiles. For requested Minimal writing, read this adaptation first and then [the original rules.v22](rules.v22.txt) once. Knowledge-only work reads the short KB contract below and skips the writing/layout rules.

## Runtime adaptation of the original rules

The fixed source governs mathematics. Original rules.v22 governs content, organization and layout; the following explicit runtime adaptations override its repeated-review and extra-report workflow. Run in the current session without required reviewer roles, child chats, approval records or a review-and-repair loop.

| Original clauses | Runtime application |
| --- | --- |
| #001–#045, #051–#092 | Preserve the mathematical concepts, complete interfaces, selected modules, short compositions, graph meaning and normal layout. A strong diagram cannot compensate for omitted concepts or hypotheses. |
| #004, #033, #040, #042, #046–#048 | Identify source versions, printed statement types/numbers, locators, module inputs and outputs during source reading and extraction. Read the necessary proof passages without reconstructing complete internal proofs or starting another audit. |
| #049–#050 | Use the same KB nodes/routes as the compact plan and source map. Prepared inputs and preparation history preserve actual bytes; no second manual planning document or approval gate is required. |
| #093–#094 | Actually compile by default, retain real logs, and record main/total pages separately using the template's body-end marker. |
| #095–#097 | Preserve local completeness, concept use, principal coverage and layout as first-pass writing duties. Do not require per-run page reviewers, dual font-evidence reports, statement-by-statement rereviews or article-first review. Never claim unseen pages were inspected. |
| #098 | Fix known omissions or false relationships locally and report what remains incomplete; do not compensate with another strength or create an unbounded review loop. |
| #099–#100 | No mandatory priority-improvement or rule-change report. Freeze the rule bytes; version changes belong to authorized development, not ordinary user runs. |
| Extra deliverables | Nodes/routes and the generated graph map replace a separate hand-written `node_edge_map.md`; omit `qa.md`. `run.json` records actual artifacts, source identities, build results and known limitations. |

The sole original file is [rules.v22.txt](rules.v22.txt), 22,806 bytes, SHA-256 `452a4d7548c23bc75fe8fec6299ae9777a3e6763eb5f955063d938c2f3b6b2c7`. Keep these adaptations in this short contract; do not rewrite the original or load development history and retired mode/dispatch instructions into a run.

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

`run.json` is a concise machine record of source identities, input hash, output paths and known limitations. After an actual build it records the build state, main pages and total pages; its `tokens` and `elapsed_seconds` remain null. Per-article model identity is not captured by this record and is unavailable without a separate factual record. Complete article token/time measurements likewise require independent evidence; build/test timings do not measure the complete article workflow. TeX-only page counts remain unmeasured. There are no mandatory overview, discovery, coverage, review files or snapshots. Old schema 2.x projects remain unsupported even if they carry the same runtime contract; failures leave them unchanged. No automatic migration or mathematical-equivalence deduplication is provided.

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

For a requested Minimal, plan directly from the current KB. The view is fixed to `integrated`; there is no `--view` option:

```sh
python3 scripts/survey.py output plan PROJECT --output minimal --profile minimal
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

## Writing, graph and page contract

Use the opening to establish core concepts and all independent principal contributions in the fixed scope. Give each selected module its complete mathematical interface, brief method identity and downstream use. Roughly five to ten major stages guide the overall scale; this is not a node quota. Internal proofs stay encapsulated unless a specific reader need makes an internal fact necessary. A statement may use precisely defined concept names, but it must state its own hypotheses, data, governing relations and conclusion.

Keep exactly the three body sections, with no abstract, extra front matter or body appendix. Use automatic section-based statement numbering without descriptive optional statement titles. Put source/version/locator attribution adjacent to the corresponding statement heading and opening. Distinguish joint premises, alternative sufficient routes and independent branches in both prose and the diagram.

The article uses 11pt body/formal statements, normal leading, one column and margins of at least 20mm. Substantive graph text has a base size of at least 10.5pt. Title and graph count toward the maximum of six main pages; references start separately. Retain the template's `\pmsmainend` before the bibliography: it starts the reference page and provides the actual main-page count used in build/report/run. Do not remove or move it to evade the cap.

Edit `manuscript/architecture_graph.tex` as TikZ. Its nodes and connections use the same unit/route identities as the body and `generated/graph-map.json`. Keep identifiers in machine names; visible nodes use ordinary formal result numbers and meaningful mathematical phrases. Attach every substantive method note or label explicitly to a node, connection, region or the whole figure; proximity alone is insufficient, and a note must not create a false implication or extra result node. Preserve grouped joint inputs, separate alternative routes, and the unresolved status of unsupported connections. First prepare creates the editable graph; repeated prepare preserves authored layout while refreshing the map, so adjust any now-stale connections to match the changed KB.

Keep literal declarations such as `\node[pmsresult] (N-id) at (0,0) {Theorem~\ref{node:N-id}: short mathematical phrase};`. Each recorded premise set has its own `\node[pmsjoin] (R-id-1) ...;`, with one `\draw[pmsedge] (N-id) -- (R-id-1);` per formal input and another from the join to its target. Use `pmsunresolved` instead of `pmsedge` for unresolved connections. A `pmsannotation` node needs an explicit `% note-owner: note-name R-id-1` comment and a `\draw[pmsattachment] (note-name) -- (R-id-1);` attachment. Edit coordinates and short mathematical labels while keeping the installed semantic styles. Connections support literal `--` or `to[bend left=15]` and anchors such as `(N-id.south)`; complex paths and `\path`/`\edge` syntax are unsupported by the mechanical relationship check.

Resolve excessive length by removing repetition, combining internal support where mathematically justified and adjusting natural page/graph layout. Do not shrink fonts or margins, globally scale the diagram, add negative layout spacing, remove principal coverage or silently split the article to fit. After at most two local correction rounds for concrete build errors or excess pages, report an unmet contract with the existing artifacts if it still fails.

## Mechanical checks and delivery

Checks cover safe paths, valid schemas and references, concept dependency closure, exact exported bytes, retained source hashes, literal TeX dependencies, graph identity/relationship consistency, actual compile logs/PDF bytes, main-page limits and archive integrity. They do not establish mathematical correctness, complete contribution coverage or reader understanding. `VALID`, `PREPARED`, `BUILT` and `PACKAGEABLE` describe software operations and require no review record.

PDF builds require pdfLaTeX, BibTeX, the style's TeX packages and Poppler's `pdfinfo`; optional rasterization uses `pdftoppm`. Shell escape remains disabled. Retain actual failed attempts. Use the bounded local repair policy above and report remaining failures. For TeX-only, omit build-dependent PDF packaging and state that PDF/page counts were not measured.

Report complete, incomplete or failed according to the requested artifacts actually delivered, together with known gaps and actual build state. Completeness does not mean mathematical certification. Describe removed runtime workflows and excluded installer resources as scope changes; they do not establish measured efficiency gains. Do not invent source reading, PDF inspection, tests, token counts or percentage savings. Old review/readiness commands and unsupported modes are rejected.
