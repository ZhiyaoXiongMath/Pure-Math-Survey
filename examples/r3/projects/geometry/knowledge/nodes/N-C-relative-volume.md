---
{
  "schema_version": "2.0.0",
  "id": "N-C-relative-volume",
  "kind": "relation",
  "title": "Relative lower volume and doubling are genuine consequences",
  "facets": [
    "results",
    "methods"
  ],
  "question_ids": [
    "N-Q-volume"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-R-bishop-gromov"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "compares_with",
      "target": "N-E-collapse"
    }
  ]
}
---

# Relative lower volume and doubling are genuine consequences

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold with \(\operatorname{Ric}\ge(n-1)k g\), and let \(V_k^n\) be the ball-volume function of the complete simply connected \(n\)-dimensional space form of curvature \(k\). For every \(p\in M\) and \(0<r<R\),
\[
\operatorname{Vol}B(p,r)\ge\frac{V_k^n(r)}{V_k^n(R)}\operatorname{Vol}B(p,R).
\]
In particular, if \(\operatorname{Ric}\ge0\), then for every \(p\) and \(r>0\),
\[
\operatorname{Vol}B(p,2r)\le2^n\operatorname{Vol}B(p,r).
\]
```

## Explanation and evidence

Write the Bishop–Gromov inequality as V(R)/V_k(R)<=V(r)/V_k(r) and multiply by the positive denominators. This yields the lower-volume fraction. At k=0 the model volume scales as r^n, giving the factor 2^n at each center. No cancellation produces a positive absolute volume lower bound independent of V(R); [[N-E-collapse]] makes that distinction concrete.
