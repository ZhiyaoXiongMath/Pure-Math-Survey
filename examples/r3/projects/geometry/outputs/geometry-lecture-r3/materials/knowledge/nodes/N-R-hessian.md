---
{
  "schema_version": "2.0.0",
  "id": "N-R-hessian",
  "kind": "result",
  "title": "Hessian comparison on the regular distance domain",
  "facets": [
    "results",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-local"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Theorem 3.1 and Remark 3.2, pp. 12\u201313; Section 6, equations (6.2)\u2013(6.6), p. 21",
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
      "target": "N-D-model"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "explained_by",
      "target": "N-M-riccati"
    },
    {
      "relation": "proof_input",
      "target": "N-M-riccati"
    }
  ]
}
---

# Hessian comparison on the regular distance domain

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold, \(n\ge2\), \(p\in M\), and \(x\notin\{p\}\cup\operatorname{Cut}(p)\). Set \(r=d_g(p,\cdot)\) and \(\ell=r(x)>0\). Fix \(k\in\mathbb R\) and assume \(\ell<D_k\), where \(D_k=\pi/\sqrt{k}\) for \(k>0\) and \(+\infty\) otherwise. Let \(s\) solve \(s''+ks=0,s(0)=0,s'(0)=1\).
If the sectional curvatures of every plane containing the tangent to the unit speed minimizing segment from \(p\) to \(x\) are at least \(k\), then, for all \(X\in T_xM\),
\[
\nabla^2r_x(X,X)\le \frac{s'(\ell)}{s(\ell)}\bigl(|X|^2-dr_x(X)^2\bigr).
\]
If those radial sectional curvatures are instead at most \(k\), the inequality is reversed.
```

## Explanation and evidence

Only radial sectional curvatures along the unique minimizing segment to x are needed. The statement is a quadratic-form estimate and retains the zero radial direction. It is not a smooth tensor inequality across Cut(p). The curvature-lower-bound inequality is opposite to the growth intuition for curvature: larger curvature means smaller radial sphere shape operator.

## Reading and first use

The [fast sectional route](../overview.md#sectional-bounds-to-jacobi-length-and-hessian) leads to the operator comparison. The [current-vector calculation](N-M-geometric-inputs.md#current-vectors-and-the-distance-hessian) explains why its result is precisely a distance Hessian, including the zero radial direction. The [endpoint index-form calculation](N-D-index.md#an-endpoint-field-calculation) is an alternative proof of the lower-sectional half. For \(k=0\) and \(X\perp\nabla r\), this gives \(\nabla^2r(X,X)\le |X|^2/r\). Replacing sectional by Ricci lower curvature does not justify the operator comparison.
