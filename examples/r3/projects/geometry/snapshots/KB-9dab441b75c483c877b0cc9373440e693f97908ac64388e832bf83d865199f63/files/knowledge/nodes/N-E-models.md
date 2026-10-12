---
{
  "schema_version": "2.0.0",
  "id": "N-E-models",
  "kind": "example",
  "title": "Exact calculations in constant curvature",
  "facets": [
    "foundations",
    "results"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
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

# Exact calculations in constant curvature

## Explanation and evidence

For the curvature-k space form, choose a parallel unit normal vector E. The Jacobi equation reduces to s_k''+k s_k=0, so J=s_k E. Therefore
\[
|J|=s_k,\quad S=c_k I,\quad \nabla^2r=c_k(g-dr\otimes dr),\quad
\Delta r=(n-1)c_k,\quad j=s_k^{n-1}.
\]
For Euclidean space c_0=1/r; for a unit sphere c_1=cot r before pi; for hyperbolic space c_{-1}=coth r. These formulas check inequality signs and all factors n-1. On the unit sphere s_1 vanishes at pi: the pole of c_1 is geometric, not removable. This is an explicit ODE calculation using [[N-D-model]], not a numerical test.
