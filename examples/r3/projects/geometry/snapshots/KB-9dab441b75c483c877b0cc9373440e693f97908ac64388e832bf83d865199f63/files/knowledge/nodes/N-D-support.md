---
{
  "schema_version": "2.0.0",
  "id": "N-D-support",
  "kind": "definition",
  "title": "Support sense of a Laplacian inequality",
  "facets": [
    "foundations",
    "methods"
  ],
  "question_ids": [
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Definition 12.5, p. 60",
      "role": "support"
    },
    {
      "source_id": "S-Eschenburg-Heintze-1984",
      "locator": "Section 6, p. 150",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    }
  ]
}
---

# Support sense of a Laplacian inequality

## Canonical statement

```latex
Let \(U\) be an open subset of a smooth Riemannian manifold, \(f\in C^0(U)\), and \(F\in C^0(U)\). The inequality \(\Delta f\le F\) holds in the upper-support sense if, for every \(x\in U\) and every \(\varepsilon>0\), there is a \(C^2\) function \(h\) on a neighborhood \(W\subset U\) of \(x\) such that
\[
h\ge f\text{ on }W,\qquad h(x)=f(x),\qquad \Delta h(x)\le F(x)+\varepsilon.
\]
The inequality \(\Delta f\ge F\) in the lower-support sense is defined by \(h\le f\), \(h(x)=f(x)\), and \(\Delta h(x)\ge F(x)-\varepsilon\).
```

## Explanation and evidence

The project fixes Delta=div grad. Upper supports represent Delta f<=F, lower supports represent Delta f>=F. The word support includes equality at the point and a one-sided inequality throughout a neighborhood. This is an interface for the Hopf–Calabi principle; the various weak/distributional equivalences are not assumed as definitions.
