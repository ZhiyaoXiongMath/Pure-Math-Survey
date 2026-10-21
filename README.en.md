# Pure Math Survey

[简体中文](README.md) | **English**

Current development candidate: **2.4.1-dev.2**, policy `minimal-transition-pr02`, runtime contract `minimal-lean-2.4.1`. This PR02 candidate supports **Minimal writing and knowledge-only work in the current session**. It is not a 2.4.1 release. The transitional KB/snapshot schema is 2.0.0 and output schema is 2.2.0; the lean schema and final rules.v22 layout remain later stages.

Use fixed mathematical sources to build canonical knowledge and reuse those exact statements in an English Minimal. The supported structure is Main Results, Key Mathematical Ingredients, and Connecting the Ingredients. Keep complete assumptions and conclusions, define core concepts, attribute borrowed content accurately and explain the decisive connections briefly. No particular model, child chats, reviewer roles, review records or paired fast/slow manuscripts are required.

```text
Use $pure-math-survey in this session. Read [fixed source/version], study [scope]
for [reader], and write one English Minimal from the same canonical KB statements.
```

For knowledge-only, say “Build the KB only; do not create a manuscript or PDF.” For TeX-only, request editable TeX and state that PDF/page counts are unmeasured. Thematic, Lecture, Paper and non-integrated views are explicitly unsupported. Existing projects without the new runtime contract remain unchanged; automatic migration is not provided.

## Candidate installation

Python 3.10+ is required. Build the current candidate from this checkout:

```sh
python3 skills/pure-math-survey/scripts/package_release.py --output ../pms-install-check/pure-math-survey-2.4.1-dev.2.zip
python3 tools/verify_release.py ../pms-install-check/pure-math-survey-2.4.1-dev.2.zip --report ../pms-install-check/verification.json
```

The verifier checks the archive and hashes, extracts into a clean no-pip virtual environment, runs applicable engineering tests and a neutral Minimal TeX smoke. It does not certify a paper's mathematics or final PR04 layout. PDF checks need pdfLaTeX, BibTeX and the style's TeX packages plus Poppler; `--no-build` reports incomplete verification rather than claiming a PDF build.

When receiving a ZIP, compare its SHA-256 with the adjacent `.zip.sha256` before extraction. Place the complete extracted `pure-math-survey/` in the host's skill directory, retaining any previous installation separately. GitHub's automatic Source code ZIP is not an installer. Candidate generation and successful verification do not mean a tag or release has been published; see [GitHub Releases](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases) for publication facts.

Read [the skill entry](skills/pure-math-survey/SKILL.md) and [minimal runtime](skills/pure-math-survey/references/minimal-runtime.md) for commands, storage and delivery boundaries. Source bytes keep their original rights; source access alone does not permit redistribution. Code, instructions and templates use the [MIT License](LICENSE).

Development only: [2.4.1 guide](docs/development/v2.4.1/DEVELOPMENT_GUIDE.zh-CN.md), [stage workflow](docs/development/v2.4.1/PR_WORKFLOW.zh-CN.md), and [current development state](docs/development/v2.4.1/DEVELOPMENT_STATE.yaml). These files are excluded from the installer and are not runtime readings. PR03's lean KB and PR04's six-page layout are not completed by PR02.
