---
{
  "schema_version": "2.0.0",
  "id": "N-E-global-reverse",
  "kind": "example",
  "title": "A flat torus obstructs an unrestricted reverse hinge comparison",
  "facets": [
    "boundaries"
  ],
  "question_ids": [
    "N-Q-triangles",
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-triangle"
    },
    {
      "relation": "proof_input",
      "target": "N-R-hadamard"
    }
  ]
}
---

# A flat torus obstructs an unrestricted reverse hinge comparison

## Explanation and evidence

In R^2/Z^2 take p=[(0,0)], x=[(0.4,0.1)] and y=[(-0.4,0.1)]. The indicated radial segments are minimizing since each coordinate of their lift has absolute value below 1/2. Their length is sqrt(0.17); their included angle determines a Euclidean opposite side of length 0.8. In the torus,
\[
d(x,y)=\min_{m\in\mathbb Z^2}|(0.8,0)+m|=0.2.
\]
Therefore sec<=0 alone does not imply the global reverse of the lower-curvature hinge theorem. Simple connectivity removes this quotient mechanism in Cartan–Hadamard; local normal-neighborhood comparisons remain valid.
