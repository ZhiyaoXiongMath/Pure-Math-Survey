---
{
  "schema_version": "2.0.0",
  "id": "N-D-jacobi",
  "kind": "definition",
  "title": "Normal Jacobi fields and radial Jacobi tensors",
  "facets": [
    "foundations",
    "methods"
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
      "locator": "Section 2, equations (2.1), (2.4)–(2.7), pp. 6–8; Lemma 5.3, p. 18; equations (5.9)–(5.13), pp. 19–20",
      "role": "support"
    },
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Section 9.2, pp. 57–58",
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
      "target": "N-D-riemannian"
    }
  ]
}
---

# Normal Jacobi fields and radial Jacobi tensors

## Canonical statement

```latex
Let \(\gamma:[0,T]\to(M,g)\) be a unit speed geodesic. A normal Jacobi field is a vector field \(J\) along \(\gamma\) satisfying
\[
\langle J,\dot\gamma\rangle=0,\qquad
D_t^2J+R(J,\dot\gamma)\dot\gamma=0.
\]
In a parallel orthonormal normal frame let \(\mathcal R(t)w=R(w,\dot\gamma(t))\dot\gamma(t)\). The radial Jacobi tensor is the matrix solution
\[
A''+\mathcal R A=0,\qquad A(0)=0,\qquad A'(0)=I.
\]
Where \(A\) is invertible, set \(S=A'A^{-1}\), \(m=\operatorname{tr}S\), and \(j=\det A\), choosing the initial orientation so that \(j(t)>0\) for small \(t>0\).
```

## Purpose and inputs

We want to measure the spreading of geodesics from a fixed point \(p\). A variation of their initial direction produces a field along one ray. The metric connection and parallel-frame rule are available from the [operational entry](N-D-riemannian.md#operational-entry).

### Radial variation and the exponential differential

Fix \(|v|=1\) and \(w\perp v\). Choose a smooth curve \(v(s)\) in the unit tangent sphere with \(v(0)=v\), \(v'(0)=w\), and put
\[
F(s,t)=\exp_p(tv(s)),\qquad
T=\partial_tF,\qquad J_w=\partial_sF\big|_{s=0}.
\]
Each \(t\)-curve is a geodesic. Torsion-freeness along this variation gives \(D_t\partial_sF=D_s\partial_tF\). Commuting the next derivatives using the stated curvature convention gives
\[
D_t^2J_w+R(J_w,T)T=0,\qquad J_w(0)=0,\qquad D_tJ_w(0)=w.
\]
The last identity differentiates the initial velocity \(v(s)\). Also \(\langle J_w,T\rangle''=0\), and its value and first derivative vanish at zero; hence \(J_w\perp T\).

In a parallel normal frame, uniqueness of the linear ODE gives \(J_w(t)=A_v(t)w\). Differentiating the map itself keeps track of an important factor of \(t\):
\[
\Phi(t,v)=\exp_p(tv),\qquad
d\Phi(\partial_t)=T,\qquad
d\Phi(w)=d(\exp_p)_{tv}(tw)=A_v(t)w.
\]
Thus \(d(\exp_p)_{tv}(w)=A_v(t)w/t\) for a tangent-space vector \(w\perp v\). An angular vector for \(\Phi\) and a vector at \(tv\in T_pM\) are different inputs; confusing them loses the factor \(t\).

This is Eschenburg's Lemma 5.3, now derived from the actual variation. It will convert [Jacobi estimates into map and length estimates](N-M-riccati.md#jacobi-length-and-exponential-map-use).

### The pole and the positive interval

The ODE gives \(A''(0)=0\) and \(A'''(0)=-\mathcal R(0)\). Smoothness therefore gives
\[
A(t)=tI-\frac{t^3}{6}\mathcal R(0)+O(t^4),\qquad
A'(t)=I-\frac{t^2}{2}\mathcal R(0)+O(t^3).
\]
In particular, \(A=tI+O(t^3)\), \(A'A^{-1}=t^{-1}I+O(t)\) where invertible, and \(\det A/t^{n-1}\to1\). Near \(p\), the estimates can be chosen uniformly in \(v\), by smooth dependence and compactness of the unit tangent sphere.

A nonzero vector in \(\ker A(t)\) is exactly a nontrivial normal Jacobi field vanishing at \(0,t\). Hence \(A\) is invertible before the first conjugate time. The [cut-domain input](N-M-cut-integration.md#the-uncut-domain-and-the-ball-integral) puts every minimizing uncut ray inside that interval.

### From the radial differential to volume density

Use an orthonormal angular basis at \(v\) for the ordinary unit-sphere measure \(dv\). Gauss lemma says that \(d\Phi(\partial_t)\) is unit and orthogonal to each \(d\Phi(w)\). The pullback metric on the product radial/angular tangent space has Gram matrix
\[
\Phi^*g=
\begin{pmatrix}1&0\\0&A^TA\end{pmatrix},
\qquad
\sqrt{\det(\Phi^*g)}=\sqrt{\det(A^TA)}=|\det A|.
\]
The ordinary metric-volume rule from the entrance now applies. Initially \(\det A>0\); it cannot change sign without vanishing. On the uncut domain,
\[
d\operatorname{Vol}_g=j(t,v)\,dt\,dv,\qquad j(t,v)=\det A_v(t)>0.
\]
Here the formula for a pullback density is local. Using it once for each point of a whole ball still requires the uncut parametrization; that global step is not a consequence of the determinant identity.

For comparison with familiar normal coordinates \(x=tv\), Euclidean polar coordinates give \(|dx|=t^{n-1}dt\,dv\). Thus the same calculation reads
\[
j(t,v)=t^{n-1}\sqrt{\det(g_{ij}(tv))}.
\]
This explains why the Jacobi determinant measures geometric volume, rather than merely defining another symbol.

### One complete model calculation

For constant sectional curvature \(k\), the normal equation is \(A''+kA=0\). Its initial data give \(A=s_kI\), so Gauss lemma and the same Gram calculation yield
\[
g=dt^2+s_k(t)^2g_{S^{n-1}},\qquad
j_k=s_k^{n-1},\qquad S_k=c_kI,\qquad m_k=(n-1)c_k.
\]
These formulas hold on \(0<t<D_k\), where \(s_k>0\). They explain the denominator in [normalized density comparison](N-M-trace.md#normalized-density-and-the-small-radius-limit); at the spherical endpoint division stops.

Return to the [Ricci-to-volume route](../overview.md#ricci-lower-bounds-to-ball-volume). Changing a parallel orthonormal frame changes the matrix representation by orthogonal conjugation, not these geometric quantities.
