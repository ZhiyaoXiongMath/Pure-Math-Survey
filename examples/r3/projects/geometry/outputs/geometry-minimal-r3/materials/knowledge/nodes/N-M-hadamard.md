---
{
  "schema_version": "2.0.0",
  "id": "N-M-hadamard",
  "kind": "mechanism",
  "title": "Convex Jacobi norm and completeness globalize the exponential map",
  "facets": [
    "methods"
  ],
  "question_ids": [
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Section 5, pp. 33–34; Section 8, pp. 52–53; Theorems 9.1–9.2, pp. 54–55",
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
      "target": "N-D-distance"
    },
    {
      "relation": "proof_input",
      "target": "N-M-geometric-inputs"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    }
  ]
}
---

# Convex Jacobi norm and completeness globalize the exponential map

## Route and hypotheses

Let \((M^n,g)\) be connected, complete, smooth and without boundary, with \(\sec\le0\). Fix \(p\in M\). Completeness first makes \(E=\exp_p\) defined on all of \(T_pM\); nonpositive sectional curvature will make its differential invertible.

Nonpositive sectional curvature makes the squared norm of a radial Jacobi field convex. A field starting at zero with nonzero initial derivative cannot return to zero. Gauss lemma then adds the radial direction and makes \(dE\) invertible.

The metric \(E^*g\) turns \(E\) into a local isometry. Its geodesics from \(0\) are entire radial lines, so the one-point Hopf–Rinow criterion gives completeness; complete lifting gives a covering. Simple connectivity of the target then leaves one sheet.

