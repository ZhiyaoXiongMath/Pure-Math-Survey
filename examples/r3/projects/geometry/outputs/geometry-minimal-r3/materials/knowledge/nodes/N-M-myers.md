---
{
  "schema_version": "2.0.0",
  "id": "N-M-myers",
  "kind": "mechanism",
  "title": "Second variation yields the diameter bound",
  "facets": [
    "methods"
  ],
  "question_ids": [
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Theorem 9.3, pp. 55–56",
      "role": "support"
    },
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Corollary 12.3, p. 59",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-index"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "proof_input",
      "target": "N-M-geometric-inputs"
    }
  ]
}
---

# Second variation yields the diameter bound

## Purpose and admissible fields

Assume \(\operatorname{Ric}\ge(n-1)kg\) with one constant \(k>0\) on the connected complete manifold. If a minimizing unit-speed segment had length \(L>\pi/\sqrt{k}\), [fixed-end second variation](N-D-index.md#endpoint-conditions-and-the-variation) would be nonnegative on every normal field vanishing at \(0,L\). We construct fields whose sum of index forms is negative.

### The sine-field calculation

Choose a parallel orthonormal normal frame \(E_1,\ldots,E_{n-1}\) and set
\[
V_i(t)=\sin(\pi t/L)E_i(t),\qquad
D_tV_i=(\pi/L)\cos(\pi t/L)E_i(t).
\]
The sine satisfies both endpoint conditions; its frequency \(\pi/L\) lets the derivative-energy cost be compared directly with \(k\). The curvature sum is
\[
\sum_i\langle R(V_i,\dot\gamma)\dot\gamma,V_i\rangle
=\sin^2(\pi t/L)\operatorname{Ric}(\dot\gamma,\dot\gamma).
\]
Thus summation uses exactly Ricci, not an individual sectional lower bound:
\[
\begin{aligned}
\sum_i I(V_i,V_i)
&\le(n-1)\int_0^L
\left[(\pi/L)^2\cos^2(\pi t/L)-k\sin^2(\pi t/L)\right]dt\\
&=\frac{(n-1)L}{2}\bigl((\pi/L)^2-k\bigr)<0,
\end{aligned}
\]
because each squared trigonometric term has integral \(L/2\). At least one term is negative, contradicting nonnegativity of every \(I(V_i,V_i)\). Therefore a minimizing segment cannot have length \(L>\pi/\sqrt{k}\). This strict-inequality argument needs no claim of positive definiteness at a conjugate endpoint.

### From length to compactness and finite fundamental group

[Hopf--Rinow](N-M-geometric-inputs.md#completeness-and-minimizing-segments) supplies a minimizing segment between every pair of points. The preceding exclusion proves \(\operatorname{diam}M\le\pi/\sqrt{k}\). Fixing one point, \(M\) is itself a closed bounded subset, and completeness makes it compact.

The universal covering \(\widetilde M\to M\), equipped with the lifted metric, is complete: geodesics project, extend downstairs and lift for all time. A local isometry preserves the curvature tensor and the same Ricci bound. The already proved diameter and compactness argument therefore applies to \(\widetilde M\).

A fiber in this covering is closed and discrete. It is a compact subspace of \(\widetilde M\), so it is finite (a compact discrete space is finite). For a universal covering of a connected manifold, the fiber is in bijection with the fundamental group after choosing a base point. Hence \(\pi_1(M)\) is finite.

### One use and one boundary

This result closes the [positive-curvature endpoint in volume comparison](N-M-cut-integration.md#the-positive-curvature-endpoint); the proof above does not use Bishop--Gromov, so that use is not circular. If completeness is removed, the global minimizing and compactness deductions are no longer available. If a uniform positive \(k\) is replaced by \(k=0\), the computed last expression is positive and there is no length contradiction. [The boundary examples](N-E-completeness.md) distinguish these failures from a mere missing proof.

Return to [the fast Myers route](../overview.md#myers-from-endpoint-fields-to-global-finiteness).
