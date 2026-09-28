# Historical v1 reference

This is retained legacy documentation. Native v2 follows ../records-and-delivery.md and the current SKILL.md.

# English mathematical exposition and typesetting

This file owns expression, statement granularity and meaningful repetition. Scope and principal-answer coverage belong to [introduction](introduction.md), research status to [core problems](core-problems.md), and typography to [layout and build](layout-and-build.md).

## Mathematical structure without compulsory narrative

Use a deletion test: remove a transition and ask whether any mathematical relationship becomes unclear. Delete sentences that merely announce the next definition, theorem or section. A substantive implication, obstruction or change of hypothesis is useful; generic scene-setting is not.

An introduction may consist of definitions followed by precise results. It does not need a narrative roadmap. Do not replace indispensable notation with a motivation paragraph or reproduce a displayed inequality in several sentences.

## Compact and self-contained statements

State the objects, quantifiers, ranges, hypotheses and essential conclusion. Put material assumptions, key inequalities or equivalence conditions, and the conclusion formulas directly in the statement. “Under (2.4), (2.7) implies (2.9)” makes the reader reconstruct the result and is not an adequate statement. Formula numbers may supplement the visible mathematics. Standard terminology and a nearby long definition can be referenced when restating them would obscure the result. Judge the actual backtracking needed; neither banning all references nor repeating all background is appropriate. Restore essential data in a distant restatement.

Use `itemize` for genuinely independent substantial assumptions and `enumerate` for logically numbered alternatives or conclusions. A pair of short conditions may fit better in a sentence or display. Lists are tools, not a required visual quota.

Do not bundle an existence criterion, a secondary corollary, a history paragraph and a caution into one theorem. Move secondary consequences outside the principal theorem. A directly useful consequence may deserve a separate corollary; an independently used intermediate conclusion may deserve a proposition or lemma. Only genuinely incidental observations belong in prose. Necessary regularity and branch restrictions are not optional qualifications.

## Body results and proof boundaries

Organize the body by mathematical tasks before drafting its prose. First formulate the necessary definitions, independently usable results, key proof inputs, and consumers. Draft their hypotheses and output formulas separately from the argument. Then attach a proof, proof sketch, or explicit source-and-use paragraph to each result. A whole-paper reader should be able to follow this dependency chain without reconstructing statements from explanations. A result must be recognizable without reconstructing its hypotheses and conclusion from a surrounding argument. Equation numbering and section headings cannot substitute for this structure.

Use the environment that matches the logical role:

- `theorem`: a principal result or a major sourced boundary theorem;
- `proposition`: an independently useful characterization, reduction or intermediate result;
- `lemma`: a technical input with a specific later use;
- `corollary`: a useful direct consequence, stated separately from its parent;
- `example`: a worked model or counterexample, not an unmarked interruption of a proof.

No quota applies to any type, and not every section needs a theorem. Definitions, historical context and genuinely elementary observations may be prose. A once-used lemma may stay **in the same TeX file**, but its essential mathematical statement must not disappear into prose merely because it is used once. Do not fabricate results to populate the outline.

Place indispensable local notation before a statement. Keep one mathematical task in each statement; put the derivation afterward in `proof`, `proof[Proof sketch]`, or `proof[Construction outline]` as appropriate. For an imported input, give a precise source and scope; an explanation of its use is not an independent proof. A short derivation should normally be supplied rather than sent to a citation.

Do not repair a paragraph-heavy draft merely by enclosing its whole argument in `proposition`. First extract the assumptions and usable conclusion, then separate the proof and source input. Remove rhetorical transitions, not the definitions, labels and dependencies that make the result navigable.

Two readings are mandatory. In the **statement-only reading**, skip proofs: identify what holds, under what assumptions and with what regularity/branch. In the **dependency reading**, identify which result each important step uses, what it produces and how it closes the argument. Located reviewer answers, not counts or generic PASS labels, belong in the existing reader/depth evidence; see [validation](validation.md). Inventory the claims in every body section before comparing them with the TeX environments. Record a missing independent result even when other theorems remain; record why genuinely contextual material needs no result. Do not let the environment inventory define which mathematics is worth recovering.

## Useful repetition and canonical reuse

Repetition is allowed when it saves real backtracking or permits independent reading. Avoid immediate duplicate statements. When the same substantive statement is exported or recalled, use a label-free canonical body with wrappers and labels at presentation sites. The `theoremrecall` environment preserves the original number without advancing the counter. A once-used lemma need not be split into another file.

Different formulations are not automatically the same theorem. A changed hypothesis or stronger conclusion requires a separate identity or explicit equivalence argument. Canonical consistency does not validate surrounding prose.

## Formulas, lists and sentence length

Prefer a formula for a mathematical condition and a short sentence for its role. Keep one main inference per sentence. Define new symbols at first use; place definitions of long-display notation near that display. Break long equations at mathematical boundaries, not by reducing type size.

A sentence containing several exceptions, parameter ranges and conclusions should usually become a statement followed by separate explanations. Remove process language such as “we checked all sources” from reader prose; evidence belongs in the delivery notes.

## Part V and editorial freedom

Use headings that name the mathematics rather than the production role. Part V should explain connections through actual transformations or estimates, not concatenate four inventories. A worked example must compute something, explain a hypothesis or show failure. The concise edition may cite a difficult construction precisely; it must still identify its usable output.

## Problems and their discussion

Use a numbered, labelled `problem` environment only for a selected authenticated mathematical target. State its objects, assumptions and requested conclusion inside the environment. Give source, exact status, verified progress and remaining range afterward. A vague research direction is not a Problem. No selected verified unresolved question means no active Problem block or dangling reference.

## Applications, sources and evidence

Credit the original result, not only the proof chosen for exposition. Use author attribution in an optional theorem heading when it helps, with a precise citation nearby. Do not fabricate authorial ownership of survey calculations.

## Layout and dependencies

Use the shared 12-point mathematical style. Repair excess length by selection and organization. Keep theorem hypotheses and their conclusions together where practical; avoid isolated headings or detached symbol definitions. See the separate layout guide for build and rendering commands.

## Introduction as mathematical knowledge

See [introduction](introduction.md) for the single authoritative coverage procedure. Style edits must not remove its mathematical commitments.

## Logical dependency and first use

A derivation must use defined notation and verified inputs within their stated range. Explain a changed convention before importing a formula. Do not silently identify congruence of phases with equality of real lifts.

## Statement titles and attribution

Do not give definitions or results decorative invented names. A useful author name identifies provenance, not a new taxonomy. Preserve familiar established terminology without introducing unnecessary named environments.

## V benchmark and actual pages

The examples in [the Part V guide](part-v-benchmark.md) are optional and purpose-specific, not whole-article standards. Judge the rendered article on its own agreed question.
