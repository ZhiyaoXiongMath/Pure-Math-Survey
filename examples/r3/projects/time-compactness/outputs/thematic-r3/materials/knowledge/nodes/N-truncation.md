---
{
  "schema_version": "2.0.0",
  "id": "N-truncation",
  "kind": "mechanism",
  "title": "Truncation gives compact interval integrals",
  "facets": [
    "methods"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-maitre",
      "locator": "Lemma 2.3 and equations (2.3)--(2.24), pp. 1726--1730",
      "role": "support",
      "version": "Published IJMMS 2003:27, pp. 1725--1730, DOI 10.1155/S0161171203106175"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-simon-criterion"
    }
  ]
}
---

# Truncation gives compact interval integrals

## Fast route and inputs

Use the hypotheses of [Maitre's theorem](N-maitre.md). The map $K$ need not commute with integration. Instead, truncate its input to a bounded set, average the resulting compact value set, and control the discarded output in $L^1$.
\[
C_U=\sup_{u\in U}\|u\|_{L^1(E_1)},\qquad
C_V=\sup_{v\in V}\|v\|_{L^r(E_2)},\qquad r>1.
\]
Translations are consumed only at the final invocation of [Simon's criterion](N-simon-criterion.md).

## Slow route: a uniform tail

For $M>0$, put $G_M(u)=\{t:\|u(t)\|_{E_1}>M\}$, and set $u_M=u$ off $G_M$ and zero on $G_M$. Then $v_M=K(u_M)$ is measurable because it equals $v$ or the fixed value $K(0)$, and
\[
|G_M(u)|\le C_U/M,\qquad v-v_M=\mathbf1_{G_M}(v-K(0)).
\]
Hölder, with $1/r=0$ when $r=\infty$, yields
\[
\|v-v_M\|_{L^1(E_2)}\le (C_U/M)^{1-1/r}C_V+(C_U/M)\|K(0)\|_{E_2}.
\]
The right side tends to zero uniformly in the family. No $L^p$ tail estimate is claimed when $p>r$: $L^1$ already controls every interval integral.

## Slow route: why averaging preserves precompactness

For fixed $M$, the closure $Q_M=\overline{K(\{x:\|x\|\le M\})}$ is compact. A compact set $Q$ in a Banach space has compact closed convex hull. Indeed, choose a finite $\delta$-net $q_1,\ldots,q_J$ in $Q$. Replacing each point in a convex combination by a nearby net point proves
\[
\operatorname{co}(Q)\subset\operatorname{co}\{q_1,\ldots,q_J\}+\delta B_E.
\]
The finite-dimensional simplex is compact. Hence the hull is totally bounded; its closure is compact by completeness.

For a measurable $w:I\to Q$, choose the first nearest net point to break ties. The resulting cells are measurable, and integrating their indicators gives nonnegative weights summing to one. The simple-function averages approximate $|I|^{-1}\int_Iw$ within $\delta$. Therefore
\[
|I|^{-1}\int_Iw(t)\,dt\in\overline{\operatorname{co}}(Q).
\]
Apply this to $v_M$. The truncated interval integrals form a relatively compact set. Given $\varepsilon$, choose $M$ to make the uniform tail small, then take a finite net for that fixed truncated set. The original interval integrals are totally bounded as well.

## Consumption and boundary

Simon's criterion now combines these interval integrals with the assumed $L^p(E_2)$ translations to prove [N-maitre](N-maitre.md). Maitre's original proof uses shifted finite Riemann sums; this compact-hull proof is a local reconstruction, not a quotation or an original research claim.

The exponent $r>1$ makes $1-1/r$ positive in this particular tail estimate. At $r=1$ the estimate alone stops proving uniform smallness. This is noncoverage by the argument, not a counterexample to every nonlinear compactness theorem.
