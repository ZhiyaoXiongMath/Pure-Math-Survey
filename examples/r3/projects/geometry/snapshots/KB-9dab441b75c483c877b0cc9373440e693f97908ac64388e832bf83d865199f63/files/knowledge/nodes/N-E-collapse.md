---
{
  "schema_version": "2.0.0",
  "id": "N-E-collapse",
  "kind": "example",
  "title": "A fixed Ricci lower bound does not prevent collapse",
  "facets": [
    "boundaries",
    "results"
  ],
  "question_ids": [
    "N-Q-volume"
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
      "target": "N-R-bishop-gromov"
    },
    {
      "relation": "proof_input",
      "target": "N-R-gunther"
    }
  ]
}
---

# A fixed Ricci lower bound does not prevent collapse

## Explanation and evidence

Let M_epsilon=S^1_epsilon×R^{n-1}, n>=2, with the product flat metric and circle radius epsilon. For every epsilon>0, the manifold is complete and Ric=0. For a fixed r>0,
\[
B_{M_\epsilon}(p,r)\subset S^1_\epsilon\times B_{\mathbb R^{n-1}}(0,r),\qquad
\operatorname{Vol}B(p,r)\le2\pi\epsilon\,\omega_{n-1}^{\rm ball}r^{n-1}\to0.
\]
Thus fixed n and Ric>=0 do not give a positive lower bound for a unit ball. Also sec=0, so a global lower volume bound Vol B(p,r)>=Vol B_Rn(r) from sec<=0 alone is false. The injectivity radius here is pi epsilon, exactly the missing scale restriction in [[N-R-gunther]]. The notation omega^{ball}_{n-1} means the volume of the unit (n-1)-ball, not the area omega_{n-1} in N-D-model.
