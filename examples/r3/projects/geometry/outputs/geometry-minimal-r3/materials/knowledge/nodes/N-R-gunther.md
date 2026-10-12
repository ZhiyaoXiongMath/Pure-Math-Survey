---
{
  "schema_version": "2.0.0",
  "id": "N-R-gunther",
  "kind": "result",
  "title": "G\u00fcnther-type lower volume comparison before the injectivity radius",
  "facets": [
    "results",
    "boundaries"
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
      "target": "N-R-hessian"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "compares_with",
      "target": "N-R-bishop-gromov"
    }
  ]
}
---

# Günther-type lower volume comparison before the injectivity radius

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold, \(n\ge2\), with sectional curvature \(\sec\le k\), and let \(p\in M\). Define \(D_k=\pi/\sqrt{k}\) if \(k>0\) and \(+\infty\) otherwise, and let \(V_k^n(r)\) be the ball volume in the complete simply connected \(n\)-dimensional space form of sectional curvature \(k\). Then
\[
\operatorname{Vol}_g B(p,r)\ge V_k^n(r)
\quad\text{for every }0<r<\min\{\operatorname{inj}_p(M),D_k\}.
\]
```

## Explanation and evidence

This node is a local deduction from the reviewed upper-sectional Hessian comparison, with the traditional theorem attribution used only for navigation. It does not claim to reproduce Günther's original formulation. On every radial ray below R, tr S>=(n-1)c_k and j/s_k^{n-1}>=1. Integrating j over the entire uncut polar ball proves the volume lower bound. All directions are available because R<inj_p(M). There is no replacement of a sectional upper bound by a Ricci upper bound.
