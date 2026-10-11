# vNext requirement-to-implementation record

Candidate **2.1.0-rc1**, policy `four-modes-2026-10-11-r2`.
Authoritative input: `Pure-Math-Survey_vNext_Integrated_Development-Guide_2026-10-11_r2(2).md`, supplied 2026-10-11, SHA-256 `2e8c5ab518cc40f62a2085ec573ac3c53c81ad9cf53e0fefe9e38f2d35420188`.
The whole specification was read. The starting main was `f663027822fb13a02d319167fd5e5e68456876c2` (2.0.4, KB schema 2.0.0), confirmed through GitHub rather than inferred from the guide.

## Status vocabulary

**IMPLEMENTED** identifies actual code or installed rules. **TESTED** means the named executable check ran. **REVIEWED** means an actual reading, with scope; here all mathematical and page readings are **author_reread**, not independent review. **NOT VERIFIED** is not a pass. **BLOCKED** identifies an intentionally failing publication gate or an unresolved dependency. Synthetic accepted test records prove only gate behavior.

## Architecture and compatibility decisions

Retain the existing single-writer file architecture, dependency closure, evidence, immutable snapshots, literal canonical imports, authoring-material integrity, build history, render and package mechanisms. Add one small `survey_core/profiles.py` policy module; it owns versioned mode contracts, not mathematical facts. No database, Web UI, scheduler, graph store, `output_kind`, or alternate knowledge authority was added.

Knowledge/project/node/source/snapshot formats remain **2.0.0**. New plans and policy-bearing reviews are **2.1.0**. Other existing review kinds remain readable. The new reader accepts legacy 2.0.0 plans under `legacy-2.0.0`; no on-read mutation or automatic reacceptance occurs. Old 2.0.4 software cannot parse new plans or new policy-bearing review records, including such reviews embedded in an otherwise 2.0.0 snapshot. This is backward reading by new software, not forward compatibility or a downgrade facility.

New `output plan` uses the new policy; it never edits an existing plan. To adopt it, create a new output ID against the chosen fixed snapshot and perform new reviews. Repair deficient canonical statements in live KB, review and freeze a new snapshot; retain the old snapshot and output. `prepare` preserves authored `main.tex`, style and edited `outline.md`. Historical validation reports its legacy policy; it does not assert vNext compliance. No in-place migration command is needed or claimed.

## Complete requirement map

Paths below are relative to `skills/pure-math-survey` unless prefixed `tests/`, `tools/`, `examples/`, or `docs/`.

