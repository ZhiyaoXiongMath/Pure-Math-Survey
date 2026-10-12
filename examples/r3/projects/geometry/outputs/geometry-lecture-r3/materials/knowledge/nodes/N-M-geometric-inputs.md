---
{
  "schema_version": "2.0.0",
  "id": "N-M-geometric-inputs",
  "kind": "mechanism",
  "title": "Geometric interfaces used by the classical comparison chain",
  "facets": [
    "foundations",
    "methods"
  ],
  "question_ids": [
    "N-Q-classical-core"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Lemma 5.5 and Proposition 5.10, p. 33; Theorem 5.11 and Corollary 5.12, p. 34; Section 7.1, pp. 45–46; Proposition 8.2 and Theorems 8.3–8.4, pp. 52–53; Theorem 9.2, p. 55",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-riemannian"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    }
  ]
}
---

# Geometric interfaces used by the classical comparison chain

## Scope of the imported geometry

The metric and connection are introduced in [the operational entrance](N-D-riemannian.md#operational-entry). This node separates exact foundational inputs from the calculations performed with them. The [Jacobi variation](N-D-jacobi.md#radial-variation-and-the-exponential-differential) fixes all initial/current-vector conventions.

### Completeness and minimizing segments

We import Hopf--Rinow for a connected Riemannian manifold: metric completeness is equivalent to geodesic completeness; it suffices that geodesics from one point extend for all times. A complete manifold has minimizing segments between any two points and compact closed bounded subsets.

A Riemannian covering of a complete manifold is complete: project a geodesic, extend it downstairs, and lift that extension with its initial point. Hopf--Rinow then applies upstairs. These are the global inputs consumed by [Myers](N-M-myers.md) and [Hadamard](N-M-hadamard.md).

### Current vectors and the distance Hessian

Gauss lemma is imported in the following form: the radial differential of \(\exp_p\) has unit length and is orthogonal to angular variations. On the regular minimizing domain, this identifies \(T=\partial_t\Phi=\operatorname{grad}r_p\).

Fix an uncut ray. An initial vector \(w\) becomes the current normal separation \(X=A(t)w\). To differentiate a given current separation, first recover its initial vector:
\[
w=A(t)^{-1}X,\qquad J_w'(t)=A'(t)w=A'(t)A(t)^{-1}X=SX.
\]
This is why \(A'\) alone is not the relative expansion operator: its input is the initial vector. The input of \(S\) is a vector at the current point, after parallel identification.

For the radial variation, the coordinate fields commute. Torsion-freeness consequently gives
\[
\nabla_{J_w}\operatorname{grad}r_p
=\nabla_{J_w}T=\nabla_TJ_w=J_w'=SJ_w.
\]
Invertibility of \(A\) means these fields span the normal space. Thus, if \(X,Y\perp T\),
\[
\nabla^2r_p(X,Y)=\langle SX,Y\rangle,\qquad
\nabla^2r_p(T,\cdot)=0,\qquad \Delta r_p=\operatorname{tr}S.
\]
The first expression is a bilinear form; \(S\) is its endomorphism after metric identification. The radial component vanishes because \(\nabla_TT=0\). The symmetry and evolution of \(S\) are calculated in [Riccati](N-M-riccati.md#symmetry-and-the-riccati-equation).

For an arbitrary \(X\), write \(X^\perp=X-dr_p(X)T\). A bound \(S\le c_kI\) gives
\[
\nabla^2r_p(X,X)\le c_k\bigl(|X|^2-dr_p(X)^2\bigr).
\]
This is the actual application yielding the full Hessian form, on the uncut and model-positive domain. It does not assert a classical Hessian at a cut point.

### Complete local isometries and covering

We use the following interface: a local isometry \(F:N\to M\) from a connected complete Riemannian manifold to a connected Riemannian manifold is a surjective covering. In the applications here \(M\) is complete as well.

For the complete-target case, a minimizing segment from a point in the image to any \(y\in M\) lifts as a geodesic in \(N\), giving surjectivity. Fix a sufficiently small normal ball about \(y\). From each \(x\in F^{-1}(y)\), lift its radial segments using \(dF_x^{-1}\) and completeness.

The resulting local sections have disjoint images: reversing a radial segment and uniqueness of its lift would otherwise give two endpoints in the same fiber. Conversely, reverse the radial segment from any preimage of the ball to obtain its fiber point. These sections exhaust the preimage, proving it is evenly covered.

This restates the path-lifting mechanism in Bishop's Theorem 9.2; it is not advertised as a separately numbered theorem there. If \(M\) is simply connected, a connected covering has one sheet, and the local diffeomorphism \(F\) is a global diffeomorphism.

### Other inputs and their actual uses

The [index-form interface](N-D-index.md) supplies nonnegativity for endpoint-zero fields along a minimizing segment. [Myers](N-M-myers.md) performs the sine-field substitution and integral; these operations are not imported with that theorem.

The [uncut-domain theorem](N-M-cut-integration.md#the-uncut-domain-and-the-ball-integral) supplies parametrization and zero measure. The radial-to-ball change of variables and weighted-average argument are performed there. Singular matrix comparison and triangle gluing have their own precise boundaries in the corresponding mechanisms.

Return to the [reader entrance](../overview.md#reader-entrance-and-available-operations). These interfaces are used where needed; the scalar Ricci route does not require learning all matrix or triangle comparison first.
