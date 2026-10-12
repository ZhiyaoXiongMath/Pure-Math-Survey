---
{
  "schema_version": "2.0.0",
  "id": "N-D-index",
  "kind": "definition",
  "title": "Index form along a unit speed geodesic",
  "facets": [
    "foundations",
    "methods"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Section 7.1, pp. 45–46 (fixed-end second variation); Theorem 9.3, pp. 55–56. Endpoint trial-field comparison is derived locally.",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    },
    {
      "relation": "proof_input",
      "target": "N-M-geometric-inputs"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    }
  ]
}
---

# Index form along a unit speed geodesic

## Canonical statement

```latex
For a unit speed geodesic \(\gamma:[0,L]\to(M,g)\), and piecewise smooth normal fields \(V,W\), its index form is
\[
I_\gamma(V,W)=\int_0^L\bigl(\langle D_tV,D_tW\rangle-\langle R(V,\dot\gamma)\dot\gamma,W\rangle\bigr)\,dt.
\]
Endpoint-vanishing means \(V(0)=V(L)=0\). If \(\gamma\) minimizes length between its endpoints, then \(I_\gamma(V,V)\ge0\) for every such \(V\).
```

## Endpoint conditions and the variation

The imported second-variation formula says that for a fixed-end variation of a unit-speed geodesic, the second derivative of the energy \(E=\tfrac12\int_0^L|\partial_tF|^2dt\) is \(I(V,V)\) at a geodesic. Given a smooth field \(V\) with \(V(0)=V(L)=0\), the variation \(F(s,t)=\exp_{\gamma(t)}(sV(t))\) realizes it for small \(s\), with both endpoints fixed. If \(\gamma\) is minimizing, Cauchy--Schwarz gives \(E(F(s,\cdot))\ge L(F(s,\cdot))^2/(2L)\ge L/2=E(\gamma)\), so \(I(V,V)\ge0\). Piecewise smooth fields follow by the same piecewise formula or approximation.

This is the only sign input used by the [Myers calculation](N-M-myers.md#the-sine-field-calculation). The connection is metric and curvature signs agree with [the curvature definition](N-D-curvature.md). Bishop's Section 7 uses an energy without the factor \(1/2\), which multiplies the second variation by \(2\); the sign and our displayed definition are unchanged.

### An endpoint field calculation

Here is a restricted index-lemma argument sufficient for a second route to Hessian comparison. Let \(\gamma:[0,L]\to M\) be the unique minimizing segment from \(p\) to an uncut point, and let \(X\perp\dot\gamma(L)\). The invertible radial tensor supplies a unique Jacobi field \(J\) with \(J(0)=0,\ J(L)=X\). For any smooth normal field \(V\) with the same endpoints, put \(W=V-J\). Integration by parts and the Jacobi equation give
\[
I(J,W)=[\langle J',W\rangle]_0^L-
\int_0^L\langle J''+R(J,\dot\gamma)\dot\gamma,W\rangle\,dt=0.
\]
Hence
\[
I(V,V)=I(J,J)+I(W,W)\ge I(J,J)
=[\langle J',J\rangle]_0^L
=\langle J'(L),X\rangle
=\nabla^2r_p(X,X).
\]
The last equality is the [current-vector Hessian identity](N-M-geometric-inputs.md#current-vectors-and-the-distance-hessian). Only the endpoint-zero field \(W\), not \(V\) or \(J\), is subjected to the nonnegativity assertion.

Now assume radial sectional curvature at least \(k\) and \(0<L<D_k\). Parallel transport \(X\) backwards to a field \(E\), and choose
\[
V(t)=f(t)E(t),\qquad f(t)=s_k(t)/s_k(L).
\]
This has exactly the required endpoint values. Since \(E'=0\) and \(|E|=|X|\),
\[
\begin{aligned}
\nabla^2r_p(X,X)&\le I(V,V)\\
&\le |X|^2\int_0^L(f'^2-kf^2)\,dt\\
&=|X|^2[ff']_0^L=c_k(L)|X|^2.
\end{aligned}
\]
The identity in the last line follows by differentiating \(ff'\) and using \(f''=-kf\). This is an actual trial-field computation, not an invocation of the entire index theorem. It yields the lower-sectional-curvature half of Hessian comparison at an uncut point. It does not claim a reversed bound merely by reversing the curvature inequality: \(I(J,J)\le I(V,V)\) has not reversed.

Return to [the comparison of the Riccati and index-form routes](../overview.md#sectional-bounds-to-jacobi-length-and-hessian). The Riccati route is useful for evolution and traces; the endpoint calculation is short when just one Hessian bound is needed.
