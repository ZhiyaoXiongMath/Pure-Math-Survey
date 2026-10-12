---
{
  "schema_version": "2.0.0",
  "id": "N-M-cheng",
  "kind": "mechanism",
  "title": "The excess function exposes maximal-diameter equality",
  "facets": [
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
      "locator": "Proof of Theorem 12.1, pp. 61\u201362",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-M-support"
    },
    {
      "relation": "proof_input",
      "target": "N-M-trace"
    },
    {
      "relation": "proof_input",
      "target": "N-R-myers"
    }
  ]
}
---

# The excess function exposes maximal-diameter equality

## Explanation and evidence

Rescale g to k g so that k=1. Choose points p,q at distance pi (Myers compactness ensures the diameter is attained). The excess e=d(p,·)+d(q,·)-pi is nonnegative and vanishes along a minimizing segment. Where both distances lie in (0,pi), support Laplacian comparison gives
\[
\Delta e\le(n-1)(\cot r_p+\cot r_q)
=(n-1)\frac{\sin(r_p+r_q)}{\sin r_p\sin r_q}\le0.
\]
Here pi<=r_p+r_q<2pi. It is -e that is subharmonic and attains a maximum zero; e attains a minimum. The maximum-principle propagation and the radial equality analysis yield e=0 and the round polar metric. Those global propagation and endpoint steps remain imported from the source's rigidity theorem; the node records the decisive calculation rather than a complete independent proof.

Eschenburg p.62 contains apparent slips in the written distance inequality and the word maximum; the calculation above explicitly checks the correct signs. There is no claim that equality for one triangle, or one Jacobi field, forces ambient roundness.