The route is [no second Jacobi zero](#convexity-prevents-a-second-zero), [invertible differential](#the-radial-and-angular-parts-of-the-differential), [complete pullback metric](#completeness-of-the-pullback-metric), and [covering](#why-the-local-isometry-is-a-covering). Simple connectivity is needed only for [one sheet and unique minimizing geodesics](#one-sheet-and-unique-minimizing-geodesics).

The result is [Cartan–Hadamard](N-R-hadamard.md#canonical-statement). Return to the [global exponential-map route](../overview.md#hadamard-from-local-invertibility-to-a-global-cover).

## Convexity prevents a second zero

For a unit \(v\in T_pM\), put \(\gamma_v(t)=E(tv)\). For \(w\perp v\), let \(J_w\) be the normal Jacobi field with \(J_w(0)=0\) and \(D_tJ_w(0)=w\), using parallel translation to identify the normal spaces.

Metric compatibility and the Jacobi equation give
\[
\frac12\frac{d^2}{dt^2}|J_w|^2
=|D_tJ_w|^2-\langle R(J_w,\dot\gamma_v)\dot\gamma_v,J_w\rangle
\ge0.
\]
The last inequality uses sectional curvature in the plane spanned by \(J_w\) and \(\dot\gamma_v\); a Ricci bound alone does not give it.

If \(w\ne0\), then \(J_w(t)=tw+o(t)\) in a parallel frame, so \(|J_w(t)|^2>0\) for small \(t>0\). A later zero at \(t_0>0\) is impossible: convexity and the zeros at \(0,t_0\) would force \(|J_w|^2\le0\) between them.

Thus
\[
w\ne0\quad\Longrightarrow\quad J_w(t)\ne0\quad(t>0).
\]
Applying this to each \(w\) shows that the angular Jacobi tensor \(A_v(t):w\mapsto J_w(t)\) has no kernel. The next step includes the radial direction, which this normal-field argument has not yet addressed.

## The radial and angular parts of the differential

The [radial-variation calculation](N-D-jacobi.md#radial-variation-and-the-exponential-differential) identifies the field with an actual differential:
\[
J_w(t)=dE_{tv}(tw),\qquad
dE_{tv}(v)=\dot\gamma_v(t).
\]
The factor \(t\) comes from differentiating \(t\,v(s)\) when \(v(s)\) is a curve of unit initial directions with \(v'(0)=w\).

At \(tv\ne0\), decompose any tangent vector to \(T_pM\) as \(a v+w\), with \(w\perp v\). By linearity and Gauss lemma,
\[
dE_{tv}(a v+w)=a\dot\gamma_v(t)+t^{-1}J_w(t),
\qquad
|dE_{tv}(a v+w)|^2=a^2+t^{-2}|J_w(t)|^2.
\]
The two summands are orthogonal. The preceding nonvanishing result makes this norm zero only when \(a=0=w\).

Since domain and codomain have equal dimension, \(dE_{tv}\) is an isomorphism. At the origin \(dE_0=\mathrm{id}_{T_pM}\). Hence \(E\) is a local diffeomorphism everywhere, without any assertion yet that different tangent vectors have different images.

## Completeness of the pullback metric

Invertibility makes
\[
h=E^*g,\qquad
h_u(\xi,\eta)=g_{E(u)}(dE_u\xi,dE_u\eta)
\]
a smooth positive-definite metric on all of \(N=T_pM\). By construction \(E:(N,h)\to(M,g)\) is a local isometry.

For every \(u\in T_pM\), the line \(c_u(s)=su\), \(s\in\mathbb R\), projects to the geodesic \(s\mapsto\exp_p(su)\). A local isometry preserves the Levi–Civita connection, so its local inverses pull that geodesic back to an \(h\)-geodesic.

Moreover \(c_u(0)=0\) and \(c_u'(0)=u\). Uniqueness for the geodesic initial-value problem shows that these lines are all the \(h\)-geodesics issuing from \(0\), and every one is defined for all real times.

Now apply this precise form of Hopf–Rinow: a connected Riemannian manifold is metrically complete if all geodesics from one point extend for all real times. Thus \((T_pM,h)\) is complete. No assertion about straight lines for an arbitrary pullback metric is being used.

Hopf–Rinow is a foundational import; its current application has supplied the single base point \(0\), every initial velocity there, and the required extensions. See the [geometric interfaces](N-M-geometric-inputs.md#complete-local-isometries-and-covering).

## Why the local isometry is a covering

We use the complete-local-isometry covering theorem, retaining its construction here. Surjectivity in the present case already follows from Hopf–Rinow on \(M\): a minimizing segment from \(p\) to any \(y\in M\) writes \(y=\exp_p(u)\).

Fix \(y\in M\) and a normal ball \(B_g(y,\varepsilon)\). For each \(x\in E^{-1}(y)\), define
\[
\Psi_x(z)=\exp_x^h\!\left((dE_x)^{-1}(\exp_y^g)^{-1}(z)\right),
\qquad z\in B_g(y,\varepsilon).
\]
Completeness of \(h\) defines the entire lifted radial segment. Preservation and uniqueness of geodesics give \(E\circ\Psi_x=\mathrm{id}\), so \(\Psi_x\) is a smooth inverse branch with open image.

If two such images meet at \(z'\in N\), reverse the radial segment from \(E(z')\) to \(y\). Its lifted initial velocity is fixed by \((dE_{z'})^{-1}\); geodesic uniqueness forces the two lifts to coincide and their endpoints \(x\) to agree.

These images also exhaust \(E^{-1}(B_g(y,\varepsilon))\). For any point in that preimage, lift the reversed radial segment starting there; completeness gives its endpoint in \(E^{-1}(y)\), and reversal recovers the relevant \(\Psi_x\).

Consequently
\[
E^{-1}(B_g(y,\varepsilon))
=\coprod_{x\in E^{-1}(y)}\Psi_x(B_g(y,\varepsilon)),
\]
with \(E\) a diffeomorphism from each sheet to the ball. This is the covering property; local nonsingularity by itself would not have supplied these full sheets.

## One sheet and unique minimizing geodesics

The space \(T_pM\cong\mathbb R^n\) is connected. If \(M\) is simply connected, the elementary covering-space theorem says that a connected covering over \(M\) has one sheet. Thus \(E\) is bijective and its smooth local inverses form a global smooth inverse.

Repeat the argument with any \(q\in M\) as base point. A minimizing geodesic from \(q\) to \(r\), parametrized on \([0,1]\), has initial velocity \(\exp_q^{-1}(r)\). Hopf–Rinow gives existence, and injectivity of \(\exp_q\) and geodesic uniqueness give uniqueness.

On the [flat cylinder](N-E-cylinder.md#explanation-and-evidence), Jacobi fields have no second zero and the exponential map is a covering with multiple sheets. Removing simple connectivity therefore breaks the one-sheet step, not convexity or covering.

Removing completeness breaks the argument earlier: on an open Euclidean ball, geodesics may leave the manifold in finite time, so \(\exp_p\) need not be defined on all \(T_pM\). The pullback metric on that entire vector space is then unavailable.

## Source and proof boundary

Bishop, arXiv:1303.5390v2, §9.1, Theorems 9.1–9.2, pp. 54–55, supplies the no-conjugate-point and pullback-covering route. The one-point completeness criterion is in §8, pp. 52–53; Gauss lemma and the Jacobi equation are in §5, pp. 33–34.

The Jacobi/differential decomposition, the pullback application and the sheet construction above are developed explicitly. Hopf–Rinow, connection preservation by a local isometry, geodesic uniqueness and the elementary covering-space theorem remain precise foundational inputs.

In Bishop's printed computation of \((|J|^2)''\) on p. 55 the curvature summand lacks the factor \(2\). The displayed identity here follows by differentiating directly in the conventions of [curvature and normalization](N-D-curvature.md#canonical-statement); the sign and no-zero argument are unchanged.

Return to the [global exponential-map route](../overview.md#hadamard-from-local-invertibility-to-a-global-cover).
