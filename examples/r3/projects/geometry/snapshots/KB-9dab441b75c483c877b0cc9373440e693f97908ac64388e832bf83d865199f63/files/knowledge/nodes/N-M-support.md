---
{
  "schema_version": "2.0.0",
  "id": "N-M-support",
  "kind": "mechanism",
  "title": "Move the distance center to construct upper supports",
  "facets": [
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Section 12, pp. 60\u201362",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-R-laplacian"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-support"
    }
  ]
}
---

# Move the distance center to construct upper supports

## Explanation and evidence

Assume the connected complete manifold satisfies Ric>=(n-1)k g as in N-R-laplacian. Fix x distinct from p, with 0<d(p,x)<D_k, and choose a minimizing segment gamma from p to x. For sufficiently small epsilon>0 move the center to p_epsilon=gamma(epsilon). The shifted function
\[
r_\epsilon(y)=\epsilon+d(p_\epsilon,y)
\]
is an upper support for d(p,y), with equality at x by minimization and the triangle inequality. The standard cut-locus lemma ensures x is a regular point of the distance from p_epsilon. At x the smooth comparison yields
\[
\Delta r_\epsilon(x)\le(n-1)c_k(d(p,x)-\epsilon)\longrightarrow(n-1)c_k(d(p,x)).
\]
Thus the upper-support comparison extends to cut points in this radial range. The shift lemma is an imported geometric input; it is not permissible to differentiate the original distance at a cut point. Apply signs consistently when passing to negative distance or Busemann functions. The strong maximum principle for these support inequalities is imported from Eschenburg Theorem 12.6 / EH1984 §6.
