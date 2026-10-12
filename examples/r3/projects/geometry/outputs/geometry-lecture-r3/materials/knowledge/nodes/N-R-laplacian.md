---
{
  "schema_version": "2.0.0",
  "id": "N-R-laplacian",
  "kind": "result",
  "title": "Laplacian comparison under a Ricci lower bound",
  "facets": [
    "results",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Theorem 4.1 and Remark 4.2, pp. 15\u201316; Section 12, p. 61",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-distance"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "explained_by",
      "target": "N-M-trace"
    }
  ]
}
---

# Laplacian comparison under a Ricci lower bound

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold, \(n\ge2\), with \(\operatorname{Ric}\ge(n-1)k g\), \(k\in\mathbb R\). For every \(p\in M\), set \(r(x)=d_g(p,x)\). Let \(s\) be the solution of \(s''+ks=0,s(0)=0,s'(0)=1\), and let \(D_k=\pi/\sqrt{k}\) for \(k>0\), \(+\infty\) otherwise. With \(\Delta=\operatorname{div}\nabla\),
\[
\Delta r(x)\le(n-1)\frac{s'(r(x))}{s(r(x))}
\]
for every \(x\notin\{p\}\cup\operatorname{Cut}(p)\) with \(0<r(x)<D_k\).
```

## Explanation and evidence

The canonical statement is the classical smooth-domain interface. A support-function extension is recorded separately in [[N-M-support]] for rigidity arguments; no unspecified distributional sign convention is imported here. The weaker Ricci hypothesis cannot generally give the full Hessian comparison.

## Reading and first use

The [fast Ricci route](../overview.md#ricci-lower-bounds-to-ball-volume) separates the trace inequality from later integration. The [singular integrating factor](N-M-trace.md#singular-scalar-comparison-by-an-integrating-factor) proves the displayed bound without treating infinity as ordinary initial data. For \(\operatorname{Ric}\ge0\), it gives \(\Delta r\le(n-1)/r\) on the regular domain. A value at a cut point requires the separately stated support-function interpretation; it is not supplied by this smooth formula.
