---
{
  "schema_version": "2.0.0",
  "id": "N-R-myers",
  "kind": "result",
  "title": "Bonnet\u2013Myers diameter and fundamental-group theorem",
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
      "locator": "Theorem 9.3, pp. 55\u201356",
      "role": "support"
    },
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Corollary 12.3, p. 59",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "explained_by",
      "target": "N-M-myers"
    }
  ]
}
---

# Bonnet–Myers diameter and fundamental-group theorem

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold without boundary, \(n\ge2\). Suppose that there is a constant \(k>0\) such that
\[
\operatorname{Ric}_x(v,v)\ge(n-1)k|v|_g^2\quad\text{for every }x\in M\text{ and }v\in T_xM.
\]
Then \(M\) is compact,
\[
\operatorname{diam}_g(M)\le\pi/\sqrt{k},
\]
and \(\pi_1(M)\) is finite.
```

## Explanation and evidence

The same positive constant k must work at every point and in every tangent direction. Completeness enters both minimization and compactness. Equality of diameter is stronger than the inequality and is recorded separately in [[N-R-cheng]].

## Reading and first use

The [fast Myers route](../overview.md#myers-from-endpoint-fields-to-global-finiteness) summarizes the contradiction. The [sine-field computation](N-M-myers.md#the-sine-field-calculation) shows exactly how the Ricci trace enters, and the [global argument](N-M-myers.md#from-length-to-compactness-and-finite-fundamental-group) proves the topological conclusion. In particular, for \(k=1\), every pair has distance at most \(\pi\); this uniform bound closes the spherical endpoint in Bishop--Gromov independently of that theorem.
