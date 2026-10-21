# Pure Math Survey

[简体中文](README.md) | **English**

Current release candidate: **2.4.1**, policy `minimal-rules-v22-lean-2.4.1`, runtime contract `minimal-lean-2.4.1`. This candidate supports **Minimal writing and knowledge-only work in the current session**. Version 2.4.1 identifies this candidate; no formal tag or Release is announced here. KB and output schemas are 3.0.0. The lean KB provides shared units, routes and a short index. Minimal uses the rules.v22 content and layout contract with explicit runtime adaptations.

Use fixed mathematical sources to build canonical knowledge and reuse those exact statements in an English Minimal. The supported structure is Main Results, Key Mathematical Ingredients, and Connecting the Ingredients. Keep complete assumptions and conclusions, define core concepts, attribute borrowed content accurately and explain the decisive connections briefly. No particular model, child chats, reviewer roles, review records or paired fast/slow manuscripts are required. Knowledge-only work ends with sources, conventions, units, routes and an index. Plans use the current KB; snapshots are optional. Repeated preparation updates derived inputs while preserving authored manuscript, outline and style. A unit can be exported with its referenced definitions, conventions and source locators. For Minimal, read the short runtime adaptation first and the original rules.v22 once; knowledge-only work skips the layout rules. The article uses 11pt body text, margins of at least 20mm and substantive diagram text of at least 10.5pt, with at most six main pages including title and graph and a separately started bibliography. Actual builds record main and total pages; TeX-only does not claim measured page counts.

```text
Use $pure-math-survey in this session. Read [fixed source/version], study [scope]
for [reader], and write one English Minimal from the same canonical KB statements.
```

For knowledge-only, say “Build the KB only; do not create a manuscript or PDF.” For TeX-only, request editable TeX and state that PDF/page counts are unmeasured. Thematic, Lecture, Paper and non-integrated views are explicitly unsupported. Schema 2.x projects are incompatible and remain unchanged when rejected; adding the runtime contract does not convert them to schema 3.0.0. Automatic migration is not provided.

This version removes runtime review/dispatch workflows and excludes retired modes and their resources from the installer. These are workflow and resource changes, not measured token or percentage savings. Without independent records, per-article model identity, token usage and complete elapsed time are null or unavailable; build/test timings do not measure the whole article workflow.

## Candidate installation

Python 3.10+ is required. Build the current candidate from this checkout:

```sh
python3 skills/pure-math-survey/scripts/package_release.py --output ../pms-install-check/pure-math-survey-2.4.1.zip
python3 tools/verify_release.py ../pms-install-check/pure-math-survey-2.4.1.zip --report ../pms-install-check/verification.json
```

The verifier checks the archive and hashes, extracts into a clean no-pip virtual environment, runs applicable engineering tests and a neutral Minimal TeX smoke. It checks software behavior; a particular paper still needs truthful source-grounded content and actual build measurements. PDF checks need pdfLaTeX, BibTeX and the style's TeX packages plus Poppler; `--no-build` reports incomplete verification rather than claiming a PDF build.

When receiving a ZIP, compare its SHA-256 with the adjacent `.zip.sha256` before extraction. Place the complete extracted `pure-math-survey/` in the host's skill directory, retaining any previous installation separately. GitHub's automatic Source code ZIP is not an installer. Candidate generation and successful verification do not mean a tag or release has been published; see [GitHub Releases](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases) for publication facts.

Read [the skill entry](skills/pure-math-survey/SKILL.md) and [minimal runtime](skills/pure-math-survey/references/minimal-runtime.md) for commands, storage and delivery boundaries. Source bytes keep their original rights; source access alone does not permit redistribution. Code, instructions and templates use the [MIT License](LICENSE).

Development only: [2.4.1 guide](docs/development/v2.4.1/DEVELOPMENT_GUIDE.zh-CN.md), [stage workflow](docs/development/v2.4.1/PR_WORKFLOW.zh-CN.md), and [current development state](docs/development/v2.4.1/DEVELOPMENT_STATE.yaml). These files are excluded from the installer and are not runtime readings. The candidate is development work, not a formal 2.4.1 release. A development sample or engineering check does not establish universal mathematical correctness.
