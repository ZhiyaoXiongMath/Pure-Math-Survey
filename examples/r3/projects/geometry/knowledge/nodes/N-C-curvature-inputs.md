---
{
  "schema_version": "2.0.0",
  "id": "N-C-curvature-inputs",
  "kind": "relation",
  "title": "Sectional lower bounds imply Ricci lower bounds, but the converse fails",
  "facets": [
    "foundations",
    "results",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "proof_input",
      "target": "N-E-product"
    },
    {
      "relation": "compares_with",
      "target": "N-R-hessian"
    },
    {
      "relation": "compares_with",
      "target": "N-R-laplacian"
    }
  ]
}
---

# Sectional lower bounds imply Ricci lower bounds, but the converse fails

## Canonical statement

```latex
For every smooth Riemannian n-manifold, \(n\ge2\), and every \(k\in\mathbb R\),
\[
\sec\ge k\quad\Longrightarrow\quad\operatorname{Ric}\ge(n-1)k g.
\]
The converse is false in general: on \(S^2(1)\times S^2(1)\), with \(n=4\), \(\operatorname{Ric}=g=3(1/3)g\), but a plane spanned by vectors in distinct factors has sectional curvature \(0<1/3\).
```

## Explanation and evidence

Complete the unit vector v to an orthonormal basis. The formula Ric(v,v)=sum_{i=1}^{n-1} K(v,e_i) proves the forward implication with exactly n-1 summands. The product S^2×S^2 has Ric=g but a zero mixed plane, proving failure of the normalized converse at k=1/3. This is an implication about hypotheses, not an equivalence between their comparison consequences. The explicit Hessian and hinge failures are in [[N-E-product]].
