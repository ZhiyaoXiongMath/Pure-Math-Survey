# Bounded editorial reading cases

These sources and manuscripts are synthetic public engineering fixtures. They
are not private samples or assertions that an actual literature theorem has
been read. A real non-author reviewer must read both source notes and the
resulting manuscripts, identify the supported/unsupported claim and explain
why; the test runner only verifies byte edits and structural behavior.

Positive manuscript: `positive.tex`, controlling sources `source-a.md` (v1) and
`source-b.md` (v2), canonical input `N-SQUARE.tex`.

1. Borrowed theorem: the opening states the exact canonical real-variable
   claim and places Note A v1/Theorem 1.1 immediately before it.
2. Adapted proposition: the adjacent origin identifies the substitution y/2
   and positive factor 4. Its proof checks the domain and inequality direction.
3. Composite corollary: both sources and locators are named; the proof consumes the translated lemma and sets
   a=(x+1)^2, checks a>=0 and epsilon>0, and calls B's precise interface.
4. Local lemma: the translated formulation claims local derivation, with the
   external square input attributed at actual proof use. Its assumptions are
   checked. The directly calculated example has no fabricated citation.
5. Borrowed example/problem/conjecture: each names Note A's actual version and
   exact locator. The conjecture is not used as a proved premise.
6. Dependency order: the scaled proposition and translated lemma precede their
   later reference; the proposition is consumed by the translated lemma and that lemma by
   the corollary; the illustrative conjecture is not a proof premise. Numbers, ref links and the proof-target heading must
   also be inspected in the compiled PDF. Recall keeps its original number.

Negative manuscripts are mechanically derived in test_pr04_editorial.py. The
code's expected semantic issue labels are review prompts, not accepted records:

- bibliography_only: remove the opening's adjacent origin while retaining its
  bibliography. The borrowed main theorem has no nearby attribution.
- wrong_version: cite the hypothetical v0 integer restriction as if it supported
  every real x. A citation exists but does not support the domain/version.
- unsupported_hypothesis: change the composite corollary to epsilon>=0 and
  its proof's input claim accordingly. B's strict hypothesis fails at epsilon=0;
  the stated conclusion is actually false at x=-1, epsilon=0.
- missing_composite_input: remove Note B's adjacent attribution/citation and
  describe the proof input generically. A alone does not state the addition
  interface; the composition's second imported input is unacknowledged.
- imported_as_original: claim the borrowed opening theorem is proved from
  scratch here and is original, while retaining the unproved imported input.
- hidden_attribution: put the opening attribution only in a literal false branch;
  source tokens exist but are not displayed beside the theorem.
- optional_source_title: move the source into a theorem's optional title; this
  additionally violates the mechanical statement-title policy.
- unused_template_lemma: insert an unused tautological lemma and proof. The
  structural scanner cannot decide whether it supplies a useful consumed point.
- unresolved_complete: replace the decisive B application by a declaration that
  the proof is complete while explicitly leaving that step unresolved.

The first six and last two are deliberately semantic failures which generally
remain mechanically structural: do not add citation quotas or semantic regexes
to force rejection. Independent review must report its actual attempted reasoning,
version/hypothesis checks, findings and unchecked scope. Compilation proves only
that the fixture typesets; these instructions are not a completed review.
