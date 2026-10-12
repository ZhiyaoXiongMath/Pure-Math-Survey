---
{
  "schema_version": "2.0.0",
  "id": "N-R-cheng",
  "kind": "result",
  "title": "Cheng maximal-diameter rigidity",
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
      "source_id": "S-Eschenburg-1994",
      "locator": "Theorem 12.1, p. 59; equality argument pp. 61\u201362",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "proof_input",
      "target": "N-R-myers"
    },
    {
      "relation": "explained_by",
      "target": "N-M-cheng"
    }
  ]
}
---

# Cheng maximal-diameter rigidity

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold without boundary, \(n\ge2\). If, for some \(k>0\),
\[
\operatorname{Ric}_g\ge(n-1)k g\qquad\text{and}\qquad
\operatorname{diam}_g(M)=\pi/\sqrt{k},
\]
then \((M,g)\) is isometric to the round sphere of radius \(1/\sqrt{k}\).
```

## Explanation and evidence

The statement is verified in Eschenburg's later exposition; Cheng's 1975 historical paper was located but its original full text was inaccessible. It is a rigidity theorem under Ricci, stronger in hypothesis range than the sectional-curvature maximal-diameter theorem. Its source provenance is explicit; this node does not claim to have verified Cheng's spectral comparison theorem.
