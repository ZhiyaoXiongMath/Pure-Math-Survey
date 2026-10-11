---
{
  "schema_version": "2.0.0",
  "id": "N-norm",
  "kind": "definition",
  "title": "Fixed periodic Holder norms",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-guide",
      "locator": "Appendix B",
      "role": "provenance"
    }
  ],
  "links": []
}
---

# Fixed periodic Holder norms

## Canonical statement

```latex
For an integer $d\geq1$, write $\rho$ for flat distance on
$\mathbb T^d=\mathbb R^d/\mathbb Z^d$ and set, for $0<\gamma<1$,
\[
 [v]_\gamma=\sup_{x\ne y}\frac{|v(x)-v(y)|}{\rho(x,y)^\gamma},\qquad
 \|u\|_{C^{2,\gamma}}
 =\max_{|\nu|\leq2}\|D^\nu u\|_\infty
   +\max_{|\nu|=2}[D^\nu u]_\gamma.
\]
Here $D^\nu$ denotes a periodic coordinate derivative of multi-index $\nu$.
Only the fixed flat structure is used below.
```

## Local meaning

This is the exact norm used in the principal and compactness lemma. Maxima run over finitely many multi-indices; the first includes order zero. The lower-order sup norms and top-order Holder seminorm are both required. The definitions use the fixed flat torus, not varying charts or an unspecified norm family.
