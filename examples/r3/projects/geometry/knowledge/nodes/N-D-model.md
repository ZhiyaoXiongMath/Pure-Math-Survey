---
{
  "schema_version": "2.0.0",
  "id": "N-D-model",
  "kind": "definition",
  "title": "Space forms and radial model functions",
  "facets": [
    "foundations"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume",
    "N-Q-global",
    "N-Q-triangles"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Example 2.4, pp. 10\u201311; Theorem 5.5 and formula (5.14), pp. 19\u201320",
      "role": "support"
    }
  ],
  "links": []
}
---

# Space forms and radial model functions

## Canonical statement

```latex
For \(n\ge2\) and \(k\in\mathbb R\), let \(M_k^n\) be the complete simply connected n-dimensional space form with sectional curvature \(k\). Put
\[
D_k=\begin{cases}\pi/\sqrt{k},&k>0,\\+\infty,&k\le0,\end{cases}
\quad
s_k(t)=\begin{cases}\sin(\sqrt{k}t)/\sqrt{k},&k>0,\\t,&k=0,\\\sinh(\sqrt{-k}t)/\sqrt{-k},&k<0.\end{cases}
\]
For \(0<t<D_k\) set \(c_k(t)=s_k'(t)/s_k(t)\). Thus
\(s_k''+ks_k=0\), \(s_k(0)=0\), \(s_k'(0)=1\), and \(c_k'+c_k^2+k=0\).
Writing \(\omega_{n-1}=\operatorname{Vol}(S^{n-1}(1))\), the model ball volume is
\[
V_k^n(r)=\omega_{n-1}\int_0^{\min\{r,D_k\}}s_k(t)^{n-1}\,dt,\qquad r>0.
\]
```

## Explanation and evidence

The spherical endpoint is excluded from formulas involving s_k'/s_k. Model ball volume is extended by the full sphere volume after D_k; the polar integral uses min(r,D_k), not sin beyond its first zero. This convention prevents a spurious negative volume density.
