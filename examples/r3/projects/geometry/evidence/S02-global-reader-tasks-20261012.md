# Actual reconstruction tasks and author findings

Attempt s02-global-branches-a1; S02 epoch 2, generation 3. These tasks were performed during candidate drafting and rereading. The author already knows the proofs and has read the S01 audit; this is neither blinded assessment nor a target-student experiment. Every answer below is author/AI work.

## Fast reconstruction: Hadamard

Input reread: the candidate's “Route and hypotheses”, with the long calculations set aside. Task: identify the target, the role of each hypothesis, and what each intermediate object supplies.

Actual answer: completeness initially defines E=exp_p on all of T_pM. Nonpositive sectional curvature makes each squared normal Jacobi norm convex, preventing a second zero. The radial/angular differential decomposition then proves dexp invertible. The pullback metric h=E*g makes E a local isometry; its geodesics from zero are entire radial lines, so one-point Hopf–Rinow supplies metric completeness. Complete lifting gives an evenly covered normal ball. Simple connectivity only converts the connected cover to one sheet; repeating at every base point gives unique minimizing geodesics.

Finding: the fast paragraphs now explain why each intermediate object is chosen and point to a concrete subsection. The formerly absent factor-t differential conversion is in “The radial and angular parts of the differential”. Expert contribution: I supplied the reconstruction and authored the proof; no independent reader uptake is established. Full Hopf–Rinow and covering-space topology remain declared imports.

## Fast reconstruction: Toponogov

Input reread: “Route and fixed data” and “Three different comparison experiments”, with long proof sections set aside. Task: state which data stay fixed, why a local map is relevant, and how the proof escapes its local domain.

Actual answer: an SSS triangle fixes a,b,c and yields angle >= and matching chord >=. A same-angle model fixes a,b,alpha and yields endpoint distance <=; it is a different experiment. F=exp_p composed with I composed with inverse model exponential preserves radial speed and contracts angular speed only inside a common normal domain. A contained short model chord gives local SAS, and monotonic model cosine law gives local SSS angle comparison. The global step is the imported 4/5 shrinking proposition; its shared endpoint controls the change of vertex. A Cauchy limit and uniformly valid local comparisons near it prohibit a violating sequence. Global angle comparisons for all necessary auxiliary hinges then give chords by the imported conversion lemma.

Finding: the fast route now identifies both the domain obstacle and the reason uniformity in the moving vertex is required. Expert contribution: the reconstruction is by the candidate author. The technical gluing and chord-conversion proofs remain source imports; the candidate does not promise to teach those proofs from scratch.

## Slow computation 1: dexp, including the radial direction

Task: start with a unit v, w perpendicular to v, and the radial variation gamma_v(t)=exp_p(tv), and decide whether dexp at tv can have a kernel.

Actual calculation:
- Vary the unit direction through v(s), v'(0)=w. Differentiating exp_p(t v(s)) gives J_w(t)=dexp_(tv)(t w).
- Vary the radius through t+s. This gives dexp_(tv)(v)=gamma_v'(t).
- Thus dexp_(tv)(a v+w)=a gamma_v'(t)+J_w(t)/t.
- Gauss lemma eliminates the mixed term, so its squared norm is a^2+|J_w(t)|^2/t^2.
- With sec<=0, f=|J_w|^2 is convex, f(0)=0, and f(t)>0 near zero for w nonzero. A later zero would force f<=0 between its zeros, contradiction. Therefore the displayed squared norm vanishes only when a=w=0. At zero dexp is the identity.

This computation now appears in the candidate and follows the shared Jacobi interface exactly. Expert-supplied foundational input: Gauss lemma and the fact that radial variations satisfy Jacobi's equation. These are declared and linked; the factor t and the radial kernel check are worked out locally.

## Slow computation 2: contained model chord and moving vertex

Task: verify the actual use of a local differential inequality.

With a,b<R/2 and a minimizing model chord of length L<=a+b, its point at arclength s satisfies
d(o,sigma(s))<=min(a+s,b+L-s)<R.
Thus sigma stays in F's domain, and
d_M(x,y)<=L_M(F sigma)<=L_k(sigma)=h_k(a,b,alpha).
The monotonicity of h_k gives bar_alpha<=alpha.

