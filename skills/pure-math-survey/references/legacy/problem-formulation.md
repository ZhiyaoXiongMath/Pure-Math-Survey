# Historical v1 reference

This is retained legacy documentation. Native v2 follows ../records-and-delivery.md and the current SKILL.md.

# Problem formulation: understand before fixing

This file owns the first mathematical step. It is not a final quantifier spell-check. A survey reconstructs the question from the definitions and geometry; it does not concatenate the hypotheses of papers. Source checking remains necessary, but a faithful transcription can still answer the wrong or unnecessarily restricted question.

## 1. Reconstruct the objects

Before fixing a parameter, identify what it is: intrinsic data; an equivalence class; a representative; an unknown; a normalization or gauge choice; an auxiliary parameter in a proof. Recover how the equation, functional, admissibility condition and solution notion depend on it. Work through a defining calculation or elementary model when that dependence is not clear.

For each material apparent choice ask what happens when it changes. Distinguish changes that preserve the same object in different coordinates from changes to the actual equation. Identify the invariants worth preserving and the admissible domain of the change. A natural question often fixes a class, topology, boundary data or normalization while allowing representatives to move. This is not a command to free every variable: a parameter may be correctly held fixed, but the decision needs a mathematical reason, not merely “the cited papers fix it.”

Record considered variations and their decisions: in scope, gauge only, held fixed, auxiliary, or out of scope. Explain why the selected range is meaningful and why excluded changes form a different problem or exceed the task. Do not manufacture a large catalog of irrelevant variations to satisfy a quota. These decisions belong in the existing architecture note and the `problem_formulation` field of existing reader evidence, not a new stack of registries.

## 2. Formulate before answering

Specify the chosen data and domains before the first principal answer. For a parameter p and unknown u, distinguish the original fixed-p question, existence of a pair, and solvability for every admissible p. Write ordered quantifiers when they carry the point. Say what u and any constants may depend on. “For every p there exists u_p” does not mean “there exists one u for all p,” nor does it supply estimates uniform in p.

The range of a quantifier is mathematical content. An equivalence class is not all representatives of all classes; a smooth positive family is not its degenerate boundary; a pointwise-in-parameter theorem is not a uniform theorem. A branch, regularity class and normalization may also change the question.

Do not assume that two formulations are equivalent because an invariant agrees. Distinguish an equivalence by definition/gauge, a proved equivalence, a checked implication, a disproved implication and a genuinely unresolved relationship. Source and/or prove the precise relationship. A scope-defining equivalence belongs to the principal answer to the questions posed at the outset; hiding it in a late corollary is not an acceptable repair. Ordinary secondary consequences can still be corollaries.

A local analytic argument may freeze an arbitrary member of the globally chosen domain. State this scope transition. A proof path, moving background and time evolution are different parameter changes; do not transfer estimates or evolution identities between them without justification. Identify the hypotheses controlling uniformity, and do not claim it when only separate existence has been proved.

## 3. Research actively, then revise the model

Inspect original definitions, source formulations, natural variants, examples, counterexamples and organizing problems. Search both the conventional formulation and the meaningful variants found above. Ask whether historical hypotheses are geometric requirements, proof devices, normalizations or restrictions later removed. Do not broaden a theorem merely because its statement looks unnecessarily narrow. Derive what can be derived, locate what needs a theorem and mark what is unverified.

For every user-emphasized question and every input conclusion essential to the selected problem, record its destination. Test input-to-opening-to-answer coverage as well as introduction-to-body coverage. Both introduction and body can omit the same central question and still agree. Logical consequence alone does not count as reader-facing preservation of a core question or answer.

## 4. Two editions, one problem

Concise and standard keep the same selected variable domains, quantifier order, core questions, core answers and key lemma structure. Concise compresses proof interiors, routine calculations and redundant transitions. Standard explains the same choices, estimates and constructions in more detail for readers studying the techniques. Neither edition silently locks a variable, removes a branch condition or leaves an essential equivalence for readers to reconstruct.

## 5. Checks and their limits

`check_problem_formulation.py --stage plan` requires a considered model before prose: objects, meaningful variation decisions, ordered quantified question variants, relationship status and source/user commitments. It checks reference/dependency consistency; it does not decide that the chosen model is optimal. New scaffolds remain pending and must fail production acceptance.

At release, the same record adds bounded, exact source bindings. Opening bindings must precede the designated principal answer; answer bindings must occur inside that result; local-scope bindings locate actual qualifications. Quantifier tokens must match their ordered record and all required user/input commitments need destinations. A changed source digest or a changed model invalidates the corresponding review. Plan-time selection and release-time writing must be read by a mathematical reviewer; a hash is not a proof of thought, chronology, correctness or semantic completeness.

Perform three readings: problem-only (definitions, ranges, questions); statement-only (answers and key lemmas); dependency reading (inputs, outputs, closure and constant dependence). Do not accept generic PASS prose. Record what can actually be recovered and where. Challenge the formulation against a late-only scope repair, a silent parameter freeze, reversed quantifiers, unrestricted broadening, missing user commitments and an unjustified claim of uniformity.

## A generic comparison, not a prescribed answer

A reference representative may be a coordinate choice for the unknown, while a background with the same invariant class may change the differential operator. A family parameter can change the instance being solved. Derive these distinctions from definitions, not notation. Some-instance existence, every-instance existence, a common unknown and estimates uniform over parameters are different assertions. State only sourced or proved relations. Other subjects may have no representative variable at all.

Bind scope-defining qualifiers as well as displayed formulas. A formula-only excerpt can miss contradictory adjacent prose even when the global source digest is refreshed. Exact bindings still do not certify all unrecorded semantic consistency.
