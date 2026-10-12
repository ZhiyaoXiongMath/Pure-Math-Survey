---
{
  "schema_version": "2.0.0",
  "id": "N-D-triangle",
  "kind": "definition",
  "title": "Comparison triangles and same-angle hinges",
  "facets": [
    "foundations",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Lang-2026",
      "locator": "Definitions 5.4\u20135.7 and Lemma 5.8, pp. 65\u201366",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    }
  ]
}
---

# Comparison triangles and same-angle hinges

## Canonical statement

```latex
Let \(p,x,y\) be points in a Riemannian manifold joined by chosen minimizing segments, and set \(a=d(p,x), b=d(p,y), c=d(x,y)\). Suppose the strict triangle inequalities hold and \(a+b+c<2D_k\), where \(D_k=\pi/\sqrt{k}\) for \(k>0\) and \(+\infty\) otherwise.
An SSS comparison triangle is a triangle \((\bar p,\bar x,\bar y)\) in the complete simply connected constant-curvature-\(k\) surface \(M_k^2\) with side lengths \(a,b,c\). Its angles are determined by those lengths.
A same-angle comparison hinge consists of two minimizing segments in \(M_k^2\) of lengths \(a,b\) whose included angle equals the angle between the chosen segments \(px,py\). Its opposite side length is not prescribed to equal \(c\).
```

## Explanation and evidence

These are two different experiments. In SSS comparison the three distances are fixed and the angle varies. In hinge comparison the two radial distances and the angle are fixed and the opposite distance varies. A geodesic side in this project means a chosen distance-minimizing segment unless explicitly said otherwise. Degenerate comparison triangles are interpreted by a limit; the main result below uses strict triangle inequalities to avoid that convention.

### Auxiliary hinges in the proof

For the imported hinge lemmas, \(H_p(x,y)\) consists of two chosen nonzero minimizing sides, so \(p\notin\{x,y\}\), while \(x=y\) is allowed. Under perimeter \(<2D_k\), degenerate SSS triples use the continuous comparison angle: \(0\) if \(c=|a-b|\), and \(\pi\) if \(c=a+b<D_k\). The principal Toponogov statement retains strict triangle inequalities.

This larger auxiliary class is needed when the [shrinking proposition](N-M-toponogov.md#the-exact-gluing-and-globalization-inputs) or the [chord conversion](N-M-toponogov.md#global-hinge-and-chord-comparison) constructs additional hinges. Their hypotheses are checked in the mechanism, rather than inferred from the original triangle alone.

Return to the [triangle route](../overview.md#toponogov-from-local-lengths-to-global-triangles).
