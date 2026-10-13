> Historical development record: all policy claims, artifact paths, results and command transcripts below apply to that earlier revision. Removed examples/reports/tools remain in Git history or private backups; they are not current instructions, answer inputs or r4 acceptance. Follow [current product workflow](../r4/workflow.md) for new work.

# Validation record — 2.1.0-rc1

Date: 2026-10-11. This record distinguishes actual author work from deterministic reruns. GitHub commit/check identifiers belong in the PR; do not treat a local test as a completed remote check.

## Actual local execution

The unmodified downloaded baseline passed all **84** tests with local TeX/Poppler. The implementation then passed **124** tests (84 historical plus 40 new policy tests). Actual benchmark use exposed a further review-selection defect; its fix added V41–V42, giving 126. Two authored-example regressions raise the final suite to **128**; the final local run passed **128/128 in 31.401 seconds**. The full isolated installation passed and rebuilt/rendered all seven PDFs using only installed modules. Remote CI remains a separately reported run.

`validate_assets.py` exercises all four installed templates/entry paths. `package_release.py` reopens the ZIP, checks its explicit member whitelist, SHA-256 manifest, CRC, single-root layout and font exclusion. `tools/verify_release.py` imports every module from an extracted installation in an isolated no-pip virtual environment. Its full path now rebuilds all seven authored examples with the installed runtime; `--no-build` reports external build work unexecuted rather than passing it implicitly.

`tools/verify_vnext_examples.py` copies rather than mutates the committed source projects, verifies every old/new snapshot, literal canonical/material integrity, actual stored author-semantic bindings, six ready known-math outputs and the nonreleasable Paper. Its fresh builds/renders are **NOT new visual reviews**. It never creates accepted semantic or visual evidence.

## Actually written, compiled and read

| Module | Minimal | Thematic | Lecture | Paper internal |
|---|---:|---:|---:|---:|
| Classical Schur complement | 2 pages | 2 pages | 2 pages | 2 pages, deliberately BLOCKED |
| Conditional Hölder compactness and admissible limit | 2 pages | 3 pages | 3 pages | Not generated |

All **16 pages** of these seven local PDFs were opened and read at normal typography. The six known-mathematics outputs have accepted **author_reread** semantic and PDF/image-bound visual records and pass the existing complete `RELEASABLE` gate. The Paper's formal semantic review is `revise`; its visible notice and actual no-novelty scope remain. The final evidence bundle preserves actual builds, source hashes, page images, observations and history. Source-only fixtures deliberately omit orphaned visual approval for PDFs they do not contain.

Actual author checks reconstructed the result/points/connection route before the detailed proofs. For Schur, square completion and the inverse map deliver the two positivity directions; congruence and minimization are compared under their actual common assumptions. The Lecture expands the cross terms, inverse and nonzero cases. For compactness, the uniform bound supplies strong C2,beta subsequential convergence; the same positive delta supplies admissibility; only then does continuity close F=0. The Lecture expands diagonal/finite-net extraction, derivative compatibility and the interpolation estimate. The thematic article admits one genuine route rather than inventing competitors. Counterexamples evaluate A=-1, u_j=1/j, and a nonvanishing top-alpha seminorm explicitly.

The guide was the supplied provenance source. The elementary and conditional claims were independently derived and reread by their author; this is not an external historical priority search. No supplied guide, classical theorem, fixture or author's proof was relabeled an original research contribution. No live research prior-art review was performed.

## Failures actually found and repaired

| Failure | Cause and correction | Evidence |
|---|---|---|
| Initial audit Actions: 3 errors | Temporary audit job lacked pdflatex (ordinary CI already installed it). Add explicit TeX/Poppler installation; retain failure logs | Initial run 38113286094 / job 114393093631; not counted as baseline code failure |
| Resource/isolated-install failures | New references were initially absent and legacy version/profile assertions still expected 2.0.4/three profiles | Add real files to whitelist; assert candidate version and all four actual preparation paths |
| Undefined local Q in Schur prose | Canonical square identity was correct but a neighboring use lacked a reminder | Add the quadratic-form definition at its first local use; rebuild and reread |
| Compactness supporting lemma split across pages | Assumptions and conclusion separated at a page break | Keep this supporting lemma together; no typography shrink or removed hypotheses |
| Missing exact Hölder norm at output entry | A pivotal convention was only explained locally rather than canonical | Add N-norm definition and dependency links to KB, review, freeze NEW snapshot; retain old snapshot; export exact fragment |
| Finite-net proof used v_j without explicit definition | Teaching proof's derivative sequence was tacit | Name the derivative sequence before the displayed inequality |
| Old mathematical review shadowed a valid new-mode proof reading | Candidate selection checked statement/bindings before later proof-step coverage | Require this plan's promised steps during candidate selection; try later valid reviews. V41–V42 test both success and continued blocking |
| First source-only relocation lost materials/evidence | Packaging filter accidentally omitted nested immutable authoring evidence | Filter only output-level evidence, retaining all materials; relocated verification then passed |
| Isolated verifier pointed at missing matrix-tree example | Old optional build path was unusable for this repository | Use the actual authored two-project suite with the extracted runtime; preserve explicit --no-build behavior |

All source/math changes were made before the final author records. Nonvisible plan/evidence refinements were followed by actual rebuilds/renders; the final image hashes matched the exact pages already inspected. Historical snapshot/build evidence was retained, not silently overwritten.

## Limits and nonclaims

**IMPLEMENTED:** four-mode runtime/rules/templates, policy-aware compatibility, guarded original-contribution and step-by-step semantic contracts, actual source fixtures and repeatable installation verification.

**TESTED:** local regression suite, actual builds/renders, integrity and rejection checks, snapshot relocation, installation/archive verification. Remote CI must be reported from its actual Actions result; pending does not mean passed.

**REVIEWED:** exact sample statements, neighboring prose, fast route, promised proofs and all local sample pages, by the author only. Software tests containing invented accepted records are clearly marked synthetic and do not constitute these readings.

**NOT VERIFIED:** a real authorized original Paper end to end, real-world novelty/completeness of a research prior-art search, independent mathematical review, real-reader understanding, host application installation on a user's machine, and arbitrary TeX execution semantics outside the supported literal-input model. The existing TeX parser remains a bounded inspector, not a general interpreter or a security sandbox.

**BLOCKED:** formal packaging of the classical/unverified Paper; pending principal self-contained readings, missing proof steps, missing contribution/prior-art records, stale evidence and unobserved new PDFs continue to fail their relevant release gates.

No automatic merge and no formal Release. The candidate label deliberately avoids presenting the permitted Paper validation exception as comprehensive research-quality acceptance.
