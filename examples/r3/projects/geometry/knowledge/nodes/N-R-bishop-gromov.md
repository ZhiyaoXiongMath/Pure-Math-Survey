---
{
  "schema_version": "2.0.0",
  "id": "N-R-bishop-gromov",
  "kind": "result",
  "title": "Bishop\u2013Gromov relative volume comparison",
  "facets": [
    "results",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-volume"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Theorem 5.5 and Corollary 5.6, p. 19; proof p. 20",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "explained_by",
      "target": "N-M-cut-integration"
    }
  ]
}
---

# Bishop–Gromov relative volume comparison

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold, \(n\ge2\), with \(\operatorname{Ric}\ge(n-1)k g\) for a fixed \(k\in\mathbb R\). Let \(V_k^n(r)\) denote the volume of a radius-\(r\) ball in the complete simply connected space form of dimension \(n\) and sectional curvature \(k\); for \(k>0\) it is constant for \(r\ge\pi/\sqrt{k}\).
For every \(p\in M\) and all \(0<r<R<\infty\),
\[
\frac{\operatorname{Vol}_g B(p,R)}{V_k^n(R)}
\le \frac{\operatorname{Vol}_g B(p,r)}{V_k^n(r)}\le1,
\qquad
\lim_{r\downarrow0}\frac{\operatorname{Vol}_g B(p,r)}{V_k^n(r)}=1.
\]
Equivalently,
\[
\frac{\operatorname{Vol}_g B(p,R)}{\operatorname{Vol}_g B(p,r)}\le\frac{V_k^n(R)}{V_k^n(r)}.
\]
```

## Explanation and evidence

The estimate compares concentric balls at the same base point. It implies an absolute upper bound but only a relative lower bound once the volume of a larger ball is specified. The full canonical theorem does not assert an unverified general equality case; the carefully stated maximal-volume equality is a separate local deduction [[N-R-volume-rigidity]].

## Reading and first use

The [six-step route](../overview.md#ricci-lower-bounds-to-ball-volume) reconstructs why radial curvature information controls a metric ball. The [actual volume substitution](N-M-cut-integration.md#applying-the-average-to-geometric-volume) and [positive-curvature endpoint](N-M-cut-integration.md#the-positive-curvature-endpoint) establish the full range of radii in the statement. With \(k=0\) and \(R=2r\), it yields the doubling bound \(2^n\). The [relative-volume deduction](N-C-relative-volume.md) and [collapsing examples](N-E-collapse.md) explain why this is not an absolute lower volume bound.
