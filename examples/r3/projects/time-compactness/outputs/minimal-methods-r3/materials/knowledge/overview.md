# Strong time compactness: one target, three interfaces

Fix $T>0$. A sequence may have strong spatial control while oscillating arbitrarily fast in time. The [question](nodes/N-question.md) is how uniform spatial information and uniform time translations jointly force convergence in a strong Bochner norm.

The reader can use Bochner integration, Hölder, Minkowski and completeness. The unfamiliar bridge is what to do when the spatial control is nonlinear: integration and subtraction may leave the controlled set.

## The common target of the spatial argument

[Simon's interval-integral criterion](nodes/N-simon-criterion.md) asks for two inputs in the same Banach space $E$:
\[
\left\{\int_a^b f(t)\,dt:f\in F\right\}\text{ relatively compact for }0<a<b<T,
\qquad \sup_{f\in F}\|\tau_hf-f\|_{L^p(E)}\longrightarrow0.
\]
The output is strong $L^p(E)$ compactness; at infinity the criterion also supplies continuous representatives. The two conditions are joint inputs, not separate sufficient conditions.

## A linear embedding: average first, then change norms

When $X\Subset B\hookrightarrow Y$, the bound on $\|f\|_{L^p(X)}$ makes interval integrals bounded in $X$, hence precompact in $Y$. Apply the criterion in $Y$, then use
\[
\|f_n-f_m\|_{L^p(B)}\le2\eta M+C_\eta\|f_n-f_m\|_{L^p(Y)}.
\]
Choosing $\eta$ before the subsequence index gives the strong limit in $B$. The exact theorem is [N-simon](nodes/N-simon.md); the finite-net and contradiction details are in [N-linear-mechanism](nodes/N-linear-mechanism.md).

## A nonlinear map: confine the values before averaging

For $v=K(u)$, a bound on $\|u\|_{L^1(E_1)}$ does not place $\int_Iv$ in the image of a bounded set. Cut off $u$ above height $M$ first. The image then lies in a compact set, whose closed convex hull contains its averages.

The lost part obeys
\[
\|v-v_M\|_{L^1(E_2)}\le(C_U/M)^{1-1/r}C_V+(C_U/M)\|K(0)\|_{E_2}.
\]
This supplies compact interval integrals; the separately assumed $L^p(E_2)$ translations supply time control. Read [N-truncation](nodes/N-truncation.md) for the construction and [N-maitre](nodes/N-maitre.md) for the complete result. The small tail is only an $L^1$ estimate, even if the target exponent is larger than $r$.

## A cone: retain the two points separately

A gauge controls $v(t)$ but may not be defined on $v_n(t)-v_m(t)$. [Two-point Ehrling](nodes/N-cone-ehrling.md) keeps the two gauges separate:
\[
\|u-v\|_{A_0}\le\eta([u]+[v])+C_\eta\|u-v\|_{A_1}.
\]
Gauge truncation and a derivative-induced $A_1$ amplitude give compact interval integrals in $A_1$. The time estimates depend on $q$: finite-$p$ translations work at $q=1$, while supremum translations require $q>1$. Then the two-point estimate gives convergence in $A_0$.

[N-cone-mechanism](nodes/N-cone-mechanism.md) performs every step and identifies the source proof passage it avoids. [N-cone](nodes/N-cone.md) contains the complete result, including the forbidden pair $(\infty,1)$.

## Comparison and condition changes

[N-homogeneous-transfer](nodes/N-homogeneous-transfer.md) proves one exact overlap: an injective compact map of degree $\alpha\ge1$ produces the gauge $[v]=\|K^{-1}v\|^\alpha$. The lift must be measurable, and the derivative and image spaces must both be $E_2$. This is a special reduction, not equivalence of all three theorems.

Two tests have different logical force. The [ramp](nodes/N-endpoint.md) has bounded $L^1$ derivative but no $L^\infty$ compactness: it is a counterexample to adding the excluded endpoint. The loss of the positive power $1-1/r$ in the map tail at $r=1$ only marks the limit of that argument.

The [squared dyadic signs](nodes/N-image-only.md) have identical compact images while their inputs remain a fixed distance apart. Thus the compact unknown in Maitre's theorem really is $K(u)$.

## Scope and evidence

Three original research texts control this bounded comparison: Simon's journal text, Maitre's published theorem, and Barrett--Süli's arXiv v2. New public source notes record current original-text readings and access limits. The historical two-source-to-three-source increment remains preserved in the original rc2 project; this independent r3 project adds readable mechanism routes and fresh output responsibilities without rewriting historical evidence.
