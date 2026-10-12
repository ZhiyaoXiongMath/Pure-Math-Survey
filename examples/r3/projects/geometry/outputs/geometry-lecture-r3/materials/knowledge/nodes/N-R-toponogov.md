---
{
  "schema_version": "2.0.0",
  "id": "N-R-toponogov",
  "kind": "result",
  "title": "Toponogov angle, hinge and chord comparisons",
  "facets": [
    "results",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Toponogov-1959",
      "locator": "Section 9, Theorem 6, p. 127",
      "role": "support"
    },
    {
      "source_id": "S-Lang-2026",
      "locator": "Definition 5.7, p. 66; Theorem 5.15, p. 70",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-triangle"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "explained_by",
      "target": "N-M-toponogov"
    }
  ]
}
---

# Toponogov angle, hinge and chord comparisons

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold without boundary, \(n\ge2\), with \(\sec_M\ge k\). Put \(D_k=\pi/\sqrt{k}\) for \(k>0\) and \(D_k=+\infty\) otherwise. Choose distinct points \(p,x,y\) and minimizing segments \(px,py,xy\). Suppose their side lengths satisfy strict triangle inequalities and
\[
d(p,x)+d(p,y)+d(x,y)<2D_k.
\]
Let \((\bar p,\bar x,\bar y)\) be the triangle with the same three side lengths in the complete simply connected surface \(M_k^2\) of sectional curvature \(k\). Then each angle of the chosen triangle in \(M\) is at least the corresponding model angle.
If \((\hat p,\hat x,\hat y)\) is instead a model hinge with
\[
d(\hat p,\hat x)=d(p,x),\quad d(\hat p,\hat y)=d(p,y),\quad
\angle\hat x\hat p\hat y=\angle xpy,
\]
then \(d_M(x,y)\le d_{M_k^2}(\hat x,\hat y)\).
Moreover, for all \(u\in px\), \(v\in py\) and matching points \(\bar u\in\bar p\bar x\), \(\bar v\in\bar p\bar y\) such that
\(d(p,u)=d(\bar p,\bar u)\) and \(d(p,v)=d(\bar p,\bar v)\),
\[
d_M(u,v)\ge d_{M_k^2}(\bar u,\bar v).
\]
```

## Explanation and evidence

The nondegenerate strict-perimeter version gives a clean reusable statement. In particular every side is less than D_k, so the spherical model construction is unambiguous up to isometry. The endpoint case with perimeter 2D_k requires a separate convention and is not silently included. All three inequalities concern chosen minimizing sides; no injectivity-radius assumption is needed in M.

The original angle theorem is Toponogov 1959, §9 Theorem 6, p.127. The full modern angle/hinge/chord formulation is Lang 2026, Definition 5.7 and Theorem 5.15. Eschenburg (6.10) is not used as a controlling statement because its printed sign conflicts with its proof and the independent formulations.

## Reading and first use

The [fast triangle route](../overview.md#toponogov-from-local-lengths-to-global-triangles) identifies the three experiments. The [local-to-global mechanism](N-M-toponogov.md) includes the exponential-map length calculation and the shrinking contradiction. For \(k=0\), a hinge with two sides \(a,b\) and included angle \(\theta\) satisfies \(d(x,y)^2\le a^2+b^2-2ab\cos\theta\), under the canonical nondegenerate minimizing-triangle hypotheses. This is the SAS experiment; it does not reverse the SSS angle or chord inequalities.
