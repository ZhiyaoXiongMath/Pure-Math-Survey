# Pure Math Survey 2.0.2

Knowledge first: scope → primary-source reading → readable nodes/relations/evidence → coverage/readiness → immutable snapshot → output plan → writing → actual checks/build/page inspection → delivery.

**The core CLI uses only Python's standard library (Python 3.10+).** This is a file-based skill and deterministic tooling, not an autonomous theorem prover or an unattended survey-writing service. An agent/author performs source reading and mathematical writing; the CLI checks contracts, dependencies, fixed bytes and declared evidence. No server, vector database, multi-agent scheduler or Studio bridge.

## 2.0.2

Generated authoring materials now undergo exact snapshot/member checks before structure validation, building and release. Explicit reprepare restores disposable copies and keeps manuscript/outline edits. UTF-8 scope migration and isolated legacy entry points work on Windows and Python 3.10. Data schema remains 2.0.0.

## 2.0.1 integration

Body-aware canonical checks, seven explicit whole-manuscript reading checks, real proof/principal locations, immutable build/render history and explicit B-format v2 imports are documented in [integration-2.0.1](references/integration-2.0.1.md). Runtime 2.0.2 preserves data schema 2.0.0 and old snapshot identities. Historical accepted records never automatically satisfy new review requirements.

## Install and run

Extract `pure-math-survey-2.0.2.zip` and copy its single `pure-math-survey/` folder to the skill directory used by your host application. Or run its scripts directly without installing any pip package:

```sh
python pure-math-survey/scripts/survey.py --version --json
python pure-math-survey/scripts/validate_assets.py --json
python pure-math-survey/scripts/survey.py init --output my-topic --topic my-topic --scope my-scope.md --json
python pure-math-survey/scripts/survey.py kb validate my-topic --json
```

Write a real mathematical scope in my-scope.md first. Initialization is knowledge-only and creates no outputs. Native projects use `project.json` with schema 2.0.0. Build requires pdfLaTeX, BibTeX and the packages loaded by math-review.sty; actual page counting/rendering uses Poppler pdfinfo/pdftoppm. `bibtex.original`/`bibtex8` are recorded fallbacks when present. See references/layout-and-build.md for dependencies. No network access is required by the deterministic core; source discovery is performed through the agent's available tools and documented honestly.

## Three profiles, one knowledge authority

`minimal` gives exact core answers with essential mechanism/boundary; `thematic` organizes related results and their supported relations; `lecture` develops declared prerequisite steps and calculations. Default requested output is **minimal + integrated**. A knowledge/update-only request has no implicit manuscript. PDF is not a fourth profile. Part I–IV are overlapping foundations/results/methods/boundaries views, not required separate volumes. Only an explicit user max_pages is a length gate.

Edit canonical mathematics only in knowledge nodes. Freeze with `kb freeze`. Create an explicit plan with `output plan ... --snapshot KB-...`. Refine audience, selections and proof steps; review scoped readiness before formal preparation. `output prepare` emits exact snapshot fragments and an incomplete writing scaffold; it does not invent a finished mathematical text. `--draft` permits unverified internal preparation but prevents formal release. Existing authored main.tex is preserved on reprepare; review it before adopting a changed snapshot.

`kb diff` reports changed/added/removed knowledge and affected consumers. Old snapshots and outputs remain rebuildable. Checks compare actual files, not cached PASS labels. Rendering produces images, not a completed visual review. Read every final page before accepting visual evidence.

## Compatibility and maintenance

`create_project.py` keeps v1 creation behavior. Legacy checkers dispatch native v2 projects explicitly; both root manifests together fail. `survey.py migrate --from OLD --output NEW` preserves source bytes and imports unassessed candidates; old audits do not become new reviews. Read references/migration.md.

The public repository carries runtime source, behavioral tests and clean-install verification. A complete new-topic example and current validation summary accompany the release; earlier development baselines remain historical evidence. The installation ZIP contains only supported runtime resources, including all survey_core modules, profiles and rebuild tools. It deliberately excludes repository demonstrations, original source archives and Studio reference code. See SKILL.md for the operative workflow and references/contracts.md for schemas/CLI.

No independent review or general mathematical correctness follows from a software test. Acceptance evidence records the actual scoped author rereads and limitations; source hashes, builds and PDF inspections are separate evidence.
