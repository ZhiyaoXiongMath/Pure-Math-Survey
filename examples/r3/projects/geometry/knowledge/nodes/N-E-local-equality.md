---
{
  "schema_version": "2.0.0",
  "id": "N-E-local-equality",
  "kind": "example",
  "title": "Local or directional equality does not imply ambient rigidity",
  "facets": [
    "boundaries"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume",
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-triangle"
    },
    {
      "relation": "proof_input",
      "target": "N-R-volume-rigidity"
    }
  ]
}
---

# Local or directional equality does not imply ambient rigidity

## Explanation and evidence

On R^2×S^2(1), every triangle contained in R^2×{q} is Euclidean and attains all k=0 triangle equalities. The ambient sectional curvature is nevertheless 1 on sphere tangent planes. Likewise, along the R-factor of R×N, all normal fields J=tE attain Euclidean radial Jacobi equality, regardless of the curvature of N.

On a flat torus, an open ball of radius below the injectivity radius has the Euclidean metric and Euclidean volume, but the entire torus is compact. Thus local maximal-volume equality proves a local Riemannian isometry, not global Euclidean geometry. A global rigidity theorem must specify which directions, radii and points realize equality.
