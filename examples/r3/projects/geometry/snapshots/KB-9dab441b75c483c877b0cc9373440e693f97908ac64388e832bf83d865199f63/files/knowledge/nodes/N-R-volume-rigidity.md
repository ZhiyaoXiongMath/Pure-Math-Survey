---
{
  "schema_version": "2.0.0",
  "id": "N-R-volume-rigidity",
  "kind": "result",
  "title": "Maximal model volume gives a model polar metric",
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
      "target": "N-M-cut-integration"
    },
    {
      "relation": "proof_input",
      "target": "N-M-trace"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    }
  ]
}
---

# Maximal model volume gives a model polar metric

## Canonical statement

```latex
Let \((M^n,g)\) be a connected complete smooth Riemannian manifold, \(n\ge2\), with \(\operatorname{Ric}\ge(n-1)k g\). Let \(p\in M\), let \(D_k=\pi/\sqrt{k}\) for \(k>0\) and \(+\infty\) otherwise, and fix \(0<R<D_k\). If
\[
\operatorname{Vol}_g B(p,R)=\operatorname{Vol}_{M_k^n}B(\bar p,R),
\]
where \(M_k^n\) is the complete simply connected \(n\)-dimensional space form of sectional curvature \(k\), then the open Riemannian manifolds \(B(p,R)\) and \(B(\bar p,R)\), with their restricted metric tensors, are isometric by an isometry taking \(\bar p\) to \(p\).
```

## Explanation and evidence

If the ball volume equals the model volume, the density deficit (nonnegative on every ray) integrates to zero. Positivity of the model density and continuity exclude an early cut in any direction before R: otherwise an open set of directions and radial times loses positive volume. Every pre-cut density must equal its model. Equality in the traced Riccati chain yields S=c_k I, hence the polar angular metric solves g_t'=2c_k g_t and g_t=s_k(t)^2 g_{S^{n-1}} by the Euclidean initial asymptotic. Thus exp_p is a diffeomorphism from the open radius-R tangent ball with the model polar metric onto B(p,R).

Here “isometric” concerns the restricted Riemannian tensor (and the intrinsic length metric of each open ball). Distances measured by curves allowed to leave the ball are a different question. Small flat balls in a flat torus show that this conclusion does not imply global Euclidean geometry. The argument is a local derivation; Eschenburg Remark 5.7 is not copied because its displayed radii appear mismatched.
