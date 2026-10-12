---
{
  "schema_version": "2.0.0",
  "id": "N-cone-ehrling",
  "kind": "result",
  "title": "Two-point Ehrling comparison on a cone",
  "facets": [
    "methods"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-barrett-suli",
      "locator": "Lemma 1 and proof, pp. 4--5",
      "role": "support",
      "version": "arXiv:1101.1990v2, submitted 16 April 2011, 17 pages"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-cone-definition"
    }
  ]
}
---

# Two-point Ehrling comparison on a cone

## Canonical statement

```latex
Let $A_0\hookrightarrow A_1$ be a continuous linear injection of real Banach spaces.
Let $\mathcal M_+\subset A_0$ be a seminormed nonnegative cone with gauge $[\cdot]$, satisfying $\|z\|_{A_0}\le C[z]$ and compactness of gauge-bounded sequences in $A_0$.
Then for every $\eta>0$ there is $C_\eta<\infty$ such that
\[
\|u-v\|_{A_0}\le\eta([u]+[v])+C_\eta\|u-v\|_{A_1}
\quad\text{for all }u,v\in\mathcal M_+.
\]
Here the cone is closed under nonnegative scalar multiplication and its gauge is positive definite and positively degree-one homogeneous; no addition or subtraction closure is assumed.
```

## Interpretation


Proof: if false at eta0, choose u_n,v_n with ||u_n-v_n||A0>eta0([u_n]+[v_n])+n||u_n-v_n||A1. Let a_n=[u_n]+[v_n]>0 and divide each point by a_n. Both resulting gauge values are <=1, so a common subsequence converges in A0. Its difference has A1 norm at most its bounded A0 norm divided by n, hence tends to zero. Injectivity makes the two A0 limits equal, contradicting their A0 separation >eta0. This reads and reconstructs the entire source Lemma 1 proof, pp.4--5. The sum of the two gauges is essential because the difference may not lie in the cone.
