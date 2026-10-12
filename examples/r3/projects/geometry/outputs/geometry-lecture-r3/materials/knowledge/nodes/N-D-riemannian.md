---
{
  "schema_version": "2.0.0",
  "id": "N-D-riemannian",
  "kind": "definition",
  "title": "Metric, connection, geodesics and Hessian",
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
      "locator": "Section 1, p. 3; Sections 1.2\u20131.3, p. 7; Sections 3.1, 3.5, 3.24, 3.28\u20133.29, pp. 10\u201312, 18\u201319, 22; Section 4.4, Theorem 4.1, p. 24; Section 6.2, p. 36; Section 9.2, p. 57",
      "role": "support"
    }
  ],
  "links": []
}
---

# Metric, connection, geodesics and Hessian

## Canonical statement

```latex
A Riemannian metric on a smooth manifold \(M\) is a smooth positive-definite inner product \(g_p\) on each tangent space. Write \(\langle X,Y\rangle=g(X,Y)\) and \(|X|^2=g(X,X)\). For a piecewise smooth curve \(\gamma:[a,b]\to M\), define
\[
L_g(\gamma)=\int_a^b|\dot\gamma(t)|\,dt,\qquad
d_g(p,q)=\inf_{\gamma(a)=p,\,\gamma(b)=q}L_g(\gamma).
\]
The Levi--Civita connection \(\nabla\) is the unique torsion-free, metric-compatible connection. A geodesic satisfies \(D_t\dot\gamma=0\), where \(D_t=\nabla_{\dot\gamma}\); if \(\gamma_v(0)=p\) and \(\dot\gamma_v(0)=v\), set \(\exp_p(v)=\gamma_v(1)\) whenever defined. For a smooth function \(f\), its gradient and Hessian are characterized by
\[
\langle\operatorname{grad}f,X\rangle=df(X),\qquad
\nabla^2f(X,Y)=\langle\nabla_X\operatorname{grad}f,Y\rangle
=XYf-(\nabla_XY)f.
\]
```

## Operational entry

The comparison problem begins with a smooth positive-definite matrix \(g_{ij}\) in each coordinate chart. It turns a tangent vector into a length, and a small coordinate box into volume:
\[
|X|_g^2=g_{ij}X^iX^j,\qquad
d\operatorname{Vol}_g=\sqrt{\det(g_{ij})}\,|dx^1\cdots dx^n|.
\]
Curve length is the integral of speed; distance is the infimum of lengths. A minimizing segment realizes this infimum. Its arclength parameter has speed one.

### Differentiating moving vectors

The existence and uniqueness of the Levi--Civita connection are imported. The two identities used below are its defining working rules:
\[
X\langle Y,Z\rangle=\langle\nabla_XY,Z\rangle+\langle Y,\nabla_XZ\rangle,
\qquad \nabla_XY-\nabla_YX=[X,Y].
\]
Parallel transport along \(\gamma\) solves \(D_tE=0\). It preserves inner products. In a parallel orthonormal frame, a field \(J=\sum_i a_iE_i\) has \(D_tJ=\sum_i a_i'E_i\); the later matrix ODEs use exactly this identification.

A geodesic solves \(D_t\dot\gamma=0\). Smooth ODE existence and uniqueness give its dependence on the initial point and velocity. Thus \(\exp_p(tv)\) is the point reached at time \(t\) with initial velocity \(v\), whenever the solution exists.

### Gradient and Hessian as operations

The gradient is the vector representing \(df\) by the metric. Differentiating that vector gives an endomorphism \(H_f:X\mapsto\nabla_X\operatorname{grad}f\); taking its inner product with \(Y\) gives the Hessian bilinear form.
\[
\nabla^2 f(X,Y)=\langle H_fX,Y\rangle,\qquad
\Delta f=\operatorname{tr}H_f=\operatorname{div}\operatorname{grad}f.
\]
We use this sign for the Laplacian throughout the distance comparison chain. Torsion-freeness makes the Hessian symmetric. No smoothness of the distance function at a cut point is asserted.

In Euclidean space, \(\nabla\) is ordinary differentiation and \(\exp_p(v)=p+v\). For \(r=|x|>0\) and \(u=x/r\), direct differentiation gives
\[
\operatorname{grad}r=u,\qquad
H_rX=\frac{X-\langle X,u\rangle u}{r},\qquad
\Delta r=\frac{n-1}{r}.
\]
The radial component vanishes; each normal component expands by \(1/r\). This is the model for the [current-vector Hessian calculation](N-M-geometric-inputs.md#current-vectors-and-the-distance-hessian).

Metric completeness means that every Cauchy sequence for \(d_g\) converges. Its consequences for minimizing segments and compactness are [precisely imported below](N-M-geometric-inputs.md#completeness-and-minimizing-segments).

Return to the [reader entrance](../overview.md#reader-entrance-and-available-operations). These rules provide the operations needed to differentiate a geodesic variation; they do not assume a previous course in comparison geometry.
