# S02 representative reader tasks and their actual answers

Date: 2026-10-12. Revision: S02 radial representative r1, epoch 2, writer generation 3. Reviewer mode: author reread. The agent knew the developing text while solving these tasks; this is not a blind novice study, an observed human reading session or independent peer review.

## Obligation coverage

Starting from the canonical targets and the smooth-manifold baseline, the author reconstructed the required chain: metric and connection operations; curvature as an operator versus its trace; radial variation and initial data; model solution and first zero; current-vector Hessian; symmetric Riccati; singular comparison; Jacobi length; geometric polar density; the uncut substitution; zero extension and angular limit; weighted averaging and its regularity; a noncircular spherical endpoint; and an actual use plus failed changes of assumptions.

This reconstruction was compared with S01's 28 obligations, not used to reduce them to the old output plan. O01–O18 are addressed by the revised entrance, radial and volume route. O19 is now addressed by the limited endpoint index-lemma calculation using the already stated nonnegativity, without importing a full Morse index theorem. O20 is addressed by the complete sine integral and universal-cover argument. O21–O25 still require final integration and rereading of the Hadamard and Toponogov candidate revisions; their complete canonical statements are retained. O26–O28 are exercised below and by the wider-branch map. This representative record therefore does not accept the entire seven-theorem revision.

Repairs are actual text, not labels: the \(t\) in \(d\exp_{tv}(tw)\), the inverse \(A^{-1}\), the Gram determinant, the \(\mu u\to0\) boundary value, the null-set substitution, and absolute continuity now appear in the relevant calculations. Imported geometry is distinguished from the operation performed with it. Every decisive fast step in the radial route links to its slow subsection, and the slow nodes return to their purpose in the overview.

## Fast route reconstruction

Task: from the overview's Ricci route and its stated inputs, explain why a lower Ricci bound controls the ratio of concentric ball volumes. Answer obtained: the Hessian endomorphism along an uncut ray is \(S=A'A^{-1}\); its trace satisfies \(m'+m^2/(n-1)+(n-1)k\le0\). Singular scalar comparison gives \(m\le(n-1)c_k\). Because \(j\) is the polar density and \(j'/j=m\), \(\lambda=j/s_k^{n-1}\) decreases from \(1\). Zero extension preserves this order when a ray stops minimizing. Its angular mean \(q\) decreases from \(1\), and the ball ratio is the \(s_k^{n-1}\)-weighted mean of \(q\); thus it decreases. Myers and the null terminal sphere handle \(k>0\) at and after \(D_k\).

The key distinction recovered was that no matrix-order theorem is needed in the trace step. The fast text gives the reason for each transition and direct slower links; a reader must still use the stated cut-locus and completeness inputs. The revised route does not claim to prove those prerequisites.

Task: produce one usable conclusion. With \(k=0\), the model ratio from \(r\) to \(2r\) is \(2^n\); hence \(\operatorname{Vol}B(p,2r)\le2^n\operatorname{Vol}B(p,r)\). Reversing the algebra gives a lower estimate for the smaller ball relative to the known larger ball, but leaves no absolute lower constant.

## Slow step reproduction

Task: obtain the density without defining it to be a determinant. Answer obtained: differentiating the actual radial map sends \(\partial_t\) to the unit tangent \(T\), and an angular vector \(w\) to \(Aw\). Gauss lemma makes these blocks orthogonal. Relative to an orthonormal angular basis the metric matrix is \(\operatorname{diag}(1,A^TA)\). Its volume density is \(\sqrt{\det(A^TA)}=|\det A|\). The expansion \(A=tI-t^3\mathcal R(0)/6+O(t^4)\) fixes the positive sign until the first conjugate point. Thus the uncut density is \(j=\det A>0\).

