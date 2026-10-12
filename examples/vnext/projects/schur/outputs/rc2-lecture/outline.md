# Lecture design: derive the criterion by executing square completion

## Reader and intended use
The reader multiplies compatible real matrices, transposes products, and expands scalar squares. They can use the definition of positive definiteness once recalled. They need not recognize Schur complements or know congruence invariance. The only imported theorem is the elementary finite-dimensional square-map zero-kernel criterion for invertibility. The manuscript explains its precise use in obtaining A^{-1} from A>0.

Assumed: multiplication, transpose rules, real-scalar transpose, scalar square expansion.
Refreshable: positivity as a universal quadratic-form test and the zero-kernel criterion.
Bridge-required: choosing the block shift, calculating the remainder, and preserving nonzero pairs through an explicit inverse.

## Methods view and teaching order
1. Section 1 states the full principal [[N-main]] and the exact block quadratic form. Its short strategy identifies both inputs and the asymmetric roles of the arbitrary pair and the cancellation vector.
2. Section 2 matches the scalar mixed term, then matches AK=B in the block model. It checks sizes and obtains invertibility from the positive-block hypothesis.
3. Section 3 develops [[N-square]] by expanding all four terms, then proves symmetry and identifies the remainder S. Symmetry/invertibility are separated from the later sign argument.
4. Section 4 proves both inverse compositions for [[N-inverse]], then proves sufficiency by the z=0 versus z nonzero split and necessity using x=-A^{-1}By for every nonzero y. These close all three N-main proof obligations.
5. Section 5 executes the recorded scalar model and the negative-block counterexample from [[N-boundary]]. The singular case is explicitly noncoverage. The model's fixed-y minimum is computed from its displayed square.

This order lets the reader first know the target, then construct the input that removes the obstruction, and finally verify the universal positivity tests. The methods focus is carried by actual operations, not by node facets alone.

## Proof and input boundaries
The main proof consumes [[N-square]] and [[N-inverse]] in full. Although these are imported canonical interfaces from the fixed knowledge snapshot, their arguments are developed in this lecture. No deep theorem, limiting procedure, uniform-constant estimate, or congruence criterion is imported.

The exact promised steps are: expand the square with A symmetric and invertible; use the invertible change of variables for sufficiency; choose x=-A^{-1}By for every nonzero y to prove necessity. The first two bridge proofs occur within this complete proof route, with the canonical statements retained literally.

The congruence comparison (N-comparison) is omitted: a separate congruence formulation is not necessary for the selected construction. The teaching task has suitable method and boundary nodes, so no missing method node is filled by an unsupported comparison. No semidefinite or singular-block extension, literature completeness, or original contribution is promised.

## Review scope
This new article binds the unchanged KB-714ebb540c07ca2585ac455f40d642f6920d708a8a3ce1f91f4e4000d41f12cd snapshot. Historical readiness evidence remains historical. A current author rereading checks the new methods view and every actual proof location; it is neither independent mathematical review nor a reader experiment. There is no requested page cap.