| Guide requirement | Actual implementation / evidence | Status and limit |
|---|---|---|
| §1.1, §15.1, §19: retain infrastructure; lightweight skill | Existing modules reused; `scripts/survey_core/profiles.py` is only new runtime module | IMPLEMENTED; TESTED legacy tests |
| §1.2–1.3, §13: modes distinct from views and length | Models/CLI four profiles; goals, proof defaults, outline, templates and per-mode review keys differ; same-spine grouping remains opt-in | IMPLEMENTED; TESTED V01–V03, V10, V24 |
| §2: replace generic audience/outline behavior | Capability-based audience seed, explicit pending editorial work; actual per-mode sample plans and outlines | IMPLEMENTED; TESTED V01–V02; REVIEWED samples |
| §3.1–3.7: four typeset lines, substantive displays, exceptions | `writing-style.md`, SKILL, common `display_rhythm` reading and existing visual reviews; no formula quota/automatic insertion/typography shrink | IMPLEMENTED rules; REVIEWED all 16 sample pages; arbitrary prose-line inference NOT IMPLEMENTED by design |
| §4.1: objects, domain, data, assumptions, equations, quantifiers, conclusion, status, local definitions | Nine principal-reading aspects, canonical SHA binding; pending KB template via `review template ... --principal-statements`; output reading also required | IMPLEMENTED; TESTED V12–V16, V31; REVIEWED actual main statements |
| §4.1.3: supporting/local statements, legitimate references | Principal-only advisory risk scanner; proof `eqref` allowed; local technical context is not globally forbidden | TESTED V11 and actual compactness lemma |
| §4.1.4: surrounding prose cannot strengthen theorem | Separate located `statement_context` semantic finding, not a hash-based truth assertion | IMPLEMENTED; TESTED rejected semantic fixtures; REVIEWED actual scope/quantifiers |
| §4.2: canonical single authority | Existing node→snapshot→exact fragments preserved; actual norm defect repaired in KB and new snapshot, not output-only rewrite | TESTED integrity regressions, V35, authored norm-history test; REVIEWED |
| §5: faithful fast path, decisive conditions, slow details | Common fast_path/points/connections/limits findings and explicit per-step review locations | IMPLEMENTED; REVIEWED all six known-math articles |
| §6: functional baseline, three roles, backward/forward selection, grain | New installed `reader-calibration.md`; output outline inventories and reader goals; per-use rather than permanent node difficulty | IMPLEMENTED; REVIEWED sample outlines; real-reader experiment NOT VERIFIED |
| §7.1–7.5: overview readable, multiple premises, no second authority | New `references/overview.md`, architecture rules, init seed; sample maps contain precise mechanisms and node/section entrances | IMPLEMENTED; REVIEWED sample maps |
| §7.6–7.8: project map ≠ output outline, detail entrances, shared-file binding | Existing `consume_overview` and file-level hashes retained; mode outlines select a route without rewriting overview | IMPLEMENTED; TESTED old shared-input regressions; no paragraph-level invalidation claimed |
| §8: Target/Audience/Principals/Points/Connections/Limits design | Mode-specific outline with snapshot, selected IDs, proof obligations and editorial inventory; no second canonical statements | IMPLEMENTED; TESTED V01; REVIEWED authored contracts |
| §9: Minimal strictly three actual sections | Literal expanded body inspection, exact titles/order, no extra unnumbered math section, numbering-reset checks, formal principal in first section; separate principal/ingredient template insertion | IMPLEMENTED; TESTED V03–V10; REVIEWED both complete Minimal articles |
| §9.2–9.4: genuine points/decisive connection, not tool list | Exact square/inverse interfaces and positivity closure; exact compactness/margin interfaces and admissible F-limit; located point_use and decisive_connections | REVIEWED actual calculations; synthetic failures test rejection mechanics only |
| §10: mathematical questions/routes/supported synthesis | Thematic outline and question/approach/comparison/synthesis review; canonical comparison relations and source/dependency checks retained | IMPLEMENTED; REVIEWED Schur congruence/minimization comparison and one-route compactness synthesis |
| §10.2, §17.3: do not invent another route | One-route example explicitly compares equivalent margin controls, not imaginary competing theories | REVIEWED; TESTED flexible sections V10 |
| §11: motivate, teach, expand promises, explicit imports | Lecture complete-proof default/pending steps; actual per-step source locations and findings; declared imported interfaces | IMPLEMENTED; TESTED V02, V20–V22, V31; REVIEWED expansions and assumptions |
| §12.1–12.3: independent Paper contribution contract | Every principal classified; original authorization/provenance, prior-result IDs, canonical comparison IDs, actual difference, closure/gaps; prior/comparison nodes join consumed closure | IMPLEMENTED; TESTED V25–V40 |
| §12.3: prior-art reading, not automatic novelty | Versioned source readiness plus actual dated searches, scope/locators/source bindings and concrete contribution findings | IMPLEMENTED gates; TESTED synthetic positives/negatives; genuine novelty NOT VERIFIED |
| §12.4–12.5: complete proofs, true imports, no gap laundering | Original principal must be established, direct complete obligation/selection, no gaps and suitable proof closure; rejects conjectural/open/refuted required proof input; supplied provenance checked | IMPLEMENTED; TESTED Paper adversarial cases |
| §12.5, §13.2: internal draft isolated | Paper defaults draft; marker checked in body; formal marker contradiction rejected; boolean flip alone cannot pass contribution/readiness/semantic gates; package denies draft | TESTED V25–V40 and actual known-theorem Paper draft BLOCKED |
| §13: KB-only/no unsolicited modes | Init/freeze still produce no manuscript; only requested profile generated; views not profiles | TESTED legacy suite, V24 and isolated install |
| §14.1–14.7: input freeze, write, fast/slow reread | Readiness→prepare scaffold→actual authored sources→source-bound readings; prepare never claims to author/understand | IMPLEMENTED; REVIEWED seven source manuscripts (Paper reading rejects formal claims) |
| §14.8–14.9: actual compile/render/page observations | Existing build/render/history; six local release-ready outputs and one internal draft; 16 actual inspected pages | TESTED real builds; REVIEWED recorded pages; CI rebuilds explicitly NOT new visual readings |
| §15.2: all named references and installation rules | SKILL, editions, writing-style, introduction, proofs-and-boundaries, architecture, output-review, exposition-examples, contracts; new reader-calibration/overview; bilingual READMEs and agent prompt synchronized | IMPLEMENTED; TESTED resource allowlist and extracted install |
| §15.3–15.4: actual pipeline and responsibilities | models/plans/exports/readiness/release/CLI integrated; four real templates; semantic checks require located substantive findings, not new automatic mathematical labels | IMPLEMENTED; TESTED positive/adversarial suites |
| §15.5: explicit schema/read policies, old evidence protection | Output/review 2.1 compatibility reader; explicit legacy report; new ID adoption; preserved old manuscripts, snapshots and reviews | TESTED legacy and V16–V19; examples retain canonical-repair history |
| §15.6: no quotas/extra DB/unimplemented commands | One lightweight policy layer; only Minimal section count hard gate; source resources explicitly allowlisted | IMPLEMENTED |
| §16.1–16.5: mechanical checks separate from mathematical/visual readings | Located common/mode/step/principal observations; exact inputs; explicit page findings; no mathematical inference from formula or character count | IMPLEMENTED; REVIEWED author scope only |
| §16.6–16.7: honesty and severity distinctions | Existing author_reread/independent_review meanings; warnings vs blockers; no real-reader or independent claim | REVIEWED status records; independent/reader feedback NOT VERIFIED |
| §17.1, §17.8: transparent + specialized end-to-end examples | `examples/vnext/projects/{schur,compactness}`: Minimal/Thematic/Lecture each; known-theorem Paper boundary draft only | TESTED source relocation/build; REVIEWED local author versions; real original Paper NOT VERIFIED |
| §17.2–17.3, §17.6: adversarial/compatibility tests | `tests/test_vnext.py` 42 tests plus 84 historical tests, `tests/test_vnext_examples.py` 2 actual-source regressions | TESTED; semantic rejection fixtures do not pretend to automatically detect bad mathematics |
| §17.4–17.7: reverse reading, DoD, honest software evidence | Actual source and page records; validation report below; no synthetic acceptance promoted to math evidence | REVIEWED author reread; full original-Paper quality still NOT VERIFIED |
| §18 A–E: concrete deliverables | A installed contracts; B authored source+reviews; C runtime integrations; D guarded Paper; E tests/ZIP/CI/PR/evidence | Implementation present; remote execution status recorded in PR, not inferred |

## DoD conclusion

The engineering implementation and six known-mathematics author-reviewed benchmarks implement the requested policy. The nine §17.5 areas have executable or actual-reading evidence, subject to the guide's explicit §17.1/§17.8 original-Paper exception. **Do not claim unrestricted full mathematical-product acceptance**: there is no genuine authorized original research paper, independent mathematical review, or measured target-reader comprehension experiment. Paper formal research quality remains **NOT VERIFIED**, and the supplied classical Paper fixture remains **BLOCKED**. No main merge or formal software Release is authorized by this record.
