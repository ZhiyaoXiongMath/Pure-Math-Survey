# Concise and standard editions

The shared mathematical core starts with the problem model: intrinsic data, variable domains, unknowns, quantifier order and evidence for relationships between formulations. Standard deepens the same question; concise does not silently freeze a variable or hide a scope-defining answer in an optional consequence.


Both editions are English mathematical articles. The user's requested part/edition set governs delivery; a single edition is assessed against its own scope and sources, not against an invented counterpart. Paired editions share a part-specific mathematical core, not every supplementary topic.

## Invariants of common content

Keep the same source identity, controlling version, cutoff, notation, conventions and truth status. Every genuinely repeated or shared full statement uses the same body-only component and preserves objects, hypotheses, quantifiers, exceptional cases, range, conclusion and qualifications. Keep material uncertainty and citations with the claim. A narrower corollary or stronger theorem is a separate result with a justified relationship, not an editorial paraphrase.

A correct common component does not validate surrounding prose. Check comparisons, historical judgments, failed converses, prose consequences and Problem status separately. Different labels and numbering across documents are acceptable; meanings and sources must agree.

## Depth and selection

| Part | Concise preserves | Standard deepens |
|---|---|---|
| I | Necessary concepts, a completed core model and its bridge to the general question | Foundations, model arguments and revealing variations |
| II | Core results, relationships and substantive proof ideas | Comparisons, conditions and explanations, then useful supplementary results |
| III | Connected routes and substantive explanation of selected decisive mechanisms | Key derivations, supporting claims, dependencies and closure |
| IV | Meaningful uses, established boundaries and the agreed core Problems | Applications, progress, relationships, remaining ranges and evidenced difficulties |
| V | An independently readable result-and-proof structure: core statements, key lemmas, decisive short derivations and precisely cited difficult inputs | The same mathematical spine with fuller estimates, constructions, dependency explanations and useful comparisons |

Concise reduces reading burden through selection and organization. Start with its mathematical thread and principal section duties; merge local technical sections, omit side branches and empty reminders, and choose representative material. Preserve repetition that makes a theorem or its use self-contained. Test a suspected detour by removing or compressing it: can the intended reader still understand the selected results, their necessary conditions and the promised explanation? If yes, shorten or omit it; if not, retain or reorganize the needed bridge. This is an editorial test, not permission to delete promised core content or essential qualifications. Identical headings are not themselves a defect, and fewer pages are not themselves success. Do not achieve brevity through smaller type, tighter margins or lost hypotheses.

Both editions keep the core mathematical statement/lemma structure. Concise is not a prose abstract of standard: it compresses proof interiors, not result visibility. Standard is the more detailed edition for readers studying the techniques. No result count or page ratio defines the difference.

Both editions use short sentences, clear lists of mathematical conditions, compact core theorems and formulas in place of wordy paraphrases. Neither edition requires trivial transitions or narrative introductions. Secondary consequences belong after a principal theorem; use a separate corollary or proposition when the consequence merits independent use, rather than automatically turning it into prose.

Standard adds understanding before breadth. For a substantial addition, identify what it enables the reader to understand: the role of a hypothesis, a missing inference, a result comparison, a revealing example or the remaining range of a Problem. More citations or neighboring topics alone do not demonstrate depth. III's complete route and selected mechanisms must remain intelligible in concise; optional supporting proofs may be cited. V's method ideas must remain intelligible in concise, but V does not owe III's technical development in either edition. V standard does not automatically restore omitted technical proofs or all I–IV nodes.

For example, V concise can explain what a construction produces and how it supports a main result, while leaving a technical sublemma to a precisely located source; V standard can clarify why a key hypothesis is needed through a checked comparison. By contrast, copying every technical branch into concise and adding an unrelated bibliography tour to standard does not serve either edition. A short decisive derivation belongs in concise when omitting it would break the chosen explanation.

Record the main selection decisions and locations of added understanding briefly in the existing architecture/edition note. Do not make a new per-paragraph ledger, score, section quota or fixed length ratio. Use the non-blocking reading-length guidance in length-and-selection.md; record scope decisions in the existing architecture note. For a single requested edition, apply only its own test; do not create a counterpart.

## Coverage and placement

