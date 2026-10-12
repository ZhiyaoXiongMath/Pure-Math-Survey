---
{
  "schema_version": "2.0.0",
  "id": "N-L-main",
  "kind": "result",
  "title": "Lichnerowicz eigenvalue lower bound",
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
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Datar",
      "locator": "Theorem 29.2.2, lower-bound part, pp.218-219",
      "role": "support"
    }
  ],
  "links": [
    {
      "target": "N-L-inputs",
      "relation": "proof_input"
    },
    {
      "target": "N-L-connection",
      "relation": "proof_input"
    }
  ]
}
---

# Lichnerowicz eigenvalue lower bound

## Canonical statement

```latex
Let $(M^m,g)$ be a closed connected smooth Riemannian manifold of dimension
$m\geq2$. Suppose that for every $x\in M$ and $v\in T_xM$,
\[
 \Ric_g(v,v)\geq(m-1)g(v,v).
\]
For the nonnegative Laplacian $\Delta=-\operatorname{div}_g\nabla$, let
$\lambda_1$ denote its smallest positive eigenvalue on smooth real functions.
Then $\lambda_1\geq m$. This classical bound makes no equality-rigidity claim.
```

## Closing the estimate
Choose the nonzero smooth eigenfunction supplied by N-L-inputs and put lambda=lambda_1. Let I=integral_M f^2>0. Combining the integrated Bochner identity, Ricci lower bound and Hessian trace inequality gives
\[
\lambda^2 I\geq \lambda^2 I/m+(m-1)\lambda I.
\]
Thus ((m-1)/m)lambda^2 I>=(m-1)lambda I. Division by (m-1)lambda I>0 is valid because m>=2, lambda>0 and f is nonzero. It yields lambda>=m. This proves precisely the target using [the connection](N-L-connection.md#integration-and-trace).
