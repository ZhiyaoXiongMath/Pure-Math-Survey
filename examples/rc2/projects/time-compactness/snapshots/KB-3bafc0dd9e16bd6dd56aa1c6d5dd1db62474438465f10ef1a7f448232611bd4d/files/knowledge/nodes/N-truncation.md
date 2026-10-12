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

Input: the hypotheses of N-maitre, but translation control is used only at the last invocation of N-simon-criterion. Let C_U=sup ||u||L1(E1), C_V=sup ||K(u)||Lr(E2), and G_M(u)={t:||u(t)||E1>M}. Markov gives |G_M(u)|<=C_U/M. Define u_M=u off G_M and zero on G_M, and v_M=K(u_M). Then v-v_M=1_{G_M}(v-K(0)), so Holder yields

||v-v_M||L1(E2) <= (C_U/M)^{1-1/r} C_V + (C_U/M)||K(0)||E2.

This tends to zero uniformly for r>1 (with 1/r=0 for r=infinity). The estimate does not claim smallness in Lp if p>r. Smallness in L1 is enough to approximate all interval integrals.

For fixed M, let Q_M be the closure of K({x:||x||E1<=M}); it is compact. On I=(a,b), every average |I|^{-1} int_I v_M lies in the closed convex hull of Q_M. Here is the finite-net proof that this hull is compact in a Banach space: choose a finite delta-net q_1,...,q_J of Q_M. A convex combination of Q_M points lies within delta of the finite-dimensional compact simplex conv{q_j}. Thus the hull is totally bounded; its closure is compact by completeness. For the integral statement, choose measurable nearest-net cells for v_M and integrate their indicators, obtaining nonnegative weights summing to one. The approximation error is at most delta, then take delta to zero.

Consequently {int_I v_M} is relatively compact. The displayed tail estimate uniformly approximates {int_I v}; for any epsilon choose M first, then a finite net for the truncated set. Hence {int_I v} is totally bounded and relatively compact in E2. Simon's criterion now gives the exact Lp target from the assumed Lp translations.

Source relation: Maitre Lemma 2.3 and (2.3)--(2.24), pp.1726--1730, use shifted finite Riemann sums. The compact-convex-hull argument here is a checked elementary reconstruction of the same spatial truncation mechanism, not a quotation or originality claim. It preserves K(0), uniformity and the r>1 limitation of this estimate.
