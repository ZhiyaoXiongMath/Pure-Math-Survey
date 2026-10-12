---
{
  "schema_version": "2.0.0",
  "id": "N-M-riccati",
  "kind": "mechanism",
  "title": "Jacobi tensors turn curvature into a matrix comparison",
  "facets": [
    "methods",
    "foundations"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Theorem 3.1, Remark 3.2, Theorem 3.3, pp. 12\u201314",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-distance"
    }
  ]
}
---

# Jacobi tensors turn curvature into a matrix comparison

## The two comparison tasks

The [Jacobi construction](N-D-jacobi.md#radial-variation-and-the-exponential-differential) supplies \(A''+\mathcal RA=0\), \(A(0)=0\), \(A'(0)=I\). Relative expansion \(S=A'A^{-1}\) acts on current normal vectors. We first derive its equation; only sectional comparison uses the later matrix-order input.

### Symmetry and the Riccati equation

The curvature operator \(\mathcal R\) is symmetric. Differentiate the Wronskian:
\[
\frac d{dt}\bigl(A^TA'-(A')^TA\bigr)
=A^TA''-(A'')^TA
=-A^T\mathcal RA+A^T\mathcal R^TA=0.
\]
It vanishes at zero. Multiply the resulting equality by \(A^{-T}\) on the left and \(A^{-1}\) on the right to obtain \(S=S^T\), wherever \(A\) is invertible.
\[
S'=A''A^{-1}-A'A^{-1}A'A^{-1}=-\mathcal R-S^2,
\qquad S=t^{-1}I+O(t).
\]
The pole estimate follows from the [actual Taylor expansion](N-D-jacobi.md#the-pole-and-the-positive-interval). For a Ricci lower bound, proceed directly to [the trace argument](N-M-trace.md#why-the-trace-is-the-controlled-quantity). It requires no matrix-order comparison theorem.

### Matrix comparison and its imported singular boundary

For regular symmetric solutions with \(\mathcal R_1\ge\mathcal R_2\), put \(U=S_2-S_1\) and \(X=-(S_1+S_2)/2\). Their equations give
\[
U'=XU+UX+(\mathcal R_1-\mathcal R_2).
\]
Choose \(G'=XG\), \(G(t_0)=I\). This fundamental matrix is invertible, although it need not be symmetric. Substituting \(U=GZG^T\) gives
\[
Z'=G^{-1}(\mathcal R_1-\mathcal R_2)G^{-T}\ge0.
\]
Thus \(U(t_0)\ge0\) implies \(U(t)\ge0\) on the common regular forward interval.

The radial pole is a separate imported interface from Eschenburg's Remark 3.2: for smooth symmetric curvature operators ordered as above and their radial solutions \(S_i=t^{-1}I+O(t)\), one has \(S_1\le S_2\) on the common positive existence interval. Their difference extends to zero with value zero. The proof of this singular extension is not claimed here.

Applying it to \(S_k=c_kI\) gives \(S\le c_kI\) for radial sectional curvature at least \(k\), and \(S\ge c_kI\) for curvature at most \(k\), while both solutions exist. The [Hessian identification](N-M-geometric-inputs.md#current-vectors-and-the-distance-hessian) then converts the operator estimate into the Hessian inequality before cut.

### Jacobi length and exponential-map use

Take \(w\ne0\), \(J=A w\). Before the first actual conjugate point and before \(D_k\), \(J\ne0\) and \(s_k>0\). Under the sectional lower bound,
\[
\frac d{dt}\log\frac{|J(t)|}{|w|s_k(t)}
=\frac{\langle SJ,J\rangle}{|J|^2}-c_k\le0,
\qquad \frac{|J(t)|}{|w|s_k(t)}\longrightarrow1.
\]
Integrating from \(\varepsilon\) and letting \(\varepsilon\downarrow0\) yields \(|J|\le |w|s_k\). The sectional upper bound reverses the derivative inequality and yields \(|J|\ge |w|s_k\).

In the upper-bound case, suppose the first actual conjugate time \(t_0<D_k\) existed. A nonzero \(w\in\ker A(t_0)\) would satisfy, by the preceding estimate and continuity,
\[
0=|A(t_0)w|\ge s_k(t_0)|w|>0.
\]
So that comparison continues to \(D_k\). For a sectional lower bound this contradiction is unavailable; its actual-conjugate restriction is essential, as the [spherical cutoff example](N-E-rauch-cutoff.md) shows.

Here is one use of the estimate. Let \(v(s)\) be a piecewise smooth unit-direction curve. Assume the radial sectional lower bound holds along each of its rays up to a fixed \(0<t<D_k\), and all those rays remain before their first conjugate time there. The [differential dictionary](N-D-jacobi.md#radial-variation-and-the-exponential-differential) gives
\[
\left|\frac d{ds}\exp_p(tv(s))\right|
=|A_{v(s)}(t)v'(s)|\le s_k(t)|v'(s)|.
\]
After integration, the image curve has length at most \(s_k(t)L_{S_pM}(v)\). This is a curve-length estimate with an explicit admissible family, not an assertion of global triangle comparison.

For variable radii, Gauss lemma separates radial and angular speed. [Toponogov's local construction](N-M-toponogov.md) uses that fact on a common normal domain and must check that its comparison curve stays inside it.

Return to [sectional comparison](../overview.md#sectional-bounds-to-jacobi-length-and-hessian). The scalar route uses only the first calculation; matrix order is an additional investment for directional bounds.
