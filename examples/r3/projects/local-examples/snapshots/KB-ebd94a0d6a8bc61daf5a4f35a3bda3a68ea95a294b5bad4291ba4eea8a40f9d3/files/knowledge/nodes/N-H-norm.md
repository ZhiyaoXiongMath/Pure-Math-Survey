---
{
  "schema_version": "2.0.0",
  "id": "N-H-norm",
  "kind": "definition",
  "title": "A fixed Holder norm on a compact manifold",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-holder"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": []
}
---

# A fixed Holder norm on a compact manifold

## Canonical statement

```latex
Fix a compact smooth $d$-manifold $M$ without boundary, a smooth background metric,
a finite smooth atlas $(U_a,\phi_a)$ and a smooth partition of unity $(\chi_a)$
with $\operatorname{supp}\chi_a\Subset U_a$.
For $0<\gamma<1$, extend $v_a=(\chi_a u)\circ\phi_a^{-1}$ by zero to $\mathbb R^d$ and set
\[
 \|u\|_{2,\gamma}=\sum_a\left(\sum_{|\nu|\leq2}\|D^\nu v_a\|_\infty
       +\sum_{|\nu|=2}[D^\nu v_a]_\gamma\right),
 \qquad [w]_\gamma=\sup_{x\ne y}\frac{|w(x)-w(y)|}{|x-y|^\gamma}.
\]
Here $\nu$ is a multi-index, and $C^{2,\gamma}(M)$ consists of the $C^2$ functions
for which this norm is finite. All these choices stay fixed throughout a sequence.
```

## Why localization is fixed
Compact support inside each chart makes zero extension C^2. Multiplication by a fixed smooth cutoff and a fixed smooth coordinate change are bounded on these Holder norms on compact sets, by the product and chain rules. Thus the finite expression is a legitimate norm for the usual C^{2,gamma} topology. Its constants may depend on this atlas and the background, but never on the sequence index. The partition identity u=sum_a chi_a u reconstructs the global function from localized pieces.
