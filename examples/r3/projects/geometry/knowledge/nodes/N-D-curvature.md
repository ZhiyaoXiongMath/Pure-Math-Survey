---
{
  "schema_version": "2.0.0",
  "id": "N-D-curvature",
  "kind": "definition",
  "title": "Curvature and normalization",
  "facets": [
    "foundations"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume",
    "N-Q-global",
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Section 1, pp. 3\u20134",
      "role": "support"
    }
  ],
  "links": []
}
---

# Curvature and normalization

## Canonical statement

```latex
Let \((M^n,g)\) be a smooth Riemannian manifold, \(n\ge2\), with Levi--Civita connection \(\nabla\). Set
\[
R(X,Y)Z=\nabla_X\nabla_YZ-\nabla_Y\nabla_XZ-\nabla_{[X,Y]}Z,
\qquad
K(X\wedge Y)=\frac{\langle R(X,Y)Y,X\rangle}{|X|^2|Y|^2-\langle X,Y\rangle^2}.
\]
For an orthonormal frame \((e_i)\), define
\[
\operatorname{Ric}(v,v)=\sum_{i=1}^n\langle R(e_i,v)v,e_i\rangle,
\qquad \Delta f=\operatorname{div}\nabla f=\operatorname{tr}_g\nabla^2f.
\]
The notation \(\operatorname{Ric}\ge(n-1)k g\) means
\(\operatorname{Ric}_x(v,v)\ge(n-1)k|v|_g^2\) for every \(x\in M\) and \(v\in T_xM\).
The notation \(\sec\ge k\) means \(K(\sigma)\ge k\) for every tangent two-plane \(\sigma\).
```

## Explanation and evidence

The project uses unnormalized Ricci. Eschenburg uses the same R(X,Y)Z convention in §1. Bishop's tensor notation has a different slot/sign presentation; only geometric sectional curvature and the Jacobi equation are translated. Normalized mean curvature will be named a=m/(n-1), never confused with the unnormalized trace m.

### The radial curvature operator

Curvature measures the failure of two covariant derivatives to commute after subtracting the Lie-bracket correction. The [connection rules](N-D-riemannian.md#differentiating-moving-vectors) make the displayed definition an operation on vector fields. The curvature identities imply that, for a unit vector \(T\), the map
\[
\mathcal R_T:T^\perp\to T^\perp,\qquad X\longmapsto R(X,T)T
\]
is self-adjoint. These algebraic identities are an imported property of the Levi--Civita curvature tensor; Eschenburg states them in Section 1. For \(X\perp T\), the definition of sectional curvature gives
\[
\langle\mathcal R_TX,X\rangle=K(T\wedge X)|X|^2.
\]
Thus a lower bound on every plane containing \(T\) is exactly the quadratic-form inequality \(\mathcal R_T\ge kI\). Completing \(T\) to an orthonormal basis gives
\[
\operatorname{tr}\mathcal R_T
=\sum_{i=1}^{n-1}K(T\wedge e_i)
=\operatorname{Ric}(T,T).
\]
This explains both the factor \(n-1\) and why a trace bound supplies less information than a bound in every direction. The [product example](N-E-product.md) makes the nonconverse concrete. In constant curvature \(k\), \(\mathcal R_T=kI\); the [Jacobi model calculation](N-D-jacobi.md#one-complete-model-calculation) then reduces to the scalar equation \(s_k''+ks_k=0\).

Return to the [reader entrance](../overview.md#reader-entrance-and-available-operations), before differentiating the radial variation.
