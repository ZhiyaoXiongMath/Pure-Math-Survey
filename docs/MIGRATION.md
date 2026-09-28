# Moving to Survey v2

Install the complete v2 skill folder; do not combine individual files from
different releases. Keep existing mathematical projects until an explicit import
has been inspected. A host's installed skill and its knowledge projects are
separate directories.

For a v1 project containing project-manifest.json:

```sh
python skills/pure-math-survey/scripts/survey.py migrate --from OLD_PROJECT --output NEW_PROJECT --json
```

NEW_PROJECT must not exist. Import preserves original files and creates
unassessed candidates, not accepted mathematical knowledge. Reconstruct scope,
read sources, resolve identities, review coverage and freeze a new snapshot
before preparing formal outputs. Old PASS fields never become new approval.

For native scope-based 2.0.0/2.0.1 projects, the data schema and frozen byte
identities remain unchanged. An existing valid prepared output continues to
validate. If MATERIALS_CHANGED is reported, inspect the path: edit authoritative
knowledge and freeze a new snapshot when the content should change, or explicitly
prepare again to restore disposable copies. Preparation preserves manuscript and
outline; adopting new knowledge still needs semantic rereading.

The two historical development archives both labeled 2.0.0 used different review
contracts. Use `kb format PROJECT`; foreign checks-based projects require
`import-v2 --from OLD --output NEW`. Do not translate accepted fields manually.

v2 has three profiles: minimal, thematic and lecture. The default requested
output is minimal + integrated. The former Parts I--IV are overlapping knowledge
views, not four mandatory manuscripts; a knowledge-only request has no output.
This release does not include a Research Studio bridge or claim native Studio
import compatibility.

For long nested histories on Windows, use a shallow project/staging path within
the path-length limits of the filesystem and external TeX tools. The clean-install
verifier accepts `--work-directory SHORT_PATH` and uses a short temporary prefix.