For the shrinking hinges, put q=4/5. From P_j<q^j P_0 and a shared endpoint,
d(p_j,p_(j-1))<=(1+q)q^(j-1)P_0.
Hence for m>n,
d(p_m,p_n)<=((1+q)/(1-q))q^n P_0=9q^n P_0.
Completeness gives p_j->p, while both endpoints are within P_j of p_j. If the normal radius R works for every vertex in V, choose delta with B(p,delta) subset V and 2delta<R/2. Eventually each violating hinge meets the local comparison hypotheses, contradiction.

Finding: the numbers 4/5, 9/5 and 9 have distinct roles and are retained. Expert contribution: this is the author's explicit calculation, not a numerical experiment. The input producing H_j is exactly the imported Proposition 5.14.

## Slow computation 3: auxiliary perimeter for chord conversion

Task: check that a global strict-perimeter theorem can actually be called on the connecting hinges required by Lang Lemma 5.9.

For u_1,u_2 on px at radii r_1<=r_2 and v on py at radius s,
d(u_1,u_2)=r_2-r_1,
d(u_1,v)<=r_1+s,
d(u_2,v)<=a-r_2+c+b-s.
Adding gives P(u_1,u_2,v)<=P(p,x,y)<2D_k. The same argument covers the swapped sides, and triples on one side have perimeter <=2max(a,b)<=P. Thus global angle comparison applies to all the auxiliary connecting hinges.

Finding: the candidate does not infer chord comparison from the angle inequality of a single hinge. Expert contribution: this elementary bound was supplied by the author and is now present in the node.

## Conditions: first failure, not an invented stronger theorem

1. Remove Hadamard simple connectivity. The first failed implication is connected covering -> one sheet. The flat cylinder still has sec=0, no conjugate points, a complete pullback metric and a many-sheeted exponential cover.
2. Remove Hadamard completeness. An open Euclidean ball can have exp_p undefined on some tangent vectors. The route already fails before defining h on all T_pM, rather than only at its last topological step.
3. Replace Hadamard sec<=0 by Ric<=0. The convexity estimate uses a particular radial sectional term <R(J,gamma')gamma',J>; controlling its trace does not control its sign. This identifies a failed inference, not a blanket claim about every theorem under a Ricci upper bound.
4. Let a Toponogov model curve leave the common normal domain. The required derivative/length inequality no longer applies along the whole curve. Local Rauch does not supply a global SAS proof.
5. Omit moving-center uniformity. A normal chart centered at the limit alone does not verify the hypotheses for F based at each p_j. A fixed R valid throughout V is needed before choosing delta.
6. Remove Toponogov completeness. The constructed vertices remain Cauchy, but their limit is not guaranteed to lie in M, so no local comparison neighborhood at the limit is available.
7. Replace chosen minimizing sides by arbitrary geodesic arcs. Side lengths need not equal endpoint distances; the perimeter estimates and the exact gluing hypotheses then fail. Lang Remark 5.16 treats a separate controlled extension, not invoked here.
8. Set the original perimeter equal to 2D_k. The strict imported interface cannot be called, and degenerate spherical configurations may occur. This is outside the principal statement; it is not asserted that every endpoint comparison is false.
9. Keep only the original hinge's angle comparison when proving chords. Lemma 5.9 additionally consumes angle inequalities for the connecting hinges and balanced sides. The auxiliary-perimeter computation is what lets the global result supply these inputs.
10. Replace Toponogov sectional lower curvature by a Ricci lower bound. The directional Jacobi/Rauch estimate used to bound every angular component of dF is no longer supplied.

## Unperformed work and integration dependencies

No independent or nonauthor review is claimed. No real student task, manuscript rendering, freeze, source redistribution, software integration, or final mathematical acceptance was performed. Planned shared headings and overview backlinks must be checked after the main integrates its files. The detailed gluing/conversion lemmas and the listed foundational theorems remain intentionally imported.
