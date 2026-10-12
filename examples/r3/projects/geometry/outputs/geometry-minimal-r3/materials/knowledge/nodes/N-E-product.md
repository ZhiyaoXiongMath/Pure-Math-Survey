---
{
  "schema_version": "2.0.0",
  "id": "N-E-product",
  "kind": "example",
  "title": "Positive Ricci does not supply a positive sectional lower bound",
  "facets": [
    "boundaries",
    "methods"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-triangles"
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
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-triangle"
    }
  ]
}
---

# Positive Ricci does not supply a positive sectional lower bound

## Explanation and evidence

On S^2(1)×S^2(1), the product curvature tensor gives Ric=g, while planes using one direction in each factor have K=0. Since n=4, Ric=3(1/3)g. A geodesic in the first factor and a normal parallel field in the second give J=tE and the corresponding radial Hessian eigenvalue 1/t. This exceeds c_{1/3}(t) for sufficiently small positive t. The Ricci hypothesis of Laplacian comparison therefore does not imply the directional Hessian inequality at k=1/3.

For a triangle test, take two length-r segments in separate factors at right angle. Product distance is sqrt(2)r. The model same-angle hinge at curvature k=1/3 satisfies
\[
\cos(\sqrt{k}c)=\cos^2(\sqrt{k}r),\qquad
c^2=2r^2-\tfrac{k}{3}r^4+O(r^6).
\]
To check the coefficient, expand the left as 1-k c^2/2+k^2c^4/24 and the right as 1-kr^2+k^2r^4/3. Substitution c^2=2r^2+A r^4 gives A=-k/3. Hence c<sqrt(2)r for small r, contradicting the hypothetical Ricci-only hinge inequality. The triangles have small perimeter, so no model-radius exception explains the failure.
