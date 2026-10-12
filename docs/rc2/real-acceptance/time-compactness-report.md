# Real time-compactness project: author handoff

Authoring and actual scoped rereading completed on 12 October 2026. Project: `examples/rc2/projects/time-compactness`. This report records work actually performed, including limitations and blocked attempts; it does not substitute for the root reviewer's separate PDF-page inspection or the final installed-resource verifier.

## Original sources and controlling versions

| Source | Controlling text and actual mathematical reading | Exact principal/mechanism locators |
| --- | --- | --- |
| Simon, *Compact sets in the space Lp(0,T;B)* | Journal text, Ann. Mat. Pura Appl. 146, 65–96, DOI `10.1007/BF01762360`. Publisher metadata gives December 1986; later references often give 1987. Original scan plus searchable original-text mirror were used, with scanned relevant pages visually checked. | Theorem 1 and proof, pp.71–73; Lemma 4, pp.77–78; Theorem 3, p.80; Lemmas 8–9/Theorem 5, pp.84–85; Corollary 4, pp.85–86; Proposition 3, p.94. |
| Maitre, *On a nonlinear compactness lemma in Lp(0,T;B)* | Published IJMMS 2003:27, 1725–1730, DOI `10.1155/S0161171203106175`; all six pages of mathematical text read. The arXiv predecessor is not the controlling version. | Theorem 2.1/Remark 2.2, p.1726; all of Lemma 2.3 and equations (2.3)–(2.24), pp.1726–1730; Corollary 2.4, p.1730. |
| Barrett–Süli, *Reflections on Dubinskii's nonlinear compact embedding theorem* | arXiv `1101.1990v2`, submitted 16 April 2011, 17 pages; original text pp.1–16 read, references used for discovery. Later journal pagination is not controlling. The internal November 2018 date differs from the arXiv submission metadata; its cause was not verified. | Definitions pp.2–3; Theorem 1/Remarks pp.3–4; complete Lemma 1 proof pp.4–5; Lemma 2 route pp.5–12; final proof/(2.22), pp.12–13; Section 3 pp.13–15; all of Section 4 pp.15–16. |

Original URLs are retained in each source record. Transient PDFs remain at `/workspace/scratch/9681b76018b6/compactness-sources/{simon,maitre,barrett-suli}.pdf` for the root's separate inspection. The PDFs were successfully downloaded and read, not inaccessible. They are not redistributed in the repository or snapshots; `local_path:null` expressly prevents a claim of project-local raw-byte rechecking.

| File | Actual downloaded SHA-256 |
| --- | --- |
| `simon.pdf` | `fa84da0e9869e20d7dd6e51b26366cba7f4a8e67cbc7e7f1556f1a3555f73608` |
| `maitre.pdf` | `e03a0c0a623cad7feb67d2961ffbf89fda8d3a08353c02266ad3020d18e89362` |
| `barrett-suli.pdf` | `030e553efcf2a73b25da62b744f03300dc7827f8bc2f9953112b90751082b2f1` |

The original Chen–Liu 2012 paper was also accessed during the omission challenge (Theorem 1, p.2253). It is a discovery lead, not a fourth imported theorem in the frozen corpus. The manuscripts therefore make no strongest-known or necessity claim for Maitre's auxiliary `r>1` hypothesis. Later nonlinear/discrete extensions remain outside the bounded review. Full own-word reading notes are under `evidence/source-checks/`; no copied full source text is bundled.

## Actual increment and immutable history

1. Simon and Maitre: ten nodes, actual source/math/coverage reviews, snapshot `KB-65fc06042750df321560ad25b06d2d673de9361427293a7ae190ff4ad0ee694c`. The initial output is a ready plan and outline, not a claimed built/reviewed manuscript.
2. Barrett–Süli: added `N-cone-definition`, `N-cone`, `N-cone-ehrling`, `N-cone-mechanism`, and `N-homogeneous-transfer`. This adds positive-cone geometry, a two-point upgrade, a locally reconstructed weak-space argument and a restricted comparison with Maitre. Increment snapshot: `KB-208032d0e85fbb7b2b1f504697e203afc1903848c9f1279d2238d816200a133e`.
3. Corrected an unverified explanation of the PDFs' internal 2018 dates: the notes now state the observed discrepancy without asserting a regeneration cause. New source/math review records and final snapshot `KB-3bafc0dd9e16bd6dd56aa1c6d5dd1db62474438465f10ef1a7f448232611bd4d` were created; no old accepted record or snapshot was rewritten.

The actual CLI diff is `time-compactness-increment-diff.json`. It identifies the five added nodes, third source, coverage/discovery/review changes and affected initial plan. Because the initial output was only a plan, it truthfully reports no authored manuscript locations. It does not silently adopt the new snapshot. The initial plan SHA-256 is still `2f2bca2745f440be0620b86c6678764c155e46752850d1f976a0cf0b7819bf8b`, matching the pre-increment fingerprint file.

## Mathematical content and view comparison

