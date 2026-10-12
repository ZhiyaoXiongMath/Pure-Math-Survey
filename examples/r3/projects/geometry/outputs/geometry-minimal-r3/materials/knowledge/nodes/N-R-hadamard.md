---
{
  "schema_version": "2.0.0",
  "id": "N-R-hadamard",
  "kind": "result",
  "title": "Cartan\u2013Hadamard theorem",
  "facets": [
    "results",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Theorems 9.1\u20139.2, pp. 54\u201355",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-distance"
    },
    {
      "relation": "explained_by",
      "target": "N-M-hadamard"
    }
  ]
}
---

# Cartan–Hadamard theorem

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold with \(\sec\le0\). For every \(p\in M\), the exponential map
\[
\exp_p:T_pM\longrightarrow M
\]
is a covering map. If \(M\) is simply connected, \(\exp_p\) is a global diffeomorphism for every \(p\), \(M\) is diffeomorphic to \(\mathbb R^n\), and every pair of points is joined by a unique minimizing geodesic.
```

## Explanation and evidence

Here “Hadamard manifold” is reserved for the complete simply connected nonpositively curved case; Bishop uses a broader naming convention, so the assumptions are repeated explicitly. Nonpositive Ricci is not a substitute for nonpositive sectional curvature.

## Reading and first use

The [fast Hadamard route](../overview.md#hadamard-from-local-invertibility-to-a-global-cover) distinguishes local nonsingularity, a global covering and one-sheetedness. The [mechanism](N-M-hadamard.md) checks each step; [the covering interface](N-M-geometric-inputs.md#complete-local-isometries-and-covering) explains why completeness is needed. The flat cylinder satisfies the covering conclusion but has multiple lifts of a point, so simple connectivity cannot be deleted from the diffeomorphism conclusion.
