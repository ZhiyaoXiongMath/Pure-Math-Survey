# S02 seven-interface author review

Date: 2026-10-12. This record follows integration of the two global candidate mechanisms and the main author's full reread of all seven canonical statements, their connecting mechanisms and the stated boundary examples. It supersedes the incomplete scope of the representative r1 task record for the current live revision. The fixed representative packet retains its original bytes.

The work is author-side mathematical review. It includes a separately authored global candidate and main integration checks; neither is the independent nonauthor review required for the stage. No target student was observed, and no blinded reconstruction is claimed.

## Obligations reconstructed from the question

The smooth-manifold reader can use elementary calculus, linear algebra and ODEs but cannot be assumed to know connection calculus, Jacobi fields, cut loci or global comparison. The canonical target determines what must be constructed before each use. S01's independent reconstruction was then used as an omission challenge.

| Obligation | Actual operation or retained boundary |
|---|---|
| O01 | All seven canonical statements reread for quantified curvature, domain, fixed model constant and conclusion; no canonical statement was weakened. |
| O02 | Metric volume, connection rules, parallel frame, gradient and Hessian endomorphism; Euclidean distance differentiated. |
| O03–O04 | Radial geodesic variation differentiated, initial Jacobi data obtained, tensor Taylor expansion and invertibility explained. |
| O05 | Constant-curvature ODE solved and used to obtain the polar metric, density, Hessian and trace; first model zero excluded. |
| O06–O09 | Current vectors converted by \(A^{-1}\); Wronskian and Riccati calculated; exact singular matrix import applied; Jacobi logarithmic length integrated; upper-bound continuation and normal/radial Hessian components checked. |
| O10–O11 | Riccati traced with the eigenvalue square inequality; loss of direction located; singular scalar comparison performed by an integrating factor. |
| O12–O13 | Actual polar differential and block Gram determinant give \(j\); determinant differentiation and the model denominator give normalized density and its initial limit. |
| O14–O16 | The uncut diffeomorphism and null set are imported, then the ball preimage is substituted; cut density is set to zero; angular dominated convergence and the absolutely continuous weighted quotient are proved. |
| O17–O18 | Independent Myers proof, terminal null sphere and volume saturation close positive curvature; doubling and relative-volume algebra are executed without an absolute noncollapse claim. |
| O19–O20 | Fixed-end second variation is stated, the restricted index lemma is derived by integration by parts, the trial-field Hessian integral and Myers sine integral are computed, and compactness/finite fiber are proved using the exact completeness inputs. |
| O21–O22 | Squared Jacobi norm is differentiated, the full exponential differential is checked, the pullback metric's radial geodesics give completeness, and evenly covered sheets plus simple connectivity give the global diffeomorphism and uniqueness. |
| O23–O25 | SSS, SAS and chord data are separated; the local map and every curve-speed estimate have a common normal domain; chord containment, uniform nearby centers, exact gluing assumptions, \(4/5\) shrinking, \(9/5\) displacement and Cauchy tail are checked; all connecting-hinge perimeters for chord conversion are verified. |
| O26 | Changed hypotheses are tested at their first failed operation; proof failures and concrete counterexamples are distinguished. |
| O27 | The overview links directly to decisive slow subsections; the slow nodes return to their route and identify where their output is used. |
| O28 | Existing Günther, rigidity, Cheng and splitting branches remain visible; pending focal, tube, spectral, isoperimetric, topology, quantitative and neighboring theories retain their broader status. |

The main additional repairs found during integration were the missing curvature-operator entrance, the absence of a concrete index-form alternative, the need to name moving-center uniformity, and the distinction between the \(9/5\) consecutive-displacement bound and its summed tail factor \(9\). The canonical claims remain the same; improved explanatory depth is not evidence for expanded endpoint or equality theorems.

## Fast route reconstruction

