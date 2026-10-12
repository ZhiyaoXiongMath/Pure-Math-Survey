---
{
  "schema_version": "2.0.0",
  "id": "N-E-completeness",
  "kind": "example",
  "title": "Completeness and a uniform positive constant have different roles",
  "facets": [
    "boundaries"
  ],
  "question_ids": [
    "N-Q-global"
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
      "relation": "proof_input",
      "target": "N-R-myers"
    },
    {
      "relation": "proof_input",
      "target": "N-R-hadamard"
    }
  ]
}
---

# Completeness and a uniform positive constant have different roles

## Explanation and evidence

The open unit ball in Euclidean space is flat and simply connected, but geodesics can reach its missing boundary in finite time. exp_p is not defined on all tangent vectors, so the global Cartan–Hadamard conclusion fails without completeness.

An open round hemisphere has constant sectional curvature 1 and Ric=(n-1)g but is not compact. It tests the completeness requirement in Bonnet–Myers. This example does not violate the diameter bound itself; it violates the compactness conclusion.

Round spheres of radii R→infinity are complete and have Ric=(n-1)R^{-2}g>0 while diameter=pi R→infinity. Hence the statement “positive Ricci” across a varying family yields no uniform diameter bound without a common positive k. This calculation does not by itself decide whether an individual complete manifold with merely pointwise positive Ricci is compact.
