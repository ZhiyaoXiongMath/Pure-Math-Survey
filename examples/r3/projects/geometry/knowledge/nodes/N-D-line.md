---
{
  "schema_version": "2.0.0",
  "id": "N-D-line",
  "kind": "definition",
  "title": "Lines, rays and the Busemann sign convention",
  "facets": [
    "foundations",
    "methods"
  ],
  "question_ids": [
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-Heintze-1984",
      "locator": "Section 2, p. 142",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-distance"
    }
  ]
}
---

# Lines, rays and the Busemann sign convention

## Canonical statement

```latex
In a complete Riemannian manifold a line is a unit speed geodesic \(\gamma:\mathbb R\to M\) satisfying \(d(\gamma(s),\gamma(t))=|s-t|\) for all \(s,t\in\mathbb R\). A ray satisfies the same condition with \(s,t\ge0\).
For a ray \(\gamma\) define
\[
b_\gamma(x)=\lim_{t\to\infty}\bigl(t-d(x,\gamma(t))\bigr).
\]
The limit exists and is finite: the terms are nondecreasing and bounded in absolute value by \(d(x,\gamma(0))\). The function \(b_\gamma\) is 1-Lipschitz.
```

## Explanation and evidence

With b=lim(t-d), b increases in the forward ray direction and is subharmonic under Ric>=0. Eschenburg 1994 uses the negative convention lim(d-t), while EH1984 uses the convention chosen here. Converting between them reverses the inequality signs; it does not change the splitting theorem.
