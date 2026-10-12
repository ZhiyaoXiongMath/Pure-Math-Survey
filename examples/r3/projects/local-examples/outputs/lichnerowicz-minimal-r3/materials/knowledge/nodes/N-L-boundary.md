---
{
  "schema_version": "2.0.0",
  "id": "N-L-boundary",
  "kind": "example",
  "title": "Where the eigenvalue proof uses its hypotheses",
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
  "sources": [],
  "links": [
    {
      "target": "N-L-main",
      "relation": "explains"
    }
  ]
}
---

# Where the eigenvalue proof uses its hypotheses

## Dimension and discarded information
At m=1 the factor m-1 vanishes, so the concluding division cannot occur. This is a genuine failure of the normalized assertion: on a circle of radius R, Ric=0=(m-1)g and Delta cos(theta)=R^{-2}cos(theta). The first positive eigenvalue is R^{-2}, which is below 1 for R>1 (by the elementary periodic Fourier spectrum).

Without a curvature lower bound of this normalization, the Ricci integral cannot be replaced by (m-1) times the gradient energy. With a boundary, integration of the divergence has a boundary term and the present argument does not establish either a Dirichlet or Neumann statement. For lambda=0, f is constant and division by lambda is impossible; this is why the theorem concerns a positive eigenvalue. Equality in the algebra is not an isometry theorem, and no Obata rigidity proof is included.

## Why the Hessian term matters
If the nonnegative Hessian term is discarded in integrated Bochner, one obtains only lambda>=(m-1). Keeping the trace recovers lambda>=m. The comparison follows by repeating the same division of gradient energy, which is positive for a positive eigenfunction. This explains the choice of the Cauchy-Schwarz input.
