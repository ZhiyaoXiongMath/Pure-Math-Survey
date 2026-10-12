# Time compactness: real rc2 review project

This is a source-based English review of linear, nonlinear-image and seminormed-cone time compactness. It uses actual original-text readings of Simon, Maitre and Barrett–Süli. The source and mathematical evidence is author rereading, not an independent referee report. No original research result or real-reader study is claimed.

The final common snapshot is `KB-3bafc0dd9e16bd6dd56aa1c6d5dd1db62474438465f10ef1a7f448232611bd4d`. The outputs have the same question, three complete principal statements, two decisive boundary examples, and comparison group `time-compactness-three-routes`.

| Output | Profile and view | Reading priority |
| --- | --- | --- |
| `thematic` | Thematic / integrated | Which spatial information produces compact interval integrals, and how the three routes compare |
| `minimal-methods` | Minimal / methods | Finite nets, nonlinear truncation, two-point normalization and the order of parameter choices |
| `minimal-boundaries` | Minimal / boundaries | The failed endpoint, compact image versus input, and the exact assumptions needed for a transfer |

Each output has its own `plan.json`, `outline.md`, `manuscript/main.tex`, generated canonical statement fragments, material bindings and located semantic evidence. Compiled PDFs and rendered pages, when distributed in the candidate bundle, are under `outputs/ID/build/` and `outputs/ID/evidence/pages/`. Build and render success do not alone constitute acceptance; inspect the current release assessment and actual review records.

The KB contains fifteen readable nodes under `knowledge/nodes/`. The useful entry points are `N-question`, `N-simon`, `N-maitre`, `N-cone`, and the four construction nodes `N-linear-mechanism`, `N-truncation`, `N-cone-mechanism`, `N-homogeneous-transfer`. The exact imported Simon interval-integral criterion is its own canonical node. Every promised mechanism step has an individual output-semantic finding pointing to the derivation body.

`evidence/source-checks/` records actual passages read, controlling versions, version discrepancies and a scoped unresolved justification in Barrett–Süli's proof. The cone argument in this project uses an explicit local reconstruction, so that passage is not silently accepted. Raw PDFs were downloaded transiently and read; actual SHA-256 values are recorded, but the PDFs are not redistributed and cannot be rehashed from this project alone.

The immutable two-paper snapshot is `KB-65fc06042750df321560ad25b06d2d673de9361427293a7ae190ff4ad0ee694c`. The third source added five nodes and a substantive cone/image comparison. A subsequent wording correction created a new snapshot and new reviews. `outputs/initial-two-paper/` is the preserved initial plan, not a claimed initial publication. Its snapshot, plan and original reviews were not migrated to the new result. The CLI increment diff and the preserved plan fingerprint are documented under `docs/rc2/real-acceptance/` in the repository.

To reassess an output from the repository root:

```sh
python skills/pure-math-survey/scripts/survey.py output validate examples/rc2/projects/time-compactness --output thematic --stage release --json
```

Use `minimal-methods` or `minimal-boundaries` for the paired views. A new build is reproducibility evidence; it does not inherit visual acceptance for changed PDF bytes.
