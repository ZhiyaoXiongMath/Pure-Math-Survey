# Minimal runtime: PR02 transition

This is the runtime contract for **2.4.1-dev.2**, policy `minimal-transition-pr02`, and project `runtime_contract: minimal-lean-2.4.1`. Run in the current session with its current model. Only `minimal` and its fixed `integrated` view are supported. Knowledge-only and TeX-only are task/delivery choices, not extra writing profiles.

## Source and mathematical content

Fix the source version or actual supplied file identity; use `unknown` for unavailable metadata. Read the introduction, necessary concepts, relevant statements and only those proof passages needed to identify the main modules and their connections. Preserve source IDs and actual locators. Report unresolved statements or missing connections directly. Do not invent source reading, originality, completeness, mathematical certification or permission to redistribute source bytes.

Store one formal LaTeX statement per mathematical unit, with all its objects, assumptions, quantifiers and conclusion. Explain a module's method, useful output and next consumer briefly. Established concepts should be defined and then used by name. Sources determine the mathematics; the manuscript uses the same canonical statements. No paired full fast/slow texts, internal reproof, proof promises, reviewer roles, review JSON, approval gates or mandatory child chats are part of this runtime.

## Transitional storage

PR02 retains KB/snapshot schema `2.0.0` and output schema `2.2.0` for fresh projects only. The runtime contract is checked before mutations. Older projects, including those lacking the contract, receive `LEGACY_PROJECT_UNSUPPORTED`; changing a schema string is not migration. Keep old projects with their corresponding old installation or start a new directory.

`project.json` and `scope.md` identify the project and scope. `knowledge/nodes/N-*.md` uses JSON frontmatter and one label-free `## Canonical statement` followed by a `latex` fenced block. Node metadata retains the transitional keys `schema_version`, `id`, `kind`, `title`, `facets`, `question_ids`, `mathematical_status`, `origin`, `sources`, and `links`; an unassessed mathematical status is allowed. Source records live in `knowledge/sources/S-*.json`, and actual shared macros in `knowledge/conventions.tex`. The initializer may retain small overview/discovery/coverage containers; they do not require long authored explanations or approval records. Do not create a second full mathematical statement in metadata or the manuscript.

A snapshot fixes input bytes for the existing exporter. It is a reproducibility operation, not approval. Output plans identify the selected nodes and their roles, audience and limits. `generated/` and fixed `materials/` are derived inputs; edit live KB instead. Repeated prepare preserves authored manuscript, outline and style. The final schema 3.0.0, routes/index representation and standalone-unit export are PR03 work, not claims of this candidate.

## Supported sequence

Use Python 3.10 or later. The paths below are examples; run the installed `scripts/survey.py` using its actual path. On systems where Python is called `python`, replace `python3` accordingly.

```sh
python3 scripts/survey.py init --output PROJECT --topic TOPIC --scope SCOPE.md
python3 scripts/survey.py kb validate PROJECT
python3 scripts/survey.py kb freeze PROJECT
python3 scripts/survey.py output plan PROJECT --output minimal --snapshot KB-ID --profile minimal --view integrated
python3 scripts/survey.py output prepare PROJECT --plan PROJECT/outputs/minimal/plan.json
```

After init, populate canonical knowledge from the fixed sources before validation and freeze. Use the snapshot ID returned by freeze. For knowledge-only, stop with the KB and a concise account of scope and gaps; do not prepare an output. Preparation creates an unfinished scaffold, not a completed article. Complete its prose and connections before validating/building:

```sh
python3 scripts/survey.py output validate PROJECT --output minimal --stage structure
python3 scripts/survey.py output build PROJECT --output minimal
python3 scripts/survey.py output validate PROJECT --output minimal --stage package
python3 scripts/survey.py output package PROJECT --output minimal --to OUTPUT.zip
```

Minimal uses exactly **Main Results / Key Mathematical Ingredients / Connecting the Ingredients**, with no abstract. Introduce necessary concepts, state all scoped principal contributions completely, select useful modules with their conditions, and explain their actual composition. Keep statements automatically numbered and avoid descriptive optional statement titles. Adjacent prose carries source/version/locator information. A diagram must agree with the actual mathematical relationships; layout cannot create an implication.

The packaged template is transitional. PR04 will install the original rules.v22 and final 11pt, six-body-page, separate-reference-page layout. This candidate does not claim those features are already satisfied and does not load development documents or old mode/review instructions during a run.

## Mechanical checks and delivery

Checks cover safe paths, valid structures and references, exact generated bytes, literal TeX dependencies, actual compile logs/PDF bytes and archive integrity. They do not establish mathematical correctness, coverage of every contribution or reader understanding. `VALID`, `PREPARED`, `BUILT` and `PACKAGEABLE` describe the corresponding software operation. A package-check or package success is an engineering result and requires no review record.

PDF builds require pdfLaTeX, BibTeX, the installed style's TeX packages, and Poppler's `pdfinfo`; optional rasterization also uses `pdftoppm`. Build in the project with shell escape disabled. Retain actual failed attempts. Make at most two local repair rounds for concrete build errors; report remaining failures and the usable artifacts. For TeX-only, omit build-dependent PDF packaging and say the PDF/page count was not measured. An archive is created only when its actual required build inputs are present and consistent.

Describe the requested result as complete, incomplete or failed according to the artifacts actually delivered, with known gaps and actual build state. Completeness does not mean mathematical certification. Never invent PDF inspection, source reading, test results, token counts or percentage savings. Old `review` and `kb readiness` commands are unsupported and cannot supply approval for this runtime.
