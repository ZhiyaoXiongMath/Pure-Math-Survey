---
{
  "schema_version": "2.0.0",
  "id": "N-H-compact",
  "kind": "mechanism",
  "title": "Extraction and the weaker Holder topology",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-holder"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Shapiro",
      "locator": "Theorem 1.1 and proof Steps I-III, pp.1-3",
      "role": "support"
    }
  ],
  "links": [
    {
      "target": "N-H-norm",
      "relation": "uses_definition"
    }
  ]
}
---

# Extraction and the weaker Holder topology

## Fast route
A common C^{2,alpha} bound controls every localized derivative through order two. The top derivatives have a common alpha-Holder modulus; the lower derivatives have a common Lipschitz modulus. Extract uniformly, identify derivatives, and interpolate. Each operation is needed: uniform convergence alone does not imply convergence of derivatives or their beta seminorms.

## Derivative extraction
All localized functions have support in finitely many fixed compact coordinate sets. For every derivative through order two choose a countable dense set in that compact set. Enumerate all resulting scalar evaluations. Successively extract convergent real subsequences and take the diagonal subsequence. For each epsilon, a finite net and the common modulus make it uniformly Cauchy: differences at arbitrary points are bounded by two modulus errors and one finite-net difference. This is the argument of Shapiro, Steps I-III, applied to finitely many derivative families.

For |nu|<=1 pass to the limit in
\[
D^\nu v_j(x+he_i)-D^\nu v_j(x)=\int_0^h D^{\nu+e_i}v_j(x+se_i)\,ds.
\]
Uniform convergence on each segment justifies passage under the integral. Therefore the uniform limits are compatible derivatives of a C^2 function. Coordinate transition rules pass by uniform convergence and fixed smooth coefficients; the partition of unity glues the localized limits to u. Their fixed support prevents a zero-extension boundary problem. Fixed-pair difference quotients show [D^nu v]_alpha<=liminf_j[D^nu v_j]_alpha. The finite sum norm has the same lower semicontinuity, so ||u||_{2,alpha}<=C.

## Interpolation
For any bounded alpha-Holder function w,
\[
|w(x)-w(y)|\leq\min\{2\|w\|_\infty,[w]_\alpha |x-y|^\alpha\}.
\]
For positive a,b and 0<theta<1, min(a,b)<=a^{1-theta}b^theta. Take theta=beta/alpha and divide by |x-y|^beta to obtain
\[
[w]_\beta\leq(2\|w\|_\infty)^{1-\beta/\alpha}[w]_\alpha^{\beta/\alpha}.
\]
The cases of zero seminorm or zero sup norm follow directly. Apply to differences of second derivatives: the sup norm tends to zero and the alpha seminorm is bounded by 2C. Together with lower derivative convergence this proves ||u_j-u||_{2,beta}->0. The exponent loss is decisive, as [the oscillation model](N-H-boundary.md#failure-models) shows.

## Local exhaustion
On an open Omega in R^d, estimates on every relatively compact open set give C^{2,beta}_{loc} extraction. Choose an exhaustion with compact closures K_l contained in the next interior. Apply the preceding cutoff argument successively on K_1,K_2,..., retaining nested subsequences. The diagonal subsequence converges on each fixed K_l; limits agree on overlaps by uniqueness of uniform limits. The bound may depend on l. There is no resulting global norm bound or boundary convergence. This explains the distinct roles of finite chart localization and a countable exhaustion diagonal.
