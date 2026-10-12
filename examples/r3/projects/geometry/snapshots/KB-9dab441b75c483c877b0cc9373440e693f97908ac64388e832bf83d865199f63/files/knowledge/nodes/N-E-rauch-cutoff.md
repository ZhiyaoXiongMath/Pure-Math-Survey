---
{
  "schema_version": "2.0.0",
  "id": "N-E-rauch-cutoff",
  "kind": "example",
  "title": "The Rauch conjugate-time restriction cannot be discarded",
  "facets": [
    "boundaries"
  ],
  "question_ids": [
    "N-Q-local"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "proof_input",
      "target": "N-R-rauch"
    }
  ]
}
---

# The Rauch conjugate-time restriction cannot be discarded

## Explanation and evidence

Compare unit-initial-derivative normal Jacobi fields in space forms of curvature 2 and 1:
\[
|J_2(t)|=|\sin(\sqrt2t)|/\sqrt2,\qquad |J_1(t)|=|\sin t|.
\]
Before the higher-curvature conjugate time pi/sqrt2 the larger curvature produces the shorter field. At t=pi, |J_1|=0 whereas |J_2|>0 (sqrt2 is not an integer). The same order cannot be continued for arbitrary times. Both manifolds are complete, so completeness does not repair this missing hypothesis.

By continuity the same strict reversal already holds for some t<pi sufficiently close to pi, while t>pi/sqrt(2). Thus even retaining the model restriction t<D_1=pi does not allow removal of the actual first-conjugate-time restriction in the lower-sectional branch.
