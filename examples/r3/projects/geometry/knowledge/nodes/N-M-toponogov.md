---
{
  "schema_version": "2.0.0",
  "id": "N-M-toponogov",
  "kind": "mechanism",
  "title": "From local Rauch comparison to global triangle comparison",
  "facets": [
    "methods"
  ],
  "question_ids": [
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Lang-2026",
      "locator": "Corollary 1.22, p. 14; Corollaries 3.20–3.21, pp. 43–44; Lemmas 5.1–5.9 and Definition 5.10, pp. 64–67; Theorem 5.12, Propositions 5.13–5.14 and Theorem 5.15, pp. 67–70",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-R-rauch"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-triangle"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    },
    {
      "relation": "proof_input",
      "target": "N-M-geometric-inputs"
    }
  ]
}
---

# From local Rauch comparison to global triangle comparison

## Route and fixed data

Let \((M^n,g)\), \(n\ge2\), be connected, complete, smooth and without boundary, with \(\sec_M\ge k\). Set \(D_k=\pi/\sqrt{k}\) for \(k>0\) and \(D_k=\infty\) otherwise. All sides below are chosen distance-minimizing segments.

For the principal result, choose distinct \(p,x,y\), put
\[
a=d(p,x),\qquad b=d(p,y),\qquad c=d(x,y),\qquad P=a+b+c,
\]
and assume strict triangle inequalities and \(P<2D_k\). These imply \(a,b,c<D_k\), so the SSS model triangle is determined up to isometry.

Match model and actual initial directions by a tangent-space isometry. The resulting local exponential map preserves radial speed, while Rauch bounds angular speed from above. A model chord contained in that normal domain therefore gives local same-angle length comparison and, by the cosine law, local SSS angle comparison.

For a global triangle, Lang's gluing proposition turns a violating hinge into a nearby violating hinge of less than \(4/5\) its perimeter. Completeness and one uniformly valid local comparison near the limiting vertex make such an infinite sequence impossible. Further angle-to-chord conversion uses all required auxiliary hinges.