Radial and volume answer: a unit initial direction generates a normal Jacobi tensor \(A\). Its relative derivative \(S=A'A^{-1}\) is the normal distance Hessian. Sectional curvature controls the matrix equation, whereas a Ricci lower bound and Cauchy--Schwarz control its trace. The scalar comparison has a singular initial point, handled by a vanishing integrating-factor boundary term. The polar Gram matrix identifies \(\det A\) with actual volume density, so the trace inequality decreases density relative to the model. The cut domain counts each regular ball point once; zero extension preserves order. Angular and positive weighted averaging convert that order into the global ball ratio, and Myers closes the spherical endpoint.

Sectional answer: comparing \(S\) with \(c_kI\) gives Hessian comparison after the current-vector identification. Differentiating \(\log(|J|/(|J'(0)|s_k))\) gives Rauch. Under an upper sectional bound its lower length estimate prevents an earlier actual conjugate point; under a lower bound this continuation argument is unavailable.

Myers answer: sine fields vanish at both endpoints of a hypothetical too-long minimizing segment. The sum of their index forms uses Ricci and is negative. Completeness turns this length exclusion into a diameter bound and compactness; the complete universal cover gives a finite fiber and finite fundamental group.

Hadamard answer: nonpositive sectional curvature makes \(|J|^2\) convex, excluding a second zero. The radial direction plus the Jacobi angular directions make \(d\exp_p\) invertible. Pulling back the metric makes \(\exp_p\) a local isometry from a complete domain because every geodesic from zero is an entire radial line. Lifting small target radial balls yields disjoint exhaustive inverse branches. Only the final one-sheet step uses simple connectivity.

Toponogov answer: the local exponential comparison map preserves radial speed and contracts angular speed. A contained model chord gives a local SAS estimate and the model cosine law gives local SSS angles. The exact shrinking input creates arbitrarily small violations whose vertex displacements are summable. Completeness and a uniform normal radius near their limit contradict local comparison. Chord comparison additionally requires all auxiliary connecting hinges; their perimeter estimate allows the already global angle theorem to be used.

## Slow step reproduction

The main author's detailed radial answers are retained in the representative task record. The global candidate author's detailed answers are retained in S02-global-reader-tasks-20261012.md. During integration the main author independently recomputed the following operations from their formulas:

- For \(a v+w\) at \(tv\), \(d\exp_p(a v+w)=aT+J_w(t)/t\). Gauss lemma gives squared norm \(a^2+|J_w(t)|^2/t^2\). Its kernel is zero because convexity forbids a second Jacobi zero.
- A local isometry pulls geodesics back, so \(s\mapsto su\) is an \(h=\exp_p^*g\) geodesic for every initial \(u\). The single-base-point Hopf--Rinow criterion applies to all these velocities, not to an arbitrary collection of curves. The inverse branch \(\exp_x^h\circ(dE_x)^{-1}\circ(\exp_y^g)^{-1}\) exists on the target normal ball; reversal of its radial segment proves disjointness and exhaustiveness.
- For a model chord of length \(L\le a+b\), a point at arclength \(s\) has distance at most \(\min(a+s,b+L-s)\le(a+b+L)/2\le a+b<R\). This verifies that the whole curve lies in the map's domain before integrating \(|dF(U)|\le|U|\).
- Writing \(q=4/5\), shared endpoints give \(d(p_j,p_{j-1})\le P_j+P_{j-1}<(9/5)q^{j-1}P_0\). Summing from \(n+1\) gives the tail \(9q^nP_0\), so vertices and endpoints converge together. A radius valid for every nearby base point is required for the final local contradiction.
- For \(u_1,u_2\in px\) at radii \(r_1\le r_2\), and \(v\in py\) at radius \(s\), the sum \((r_2-r_1)+(r_1+s)+(a-r_2+c+b-s)\) is exactly \(P\). Thus every connecting-hinge perimeter is below \(2D_k\). The angle inequality for one hinge would not have sufficed.
- The smooth tangent-angle identification follows from \(f(s,t)=d(\exp_p(su),\exp_p(tv))^2=s^2+t^2-2st\cos\alpha+st\,o(1)\). Integrating the continuous mixed derivative makes the remainder valid even for unequal shrinking rates; the Euclidean comparison angle tends to \(\alpha\).

The technical triangle gluing/conversion lemmas, Hopf--Rinow, cut-locus theorem, connection existence and standard curvature identities are still imports. Their exact hypotheses are named and checked where used.

## Condition transfer

The radial record supplies concrete product, cylinder, round-sphere and collapsing-family tests. The global reread identifies three further boundaries:

1. Local nonsingularity of \(\exp_p\) does not give a cover until completeness and the full inverse branches are checked. On a complete flat cylinder the covering survives while the one-sheet conclusion fails; on an open Euclidean ball even the everywhere-defined exponential map is unavailable.
2. A Toponogov comparison curve outside the common normal ball has no established derivative estimate along its entire length. The short-chord containment computation repairs this local use; the shrinking argument, not extrapolation of that map, repairs the global step.
3. Removing moving-center uniformity leaves no common radius for the small hinges. Removing completeness leaves no guaranteed limit inside the manifold. Removing minimizing sides invalidates the distance/perimeter inputs. Setting perimeter equal to \(2D_k\) exceeds the strict imported interface; none of these proof failures is itself a claim that all possible extended theorems are false.

The prescribed conclusions were checked in actual use: Euclidean volume doubling \(2^n\), Hessian model value \(|X|^2/r\), Myers bound \(\pi/\sqrt{k}\), unique minimizing segments in the simply connected Hadamard case, and the \(k=0\) hinge inequality \(c^2\le a^2+b^2-2ab\cos\alpha\).

## Assessment and limits

The main author finds the seven-interface knowledge route sufficient for its stated decisive-mechanism scope. This is an author assessment, pending the required independent nonauthor review of fixed bytes and any resulting repair. It is not a manuscript release, full textbook proof, broad-field completion, target-reader experiment or claim of originality. The old outputs, snapshots and accepted historical reviews have not been rewritten.
