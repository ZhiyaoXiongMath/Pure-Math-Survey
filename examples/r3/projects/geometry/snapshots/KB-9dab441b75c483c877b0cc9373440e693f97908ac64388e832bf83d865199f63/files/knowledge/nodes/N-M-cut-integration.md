---
{
  "schema_version": "2.0.0",
  "id": "N-M-cut-integration",
  "kind": "mechanism",
  "title": "Cut-time truncation and weighted averages produce Bishop–Gromov",
  "facets": [
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-volume"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Section 5, formulas (5.9)–(5.15), pp. 19–20",
      "role": "support"
    },
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Section 8.1, p. 54",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-M-trace"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-distance"
    },
    {
      "relation": "proof_input",
      "target": "N-R-myers"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    }
  ]
}
---

# Cut-time truncation and weighted averages produce Bishop–Gromov

## From one ray to a whole ball

Let \((M^n,g)\) be smooth, connected and complete without boundary, \(n\ge2\), with \(\operatorname{Ric}\ge(n-1)kg\). Fix \(p\). Use the model functions and saturated volume of [the canonical model definition](N-D-model.md).

The preceding [trace calculation](N-M-trace.md#normalized-density-and-the-small-radius-limit) controls \(j/s_k^{n-1}\) along uncut rays. It has not yet shown that integrating these rays counts every ball point once.

### The uncut domain and the ball integral

We import the cut-domain theorem in its precise form: with
\[
U_p=\{tv:v\in S_pM,\ 0<t<\tau_p(v)\},
\]
\(\exp_p:U_p\to M\setminus(\{p\}\cup\operatorname{Cut}(p))\) is a diffeomorphism. The omitted set has volume zero; before cut there is no conjugate point. The cut time is measurable (in fact continuous in the extended-real topology).

On this domain \(r_p(\exp_p(tv))=t\). Thus the preimage of the open ball is exactly \(t<r\) together with \(t<\tau_p(v)\). Apply the already derived [polar density](N-D-jacobi.md#from-the-radial-differential-to-volume-density):
\[
\operatorname{Vol}B(p,r)
=\int_{S_pM}\int_0^{\min\{r,\tau_p(v)\}}j(t,v)\,dt\,dv.
\]
Endpoints do not change the integral. The imported theorem supplies bijective geometry and the null set; the displayed substitution is the actual use of those inputs.

### Zero extension and angular averaging

Set \(h(t,v)=j(t,v)\) for \(0<t<\tau_p(v)\) and \(h(t,v)=0\) for \(t\ge\tau_p(v)\). For \(0<t<D_k\), the normalized function \(h/s_k^{n-1}\) decreases before cut, can only jump downward to zero there, and is zero afterwards.
\[
q(t)=\frac1{\omega_{n-1}}\int_{S_pM}
\frac{h(t,v)}{s_k(t)^{n-1}}\,dv,\qquad
0\le q(t)\le1.
\]
Integrating the raywise order shows that \(q\) is nonincreasing. Each direction has positive cut time, and its normalized density tends to one at zero. The bound by one on the finite-measure sphere allows dominated convergence, so \(q(0+)=1\).

This explicitly justifies exchanging the angular average and the small-radius limit. Uniform local Taylor estimates provide an alternative argument.

### A positive weighted average

Here is the one-dimensional argument used next. Suppose \(q\ge0\) is nonincreasing, \(w>0\) almost everywhere, and \(w,qw\) are integrable on every \((0,r)\) considered. Define
\[
W(r)=\int_0^r w(t)\,dt>0,\quad
N(r)=\int_0^r q(t)w(t)\,dt,\quad
F(r)=\frac{N(r)}{W(r)}.
\]
For \(t<r\), \(q(t)\ge q(r)\), so \(F(r)\ge q(r)\). On any compact \([a,b]\) with \(a>0\), \(N,W\) are absolutely continuous and \(W\ge W(a)>0\). The quotient is therefore absolutely continuous there, and
\[
F'(r)=\frac{q(r)w(r)W(r)-N(r)w(r)}{W(r)^2}
=\frac{w(r)}{W(r)}\bigl(q(r)-F(r)\bigr)\le0
\]
for almost every \(r\). Integrating this derivative proves monotonicity for all radii in the interval. The used analysis input is the fundamental theorem for absolutely continuous functions, not the false inference that every continuous function with nonpositive derivative almost everywhere is decreasing.

If \(q(0+)=1\), then for small \(r\), every \(q(t)\), \(0<t<r\), lies within any prescribed error of one. Its positive weighted average does too, giving \(F(0+)=1\).

### Applying the average to geometric volume

For \(0<r<D_k\), choose \(w=s_k^{n-1}\). The model has exactly this positive density. The ball integral and angular average give
\[
\frac{\operatorname{Vol}B(p,r)}{V_k^n(r)}
=\frac{\int_0^r q(t)s_k(t)^{n-1}\,dt}
{\int_0^r s_k(t)^{n-1}\,dt}.
\]
Here \(q\) is measurable and bounded, \(w\) is positive and integrable down to zero, and \(qw\) is integrable. All assumptions of the preceding calculation hold. It proves the ratio is nonincreasing and tends to one at zero.

### The positive-curvature endpoint

For \(k\le0\), \(D_k=\infty\), so every finite radius is covered. For \(k>0\), invoke [Myers](N-M-myers.md), whose index-form proof is independent of this volume comparison, to obtain \(\operatorname{diam}M\le D_k\).

If \(d(p,x)=D_k\), a minimizing ray to \(x\) cannot stay minimizing beyond \(D_k\), since that would contradict the diameter bound. Hence such \(x\) belongs to \(\operatorname{Cut}(p)\), and this terminal sphere has zero volume.
\[
\operatorname{Vol}B(p,D_k)=\operatorname{Vol}M,\qquad
\lim_{r\uparrow D_k}\operatorname{Vol}B(p,r)=\operatorname{Vol}M.
\]
The second equality is continuity from below for the increasing open balls. The model integral also tends to its full-sphere volume and remains constant afterwards. The quotient therefore extends monotonically to all \(r>0\), with no division by \(s_k(D_k)=0\).

### One use and the first failing conditions

If \(\operatorname{Ric}\ge0\), \(V_0^n(r)=\omega_{n-1}r^n/n\). For \(R\ge r>0\), the comparison gives
\[
\operatorname{Vol}B(p,R)\le(R/r)^n\operatorname{Vol}B(p,r),
\qquad
\operatorname{Vol}B(p,2r)\le2^n\operatorname{Vol}B(p,r).
\]
Equivalently it gives a relative lower bound on the smaller ball in terms of the larger one. It gives no absolute noncollapse constant; [thin flat cylinders](N-E-collapse.md) distinguish these claims.

Without cut truncation, the exponential map may count points more than once; the first failure is the claimed bijective ball substitution. [The flat cylinder](N-E-cylinder.md) has this issue even without conjugate points.

A raywise lower estimate also need not survive a downward jump to zero. [Günther comparison](N-R-gunther.md) consequently needs its injectivity restriction. Changing the Ricci inequality fails earlier at the [trace estimate](N-M-trace.md#what-the-hypotheses-do-not-give).

Return to the [Ricci-to-volume route](../overview.md#ricci-lower-bounds-to-ball-volume). Geometry supplies the domain, density and order; one-variable analysis performs the averaging; Myers closes only the positive-curvature endpoint.