The proof uses [a local comparison map](#the-comparison-map-on-a-common-normal-domain), [speed and length estimates](#from-angular-and-radial-speeds-to-length), [uniformity for moving centers](#a-uniform-local-neighborhood-for-moving-centers), and [a shrinking counterexample](#shrinking-hinges-and-the-cauchy-limit). The [gluing input](#the-exact-gluing-and-globalization-inputs) is imported with its full hypotheses.

Return to the [triangle-comparison route](../overview.md#toponogov-from-local-lengths-to-global-triangles). The complete principal statement is [Toponogov angle, hinge and chord comparison](N-R-toponogov.md#canonical-statement).

## Three different comparison experiments

Let \(\alpha=\angle xpy\). The SSS triangle \((\bar p,\bar x,\bar y)\) fixes \(a,b,c\); write \(\bar\alpha=\angle\bar x\bar p\bar y\). The same-angle model hinge \((\hat p,\hat x,\hat y)\) fixes \(a,b,\alpha\); its opposite distance is not prescribed to be \(c\).

The conclusions have different directions because the fixed data differ:
\[
\alpha\ge\bar\alpha,\qquad
c\le d_k(\hat x,\hat y),\qquad
d_M(u,v)\ge d_k(\bar u,\bar v)
\]
for matching \(u\in px,\ v\in py\) and points on the SSS model sides. The final inequality compares chords within the SSS experiment, not within the same-angle model.

For auxiliary hinges in the proof, only the two radial sides must be nonzero: \(p\notin\{x,y\}\), while \(x=y\) is allowed. Their perimeter is still \(P=d(p,x)+d(p,y)+d(x,y)<2D_k\). The imported lemmas allow equality in the triangle inequalities.

For these auxiliary hinges, the SSS comparison angle is defined continuously in \([0,\pi]\). It is \(0\) when \(c=|a-b|\), and \(\pi\) when \(c=a+b<D_k\). This proof convention does not enlarge the strictly nondegenerate principal statement.

## The comparison map on a common normal domain

Fix a vertex \(p\). Choose \(R>0\), with \(R<D_k\), so that \(\exp_p\) maps the tangent ball \(B(0,R)\subset T_pM\) diffeomorphically onto the normal metric ball \(B_M(p,R)\).

Use the \(n\)-dimensional model \(M_k^n\), a point \(o\) in it, and a linear isometry \(I:T_oM_k^n\to T_pM\). The model exponential map is a diffeomorphism on its radius-\(R\) tangent ball. Define
\[
F=\exp_p\circ I\circ(\exp_o^k|_{B(0,R)})^{-1}:
B_k(o,R)\longrightarrow B_M(p,R).
\]
The \(n\)-dimensional model makes the differential comparison well typed; the two hinge directions lie in a totally geodesic model surface \(M_k^2\).

For a unit \(v\in T_oM_k^n\) and \(w\perp v\), write
\[
\bar\gamma_v(t)=\exp_o^k(tv),\qquad
\gamma_{Iv}(t)=\exp_p(tIv),\qquad
\bar J_w(t)=s_k(t)\bar{\mathcal P}_t w.
\]
Here \(\bar{\mathcal P}_t\) is model parallel transport, and \(s_k''+ks_k=0,\ s_k(0)=0,\ s_k'(0)=1\). Thus \(s_k(t)>0\) on \(0<t<R<D_k\).

The [radial-variation identity](N-D-jacobi.md#radial-variation-and-the-exponential-differential) gives
\[
dF(\dot{\bar\gamma}_v(t))=\dot\gamma_{Iv}(t),\qquad
dF(\bar J_w(t))=J_{Iw}(t).
\]
The actual radial segment has no conjugate point before \(R\), because \(\exp_p\) is a diffeomorphism there. The lower-sectional part of [Rauch comparison](N-R-rauch.md#canonical-statement) therefore applies:
\[
|J_{Iw}(t)|\le s_k(t)|w|=|\bar J_w(t)|,\qquad 0<t<R.
\]
For a given \(t<R\), one may choose the terminal time in Rauch strictly between \(t\) and \(R\); no claim about the boundary sphere of the normal ball is needed.

## From angular and radial speeds to length

At \(\bar\gamma_v(t)\ne o\), every tangent vector has a unique decomposition
\[
U=\rho\dot{\bar\gamma}_v(t)+\bar J_w(t),\qquad w\perp v.
\]
Gauss lemma makes these radial and angular terms orthogonal in both manifolds. Hence
\[
|dF(U)|^2
=\rho^2+|J_{Iw}(t)|^2
\le \rho^2+s_k(t)^2|w|^2
=|U|^2.
\]
At \(o\), \(dF_o=I\), so the same estimate holds. Therefore every piecewise \(C^1\) curve \(\bar\sigma\) contained in \(B_k(o,R)\) satisfies
\[
L_M(F\circ\bar\sigma)
=\int |dF(\dot{\bar\sigma})|
\le\int|\dot{\bar\sigma}|
=L_k(\bar\sigma).
\]

To use this estimate, take \(x,y\in B_M(p,R/2)\), and let \(\hat x,\hat y\) be their preimages under \(F\). Their model radial lengths are \(a,b<R/2\), and their included model angle is the actual angle \(\alpha\).

Let \(\bar\sigma:[0,L]\to M_k^n\) be a unit-speed minimizing model segment from \(\hat x\) to \(\hat y\). Completeness of the model gives this segment, and \(L=d_k(\hat x,\hat y)\le a+b\).

The segment really stays in the domain of \(F\). For \(0\le s\le L\),
\[
d_k(o,\bar\sigma(s))
\le\min\{a+s,\ b+L-s\}
\le\frac{a+b+L}{2}
\le a+b<R.
\]
This explicit estimate is the reason for placing the endpoints in the half-radius ball.

Applying the length estimate to this curve yields the local same-angle inequality
\[
c=d_M(x,y)
\le L_M(F\circ\bar\sigma)
\le L_k(\bar\sigma)=d_k(\hat x,\hat y).
\]
A curve through \(o\) causes no difficulty, since \(F\) is smooth there. The construction makes no assertion that \(F\) is available on a global normal domain.

## From same-angle lengths to SSS angles

For fixed \(0<a,b<D_k\), denote by \(h_k(a,b,\theta)\) the opposite distance of the model hinge with included angle \(\theta\in[0,\pi]\). The model cosine laws show that \(h_k\) is continuous and strictly increasing in \(\theta\).

Writing \(h=h_k(a,b,\theta)\), the formulas are
\[
\begin{aligned}
h^2&=a^2+b^2-2ab\cos\theta &&(k=0),\\
\cos(\sqrt{k}h)
&=\cos(\sqrt{k}a)\cos(\sqrt{k}b)
+\sin(\sqrt{k}a)\sin(\sqrt{k}b)\cos\theta &&(k>0),\\
\cosh(\lambda h)
&=\cosh(\lambda a)\cosh(\lambda b)
-\sinh(\lambda a)\sinh(\lambda b)\cos\theta
&&(\lambda=\sqrt{-k},\ k<0).
\end{aligned}
\]
For \(k>0\), the sine factors are positive and the function \(r\mapsto\cos(\sqrt{k}r)\) is decreasing on \([0,D_k]\). For \(k<0\), the hyperbolic-sine factors are positive and hyperbolic cosine is increasing. In each case increasing \(\theta\) increases \(h\).

In the SSS triangle \(c=h_k(a,b,\bar\alpha)\). Thus the local length estimate gives
\[
h_k(a,b,\bar\alpha)=c\le h_k(a,b,\alpha)
\quad\Longrightarrow\quad \bar\alpha\le\alpha.
\]
This equivalence also converts the global angle inequality back into the global same-angle hinge inequality once globalization has been proved.

The strict perimeter hypothesis belongs to the given hinge and its SSS comparison data. The same-angle model hinge uses \(a,b<D_k\); its opposite distance, and hence its perimeter, need not equal those of the given hinge.

## A uniform local neighborhood for moving centers

A normal ball centered only at a prospective limit \(q\) would not suffice: the shrinking hinges have moving vertices. We need one radius that works for every nearby vertex.

The precise smooth input is the following consequence of the inverse function theorem: for each \(q\), there are a neighborhood \(V\) and \(R>0\) such that \(\exp_p|_{B(0,R)}\) is a diffeomorphism onto a normal metric ball for every \(p\in V\).

It comes from applying that theorem to
\[
\mathcal E:TM\supset\Omega\longrightarrow M\times M,
\qquad \mathcal E(p,\xi)=(p,\exp_p\xi)
\]
at \((q,0)\), then shrinking the base neighborhood and the tangent radius. Gauss lemma supplies the normal metric-ball and radial-minimizing interpretation. This is the input used in Lang's proof of Corollary 1.22 and Theorem 5.12.

Shrink \(R\) so that \(R<D_k\), and choose \(\delta>0\) with
\[
B(q,\delta)\subset V,\qquad 2\delta<R/2.
\]
For every \(p,x,y\in B(q,\delta)\), the distances from \(p\) to \(x,y\) are \(<2\delta<R/2\). The preceding construction, now centered at \(p\), proves angle comparison for every chosen hinge with these vertices.

The radius \(R\) is uniform in \(p\), and the small chosen minimizing sides are the unique normal radial segments. This is the local input consumed by the Cauchy-limit argument below.

## The angle used by the metric gluing lemmas

Our angles are angles between initial tangent vectors. Lang's metric formulation uses the limit superior of model comparison angles of shorter subsegments. These agree in a smooth Riemannian manifold; the following local calculation supplies the identification.

Let \(u,v\) be unit vectors at \(p\), with \(\alpha=\arccos\langle u,v\rangle\), and put
\[
f(s,t)=d_M(\exp_p(su),\exp_p(tv))^2.
\]
Squared distance is smooth near the diagonal: in a common normal neighborhood it equals \(g_z(\log_z z',\log_z z')\), and the preceding inverse-function construction makes \(\log_z z'\) smooth.

Here \(f(s,0)=s^2,\ f(0,t)=t^2\), and the quadratic part at the origin is \(|su-tv|^2\). Thus \(f_{st}(0,0)=-2\cos\alpha\). Integrating the mixed derivative over \([0,s]\times[0,t]\) gives
\[
f(s,t)=s^2+t^2-2st\cos\alpha+st\,o(1),
\qquad s,t\downarrow0.
\]
The remainder is uniform as both variables tend to zero, even if their ratio tends to zero or infinity.

The Euclidean comparison angle \(\beta(s,t)\) therefore satisfies
\[
\cos\beta(s,t)=\frac{s^2+t^2-f(s,t)}{2st}
=\cos\alpha+o(1),
\]
so \(\beta(s,t)\to\alpha\). Lang's Remark 5.6 makes the metric upper angle independent of the fixed model curvature \(k\); hence it is this same \(\alpha\).

## The exact gluing and globalization inputs

For a hinge \(H_p(x,y)\), write \((A_k)\) for
\[
\angle xpy\ge\bar\angle_k(p;x,y),
\]
where the right side is its SSS comparison angle. A segment \(px\) is *balanced* if, for any interior \(z\in px\) and any nonzero segment \(zy\),
\[
\angle pzy+\angle yzx=\pi.
\]
In a Riemannian manifold the velocities toward \(p\) and \(x\) are opposite, so this identity follows directly from the ordinary angle between tangent vectors.

Lang §5.3 fixes \(k\) and assumes that every segment is balanced and every pair of points at distance \(<D_k\) is joined by a minimizing segment. Completeness of the present connected Riemannian manifold supplies the latter by Hopf–Rinow.

Under these ambient assumptions, Proposition 5.14 states: if \(H=H_p(x,y)\) has two nonzero minimizing sides and \(P(H)<2D_k\), and every hinge \(H'\) with
\[
P(H')<\frac45P(H)
\quad\text{and at least one endpoint in }px\cup\{y\}
\]
satisfies \((A_k)\), then \(H\) satisfies \((A_k)\). The endpoint here is a radial-side endpoint of \(H'\), not necessarily its vertex.

The proposition uses the auxiliary degenerate-triple convention above; it does not require strict triangle inequalities for all hinges. Its technical proof is imported, rather than replaced by a claim that a local exponential map is globally defined.

The preceding thin-hinge input, Proposition 5.13, has the additional assumptions
\[
a_0=d(p_0,y_0),\quad 0<b_0=d(p_0,x_0)<a_0/5,\quad a_0+b_0<D_k.
\]
If every hinge of perimeter \(<4P(H_0)/5\) with an endpoint in \(\{x_0,y_0\}\) satisfies \((A_k)\), then \(H_0\) does. Proposition 5.14 subdivides a side into such thin pieces and uses Alexandrov's gluing lemma.

For the exact surrounding local-to-global theorem, Lang 5.15 assumes a complete metric space which is locally of curvature \(\ge k\) in the sense of Definition 5.10, plus a minimizing segment between every pair at distance \(<D_k\). It concludes angle, same-angle hinge and SSS chord comparison for every hinge of perimeter \(<2D_k\).

Here Definition 5.10 means that each \(q\) has a neighborhood \(U_q\) whose pairs admit connecting segments and whose hinges with vertices and endpoints in \(U_q\), of perimeter \(<2D_k\), satisfy SSS chord comparison. Lang 5.12 identifies this local condition with \(\sec\ge k\) in a connected Riemannian manifold.

The direction of 5.12 needed here is the sectional-bound-to-local-comparison direction. Its proof uses the same local map and uniform normal radii just developed, followed by Lemma 5.9. Below we use Proposition 5.14 directly; the already proved uniform local angle comparison suffices for its final contradiction.

## Shrinking hinges and the Cauchy limit

Suppose a hinge \(H_0\), of perimeter \(P_0<2D_k\), violates \((A_k)\). The contrapositive of Proposition 5.14 produces another violating hinge \(H_1\), with \(P_1<4P_0/5\), whose endpoint lies in \(p_0x_0\cup\{y_0\}\).

Repeat. For \(j\ge1\), obtain violating \(H_j=H_{p_j}(x_j,y_j)\) with
\[
P_j<\frac45P_{j-1}<\left(\frac45\right)^jP_0,
\]
and an endpoint \(z_j\) lying on the union of the two sides of \(H_{j-1}\). Every hinge remains within the strict perimeter domain of the imported proposition.

The shared-endpoint condition controls where the vertices move:
\[
d(p_j,p_{j-1})
\le d(p_j,z_j)+d(z_j,p_{j-1})
\le P_j+P_{j-1}
<\frac95\left(\frac45\right)^{j-1}P_0.
\]
The first distance is a side length of \(H_j\); the second is at most a side length of \(H_{j-1}\).

For \(m>n\), summing the geometric series gives
\[
d(p_m,p_n)
\le\sum_{j=n+1}^{m}d(p_j,p_{j-1})
\le9P_0\left(\frac45\right)^n.
\]
Thus \((p_j)\) is Cauchy. Completeness gives \(p_j\to q\in M\).

Since \(d(p_j,x_j),d(p_j,y_j)\le P_j\to0\), both endpoints also tend to \(q\). Every point on either chosen side is within \(P_j\) of \(p_j\), so the whole hinges shrink toward this same point.

For large \(j\), all three vertices lie in the uniform neighborhood \(B(q,\delta)\) constructed above. Local angle comparison then holds at the moving vertex \(p_j\), contradicting the choice of \(H_j\). Hence every hinge with two nonzero sides and \(P<2D_k\) satisfies \((A_k)\).

The proof did not continue a single normal-coordinate comparison map across the manifold. It combined uniformly valid local comparisons with a global shrinking argument, and completeness was used to keep the limiting point inside \(M\).

## Global hinge and chord comparison

For the strictly nondegenerate principal triangle, apply the global angle result at each of its three vertices. The monotonicity of \(h_k(a,b,\theta)\) then gives the same-angle opposite-distance inequality at \(p\).

For chords we import the lower-curvature part of Lang Lemma 5.9: let \(H_p(x,y)\) have \(P<2D_k\) and balanced sides. Suppose every pair of points in \(S=px\cup py\) admits a connecting segment and every hinge formed from two such segments satisfies \((A_k)\). Then matching points on the SSS model sides satisfy
\[
d_M(u,v)\ge d_k(\bar u,\bar v),\qquad u\in px,\quad v\in py.
\]
Thus angle comparison for this one original hinge alone is not the stated input to the chord-conversion lemma.

The global result supplies all the required auxiliary angle inequalities. To check their perimeter domain, take \(u_1,u_2\in px\), with distances \(r_1\le r_2\) from \(p\), and \(v\in py\), with \(d(p,v)=s\). Using a chosen minimizing \(xy\),
\[
\begin{aligned}
P(u_1,u_2,v)
&\le (r_2-r_1)+(r_1+s)+(a-r_2+c+b-s)\\
&=a+b+c=P<2D_k.
\end{aligned}
\]
Any three points of \(S\) have two on the same side, so this also checks the other arrangements. If all three lie on one side, their perimeter is at most \(2\max\{a,b\}\le P\).

Hopf–Rinow gives the connecting segments, and smooth Riemannian geometry gives balanced sides. Lemma 5.9 now applies with all its hypotheses checked. Coincident points or \(u=p\) or \(v=p\) give the trivial limiting cases.

## First failures when conditions are changed

Using the map \(F\) on a curve that leaves \(B_k(o,R)\) invalidates the differential-to-length step: its inverse exponential coordinate is no longer in the chosen domain. The containment estimate is therefore part of the proof, not an optional convenience.

A normal neighborhood at \(q\) without a uniform radius for nearby \(p_j\) does not justify the last contradiction. Removing completeness leaves the Cauchy sequence without a guaranteed limit in \(M\); removing the minimizing-side hypothesis removes the metric perimeter estimates and the imported gluing hypotheses.

At perimeter \(2D_k\), the strict form of Proposition 5.14 and Theorem 5.15 no longer applies, and the SSS model may be degenerate. This node makes no assertion about that endpoint case. Replacing sectional curvature by a Ricci bound also removes the directional Rauch estimate used to bound \(dF\).

## Source and proof boundary

The controlling source is Lang, *Riemannian and Metric Geometry*, preliminary and incomplete version dated 5 January 2026. Relevant locations are Corollary 1.22, p. 14; Corollaries 3.20–3.21, pp. 43–44; and §5.1–§5.3, pp. 63–70.

The comparison-map calculation, model-curve containment, moving-center application, Cauchy estimate, and auxiliary-perimeter check are written out above. Propositions 5.13–5.14, Alexandrov's technical gluing argument, and the angle-to-chord conversion in Lemma 5.9 remain explicitly imported.

The original PDF prints \(4/5\) consistently in the shrinking argument on p. 70. An extraction order of \(5/4\) is not a printed mathematical error; the earlier contrary typography note is removed after inspecting the page image.

The shared [current-vector and Hessian construction](N-M-geometric-inputs.md#current-vectors-and-the-distance-hessian) identifies the same radial variations in the local comparison branch. This triangle proof consumes their Jacobi and orthogonality properties, without assuming a globally smooth distance Hessian.

Return to the [triangle-comparison route](../overview.md#toponogov-from-local-lengths-to-global-triangles).
