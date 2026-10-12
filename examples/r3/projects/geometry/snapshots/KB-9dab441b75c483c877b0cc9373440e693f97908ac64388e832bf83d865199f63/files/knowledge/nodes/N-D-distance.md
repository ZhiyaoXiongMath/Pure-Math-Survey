---
{
  "schema_version": "2.0.0",
  "id": "N-D-distance",
  "kind": "definition",
  "title": "Cut time, conjugate time and the regular distance domain",
  "facets": [
    "foundations",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume",
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Section 5, pp. 17\u201319",
      "role": "support"
    },
    {
      "source_id": "S-Bishop-2013v2",
      "locator": "Section 8.1, p. 54",
      "role": "support"
    }
  ],
  "links": []
}
---

# Cut time, conjugate time and the regular distance domain

## Canonical statement

```latex
Let \((M,g)\) be connected and complete, \(p\in M\), and \(v\in T_pM\) with \(|v|=1\). Write \(\gamma_v(t)=\exp_p(tv)\) and \(r_p(x)=d_g(p,x)\). Define
\[
\tau_p(v)=\sup\{t>0:d_g(p,\gamma_v(t))=t\},\qquad
\operatorname{Cut}(p)=\{\gamma_v(\tau_p(v)):\tau_p(v)<\infty\}.
\]
The first conjugate time is the infimum of \(t>0\) for which there exists a nonzero Jacobi field \(J\) along \(\gamma_v\) with \(J(0)=J(t)=0\), with infimum \(+\infty\) if none exists.
The regular distance domain is \(M\setminus(\{p\}\cup\operatorname{Cut}(p))\).
The injectivity radius at p is \(\operatorname{inj}_p(M)=\inf_{|v|=1}\tau_p(v)\).
```

## Explanation and evidence

On a complete manifold the cut time is at most the first conjugate time. The map v↦tau_p(v) on the unit tangent sphere is continuous with values in (0,+infinity], with the extended-real topology (Eschenburg §5, p.17). This is an imported input used in volume rigidity. A cut point can instead result from competing minimizing geodesics. Off p and Cut(p), r_p is smooth and has a unique minimizing radial segment. The measure-zero cut locus and polar integration are imported geometric inputs (Eschenburg §5; Bishop §8.1). They are not consequences merely of writing polar coordinates.
