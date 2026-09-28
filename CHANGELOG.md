# Changelog

## 2.0.2

The first public v2 release replaces article-first planning with a reusable,
source-grounded knowledge project and immutable snapshots. Requested output
defaults to minimal/integrated; thematic and lecture are explicit alternatives.
Knowledge-only and update-only work creates no manuscript. Existing v1 projects
have an explicit, non-overwriting migration path and retain their original bytes.

The final patch validates every supplied authoring material against its fixed
snapshot, including member sets, copied reviews and manifests. Altered, missing
or extra materials fail before structure validation, building or release.
Explicit reprepare restores copies without replacing authored manuscript/outline.

UTF-8 legacy scope migration, isolated legacy command imports and Windows test
capability handling were corrected. Software version is 2.0.2; immutable data
schema remains 2.0.0. The release adds reproducible behavior tests and Linux CI
for Python 3.10 and 3.12. The separate Schur-complement example records actual
source reading, knowledge-only updates, two reviewed outputs and change impact.

The 2.0.0/2.0.1 development stages also added body-aware TeX checks, exact review
locations, scoped review-change impact and immutable build/render history.
Tests and hashes never certify mathematical truth or independent peer review.

## 1.8.1

The previous public release remains available under tag v1.8.1, including its
original skill archive and the legacy five-part concise/standard workflow.