The [publication-map definition](records-and-delivery.md#mathematical-ownership-and-placements) is authoritative for fields and treatment rules. `FULL_STATEMENT` imports the canonical body at least once at its mapped primary location; useful local recalls may reuse that same body. Canonical identity is not a ban on repetition. `REFERENCE_ONLY` is a located explanation with usable local conditions and a reason for reduced treatment. `OMITTED_WITH_REASON` has empty file/label fields and a substantive reason; no component may still be imported at that omitted placement.

I–IV standard placements require full statements. Concise placements and both V editions may select among the three treatments within their own contracts. This placement choice cannot erase a selected principal answer or an essential lemma: keep its usable statement in the article, even when the proof is quoted or sketched. A referenced supplementary result is different from an unstated indispensable input. Standard-only supplements need not be forced into concise. Likewise, a technical III node need not be forced into V standard. V core main results or Problems may not be hidden through convenient omission or delegated to absent volumes. A reference must preserve the assumptions needed to use it within this document. Every map node has at least one requested full or referenced location; a completely unused node does not belong in the publication map.

An unrequested document uses `NOT_REQUESTED` and empty coordinates, separately for each owner or V edition. This is not a treatment for skipping content inside a requested document. A V-only selection can use I–IV-owned nodes without creating those volumes.

## Reconciliation review

First compare common bodies, conventions and sources, then check surrounding prose for altered logical force. Read concise alone and apply the selection test to actual passages: can the reader follow its selected central ideas without borrowing missing necessities from standard? Read standard for located added understanding, not just extra topics. Compare the introduction, major section roles and body to ensure that promised organization is real in each edition. Record any necessary local repair and its recheck in the existing `edition_depth` evidence; a shared outline or a page-count difference cannot settle the judgment.

For V, assess its independently chosen main-result understanding, method ideas and Problems under `reader_outcomes` and `edition_depth`. `proof_depth` describes the argument treatment actually used. Only a request including III requires `proof_framework` and `decisive_mechanisms`. Shared content with other delivered parts still needs reconciliation, but those other parts do not expand V's scope automatically.

IV editions keep their own agreed core Problems. V editions keep theirs; common IV/V Problems have identical mathematical conditions, sources and status. A narrow verified settled scope is explained rather than populated with fabricated Problems. A failed search or inaccessible source proves neither openness nor settlement.

## Introduction and presentation in each edition

Every requested edition must state its own selected principal conclusions in its introduction. Concise may select less technical depth within the agreed scope, but may not replace selected conclusions with names, citations or a roadmap. Standard may not defer the knowledge to the body simply because the body is longer. Necessary assumptions, quantifiers, exceptions and source qualifications survive compression. The body reference supplements rather than supplies missing introduction content.

Both V editions use [the Part V guide](part-v-benchmark.md). Concise selects within the agreed question; standard deepens decisive mechanisms before adding breadth. No sample dictates the organization or topic coverage.

Use the identical [layout profile](layout-and-build.md) across concise and standard and all five parts. Different pagination follows from real selection and exposition, never a reduced font, compressed line spacing or smaller margins. Recheck introduction/body coverage after edition-specific cuts. A single requested edition has its own complete review; do not invent a paired manuscript.

## Selection and discovery

Record common question IDs, result IDs, mechanism IDs and frontier IDs in survey_selection. Paired editions agree on these including scope/status, not merely bibliography. Their depth and local organization may differ. Standard does not automatically restore an alternative method. An unrequested standard article is not a completed paired test.

Every mapped principal answer belongs to `core_result_ids`; agreeing on an incomplete declaration is not shared-core agreement. The checker enforces this already declared role, not its mathematical importance. A standard-only secondary supplement is allowed when it does not replace or change the common questions, principal answers or decisive mechanisms.

## Applying the paired templates

The two templates for a Part demonstrate the same mathematical tasks. Replace their provisional headings with mathematical ones and delete inapplicable slots. Part I builds a model and its bridge; II compares precise formulations; III develops a construction and closure; IV separates established range, obstruction and authenticated remainder; V integrates selected reductions and mechanisms. Standard develops the same model calculation, comparison, decisive input, or obstruction at the point of use. It has no compulsory extra chapter, and concise has no license to turn the shared core into prose.
