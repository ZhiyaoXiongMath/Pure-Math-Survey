---
{
  "schema_version": "2.0.0",
  "id": "N-L-inputs",
  "kind": "result",
  "title": "The precise Bochner and spectral inputs",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-lich"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Datar",
      "locator": "Proposition 29.1.1 and Theorem 29.2.1, pp.217-218",
      "role": "support"
    }
  ],
  "links": []
}
---

# The precise Bochner and spectral inputs

## Canonical statement

```latex
Let $(M^m,g)$ be a closed connected smooth Riemannian manifold with $m\geq2$ and put
$\Delta=-\operatorname{div}_g\nabla$. The scalar Laplacian has a smallest
positive eigenvalue $\lambda_1>0$ with a nonzero smooth real eigenfunction
$f$ satisfying $\Delta f=\lambda_1 f$.
For every smooth real $h$ on $M$, the scalar Bochner identity in this sign convention is
\[
 -\tfrac12\Delta|\nabla h|^2
 =|\Hess h|^2-\langle\nabla\Delta h,\nabla h\rangle
   +\Ric(\nabla h,\nabla h).
\]
Here $\Hess h(X,Y)=\langle\nabla_X\nabla h,Y\rangle$, its norm is the
pointwise Hilbert--Schmidt norm, and $\tr_g\Hess h=-\Delta h$.
The spectral existence and local Bochner identity are imported classical inputs.
```

## Import scope and sign
Datar Proposition 29.1.1 uses L=div grad; substituting L=-Delta yields precisely this formula. Theorem 29.2.1 gives smooth spectral eigenfunctions; connectedness identifies the zero eigenspace with constants. Neither that spectral theorem nor a derivation of the local curvature commutator is promised here. The integrations and inequalities consuming these inputs are proved in [the connection](N-L-connection.md#integration-and-trace).