All final plans bind the final snapshot, `N-question`, principals `N-simon`, `N-maitre`, `N-cone`, and boundary nodes `N-endpoint`, `N-image-only`; the nonempty comparison group is `time-compactness-three-routes`. All three full principals are literal generated canonical inputs. The cone statement repeats its own gauge axioms, and all statements specify uniform quantifiers, measurable unknowns, exact norms and exponent ranges.

The manuscripts derive linear compact interval averages and an Ehrling Cauchy upgrade; nonlinear input truncation, the retained `K(0)` tail, compact convex averages and the target-exponent Simon application; a two-point cone normalization and gauge truncation in the weak derivative space; and a homogeneous-map overlap with the explicit inverse-gauge and inverse-lift bound. The same source-supported comparison checks `alpha>=1`, injectivity, inverse-lift measurability and equality of derivative/output spaces. It is not called an equivalence of the three theorems.

The decisive limits are calculated, not merely named: the ramp has derivative L1 norm one and finite-p error `1/(n(p+1))` but no L-infinity compactness; dyadic signs have pairwise L1 distance one while their squared images are identical. These have different force from losing the small factor in a particular r>1 tail estimate.

| Output ID | Actual organization and emphasis | Author semantic evidence |
| --- | --- | --- |
| `thematic` | Four questions: controlled unknowns; compact interval averages; why two cone points; verified overlap and limits. A comparison table makes the norms and unknowns explicit. | `evidence/author-semantic.json` |
| `minimal-methods` | Exactly three main sections. Finite-net averages, two-point normalization and derivative moduli precede the constructions; the order of tail/eta and finite-net/index choices is explicit. | `evidence/author-semantic-bibgroup.json` |
| `minimal-boundaries` | Exactly three main sections. Ramp and sign examples come before the interfaces; later comparisons audit necessity claims, inverse measurability and derivative/output norm matching. | `evidence/author-semantic-bibgroup.json` |

The reader is an early doctoral PDE analyst able to use Bochner integration, Hölder, Minkowski and the W11 fundamental theorem, but not assumed to know nonlinear Aubin–Lions arguments. The exact Simon criterion is imported, stated and cited; the nonlinear bridges are developed. Each output's actual author reread contains the seven whole-manuscript checks, isolated full principal readings, view/design findings and 18 individual proof-step findings with derivation-body locations. These assertions are scoped author readings, not independent review or a real-reader study.

## Scoped source-proof limitation

In Barrett–Süli v2, the passage after (2.8), p.6, selects an index depending on time and then uses a fixed-index integral bound; the author reading did not find the required justification in that passage. The nested-subsequence description on p.8 also needs a diagonal interpretation. These are unresolved justifications of those passages, not claims that the theorem is false.

The manuscript does not use them. Its local cone reconstruction obtains an A1 supremum bound from the gauge and Bochner derivative, controls the gauge-truncation tail using that amplitude, proves compact interval integrals via compact convex averages, applies the exact Simon criterion with the permitted time exponents, and only then uses the verified two-point Ehrling upgrade. The p-infinity representative extension is also given. The root separately read and checked this reconstruction before page review; no independent-review designation is inferred.

## Build, review and runtime observations at author handoff

All three outputs reached `BUILT`, eight pages each, and `RENDERED_NOT_REVIEWED`. Root subsequently inspected the pages separately and requested a bibliography grouping fix in both Minimal outputs. The requested `clearpage` before each bibliography was applied, both were rebuilt/rendered, and new SHA-bound author semantic records were appended. Earlier accepted author records and build/render histories remain intact.

At the author's final release checks, all three had `READY` knowledge evidence and valid current semantic readings. The only release error was `VISUAL_REVIEW_INCOMPLETE`, awaiting the separate root visual record. Warnings accurately state `SOURCE_RAW_BYTES_NOT_RETAINED` and `NO_INDEPENDENT_REVIEW`. No formal package, final visual acceptance or installed-verifier success is claimed by this report; root owns those completion steps.

The actual initial canonical-block error, overflow build, repeated verified stale locks and stale staging cleanup are recorded in `time-compactness-authoring-log.md`; file inventories of removed live temporary directories are in `time-compactness-staging-cleanup.json`. The cause of leftover locks/staging was not established. Runtime, tests, old projects and GitHub were not modified by this author.

## Root completion after author handoff

All 24 final rendered pages were actually opened by the root, with page-specific
findings in each output's `evidence/root-page-review.json`. After the bibliography
fix, final pages 7–8 were reopened for both Minimal outputs; pages 1–6 were
verified byte-identical to the already opened images. All three current-policy
release assessments now return RELEASABLE, with no errors. The expected source
retention and NO_INDEPENDENT_REVIEW warnings remain. The actual package gate
created all three reviewed output ZIPs. See `time-compactness-release.json`.

The root also rechecked the full manuscripts' distinct emphasis and common
canonical spine. This is scoped model/author review within development, not an
independent human mathematical audit or target-reader experiment. Source PDFs
are intentionally not redistributed; exact source URLs, versions, hashes,
locators, own-word reading notes and scoped limitations are included.
