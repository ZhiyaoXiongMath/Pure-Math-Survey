---
{
  "schema_version": "2.0.0",
  "id": "N-R-splitting",
  "kind": "result",
  "title": "Cheeger\u2013Gromoll splitting theorem",
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
      "source_id": "S-Eschenburg-Heintze-1984",
      "locator": "Splitting Theorem, p. 141; product construction, p. 148",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-line"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "explained_by",
      "target": "N-M-splitting"
    }
  ]
}
---

# Cheeger–Gromoll splitting theorem

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold without boundary, \(n\ge2\), with \(\operatorname{Ric}_g\ge0\). Suppose there is a unit speed geodesic \(\gamma:\mathbb R\to M\) such that
\[
d_g(\gamma(s),\gamma(t))=|s-t|\quad\text{for every }s,t\in\mathbb R.
\]
Then there is a connected complete Riemannian manifold \((N^{n-1},h)\) with \(\operatorname{Ric}_h\ge0\) and an isometry
\[
(M,g)\cong(N\times\mathbb R,h+dt^2).
\]
```

## Explanation and evidence

EH1984 is an actually read original alternative proof, not the 1971 discovery paper. A line minimizes every finite subsegment. Geodesic completeness alone gives complete geodesics but does not make them lines. The factor inherits completeness and Ric>=0 from the product isometry; these facts unpack the source conclusion.