Task: recover the scalar comparison at the pole. With \(a=m/(n-1)\), \(u=a-c_k\), the inequality is \(u'+(a+c_k)u\le0\). The factor \(\mu=\exp\int_{t_*}^t(a+c_k)\) satisfies \(\mu\sim Ct^2\). Since \(u=O(t)\), \(\mu(\varepsilon)u(\varepsilon)\to0\). Integration on \([\varepsilon,t]\) gives \(u(t)\le0\). This reproduces the missing initial-boundary operation without assigning an infinite initial value to a regular ODE.

Task: justify monotonicity after angular integration. Put \(N(r)=\int_0^r qw\), \(W(r)=\int_0^rw\), \(F=N/W\). For each \(r\), nonincrease of \(q\) gives \(F(r)\ge q(r)\). On a compact interval away from zero, integrability gives absolute continuity of \(N,W\), and \(W\) is bounded below by a positive constant. Therefore \(F'=(w/W)(q-F)\le0\) almost everywhere and absolute continuity gives monotonicity for all pairs of radii. The geometric substitution \(w=s_k^{n-1}\) satisfies every stated assumption.

Task: check an alternative mechanism with the same hypotheses. At an uncut endpoint, write any endpoint-matching field \(V\) as \(J+W\), with \(W\) zero at both ends. The Jacobi equation gives \(I(J,W)=0\), so \(I(V,V)\ge I(J,J)=\nabla^2r(X,X)\). Choosing \(V=s_kE/s_k(L)\) and using sectional curvature at least \(k\) gives \(I(V,V)\le c_k(L)|X|^2\). This independently recovers the lower-sectional Hessian estimate; merely reversing the curvature inequality leaves the first comparison oriented the same way and is not a reverse proof.

## Condition transfer

- Replace the sectional lower bound by a Ricci lower bound: the operator inequality \(\mathcal R\ge kI\) is lost, so matrix comparison is the first invalid step. The trace route survives. On \(S^2(1)\times S^2(1)\), \(\operatorname{Ric}=g\), \(n=4\), but a mixed plane has curvature \(0<1/3\). Its radial mixed Jacobi field is \(tE\), so its Hessian eigenvalue \(1/t\) exceeds \(c_{1/3}(t)\) for small \(t\). This is a concrete failure, beyond merely identifying a missing inference.
- Replace a Ricci lower bound by an upper bound: \(m'=-m^2/(n-1)-Q-\operatorname{Ric}(T,T)\) contains the uncontrolled term \(-Q\), \(Q\ge0\). No lower bound for \(m'\) follows. This observation is a proof failure, not a purported universal counterexample.
- Extend a Jacobi comparison past the actual conjugate time: on curvature \(2\) versus curvature \(1\), \(|\sin(\sqrt2t)|/\sqrt2>|\sin t|\) for some \(t<\pi\) close to \(\pi\). The model interval alone does not repair the lost actual interval.
- Remove cut truncation: on \(S^1_a\times\mathbb R\), the exponential map covers a point through multiple angular lifts once the angular cut is crossed. The claimed ball change of variables first fails by multiplicity. The Jacobi tensor \(A=tI\) remains nonsingular, showing why absence of conjugate points is insufficient.
- Set \(r=D_k\) in a positive-curvature density quotient: \(s_k(D_k)=0\), so division is undefined. The surviving replacement is the terminal-sphere null-set and saturation argument; no limiting value of \(c_k(D_k)\) is assumed.
- Reverse a raywise estimate to seek a global lower-volume theorem: the downward cut jump destroys a lower bound. The thin flat cylinder gives \(\operatorname{Vol}B(p,r)\le2\pi\varepsilon\,\omega_{n-1}^{\mathrm{ball}}r^{n-1}\to0\) while \(\sec=0\). An injectivity restriction is essential to the uncut lower-volume application.
- Remove completeness or simple connectivity in the global branches: the open Euclidean ball lacks a globally defined exponential map on all \(T_pM\); an open round hemisphere is not compact despite its positive curvature. A complete flat cylinder retains an exponential covering but not injectivity. These tests are retained while the full global mechanism revisions are pending.

## Remaining review scope

The representative radial route is ready for an independent content review. The whole seven-interface route is not accepted by this record: Hadamard and Toponogov candidate integration, their independent checks, a final full-route record and a new snapshot are still pending. General equality classifications, degenerate/perimeter-endpoint triangles, focal/tube and other named neighboring branches remain outside the focused question, with their broader statuses preserved.
