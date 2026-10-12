# S02 source rereading for the radial comparison route

Date: 2026-10-12. Mode: author rereading by the S02 main agent, with explicitly identified local calculations. This supplements the previous versioned source notes; it does not rewrite their reading history or claim independent peer review.

## Controlling material and actual scope

- Eschenburg, *Comparison Theorems in Riemannian Geometry*, September 1994, Toronto-hosted 77-page PDF. SHA-256: bc1478206c223194f3ee19210062b856a38639c55e34aa68136d1c4e970a267e. The current main agent read printed pp. 3–4, 6–8 and 12–20 from the cached original PDF. Printed p. 20 was additionally rasterized and visually inspected, including formulas (5.11)–(5.15). The [registered source](../../knowledge/sources/S-Eschenburg-1994.json) and [earlier reading note](S-Eschenburg-1994.md) retain the wider historical read scope.
- Bishop, *Riemannian Geometry*, arXiv:1303.5390v2, 27 July 2013, 64-page PDF. SHA-256: 661745181375a3fe6302d2e510ca8e628eed4ae24b3fa866745a43b292b2b1a8. The current main agent read printed pp. 33–34, 45–46 and 53–56 from the cached original PDF. This covers Gauss lemma, the Jacobi equation, fixed-end second variation, the end of the completeness argument, cut points, exponential covering and Myers. The [registered source](../../knowledge/sources/S-Bishop-2013v2.json) and [earlier reading note](S-Bishop-2013v2.md) record additional foundational pages read during the earlier population.

The primary-source URLs are [Eschenburg's notes](https://www.math.toronto.edu/vtk/eschenburg-comparison.pdf) and [Bishop's versioned arXiv record](https://arxiv.org/abs/1303.5390v2). The web records were opened during this revision; the actual mathematical page reading used the identified PDF bytes.

Raw PDFs remain in a private reading cache. They are not copied into the representative review packet, public examples, the authoritative knowledge files or a new snapshot. Extracted reading text and page images are working evidence, not redistributed source editions.

## Translation and precise imports

Eschenburg writes the shape endomorphism as \(A\); this knowledge base writes it as \(S\) and reserves \(A\) for the radial Jacobi tensor. The curvature convention agrees with Eschenburg's \(R(X,Y)Z=\nabla_X\nabla_YZ-\nabla_Y\nabla_XZ-\nabla_{[X,Y]}Z\). Bishop uses different tensor slots; the translation is fixed by geometric sectional curvature and \(J''+R(J,\dot\gamma)\dot\gamma=0\).

The algebraic curvature identities, Gauss lemma, completeness/minimization theorem, cut-domain diffeomorphism and null cut locus are imported with their actual hypotheses. The singular matrix comparison in Eschenburg Remark 3.2 remains an explicit import; writing out the regular congruence calculation does not purport to prove the singular extension. The scalar singular comparison is instead proved directly by an integrating factor.

In Eschenburg's regular comparison calculation, the fundamental matrix solving \(G'=XG\) need not be symmetric even if \(X(t)\) is symmetric. The revision uses only invertibility and the valid congruence \(U=GZG^T\). Eschenburg's known equality-radius mismatch in Remark 5.7 and the triangle sign issue are not used to promote new equality or triangle assertions.

Bishop's fixed-end energy convention has an overall factor \(2\) relative to the half-energy convention used in N-D-index. Only this normalization changes. The new Myers calculation uses a hypothetical length strictly greater than the diameter bound and a strictly negative index sum, avoiding any need to assert positivity exactly at a conjugate endpoint. The text extraction of Bishop p. 55 omits a factor \(2\) in the curvature term of the convexity display; extraction alone is not evidence of a printed defect. The derivative in the revised mechanism is computed directly and does not depend on that extraction.

## Calculations performed in this revision

The following are local derivations checked by the author, not quotations of a theorem containing all the desired steps:

1. Differentiate \(F(s,t)=\exp_p(tv(s))\); obtain the normal Jacobi initial data and \(d\exp_{tv}(tw)=A_v(t)w\). Differentiate the Jacobi equation at zero to get the cubic Taylor term.
2. Use the radial/angular Gram matrix \(\operatorname{diag}(1,A^TA)\), its square-root determinant and the preconjugate sign to identify the geometric density \(j=\det A\). Solve the constant-curvature ODE and recover its polar metric and density.
3. Recover the initial vector \(A^{-1}X\) from a current normal vector \(X\), apply torsion freeness, and obtain the Hessian bilinear form, its zero radial part and \(\Delta r=\operatorname{tr}S\).
4. Differentiate the Wronskian and Riccati equation. Take the trace and the eigenvalue square inequality. Use \(\mu(t)\sim Ct^2\), \(u(t)=O(t)\), to pass the scalar comparison from \(\varepsilon>0\) to zero.
5. Identify the inverse image of the metric ball inside the uncut domain, extend its density by zero, justify angular dominated convergence, and prove the weighted-average derivative with local absolute continuity. The positive-curvature endpoint uses the independent Myers argument and the null terminal distance sphere.
6. Apply the ratio estimate to doubling and relative volume; identify the lost estimate under Ricci upper curvature, untruncated rays and a reversed raywise inequality.
7. For endpoint Hessian comparison, integrate the Jacobi cross term against the endpoint-zero difference field and then compute \(\int(f'^2-kf^2)=[ff']\). For Myers, compute the sine-field curvature sum and both squared-trigonometric integrals, and apply the completeness/covering steps explicitly.

These checks do not establish full foundational proofs, general equality classifications, endpoint triangle conventions, or any of the unassessed neighboring branches. The forthcoming independent reading is a separate stage.
