---
{
  "schema_version": "2.0.0",
  "id": "N-maitre",
  "kind": "result",
  "title": "Compact nonlinear maps with output translations",
  "facets": [
    "results"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-maitre",
      "locator": "Theorem 2.1 and Remark 2.2, p. 1726",
      "role": "support",
      "version": "Published IJMMS 2003:27, pp. 1725--1730, DOI 10.1155/S0161171203106175"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-translation-definition"
    },
    {
      "relation": "explained_by",
      "target": "N-truncation"
    }
  ]
}
---

# Compact nonlinear maps with output translations

## Canonical statement

```latex
Let $T>0$, $1\le p\le\infty$, and let $E_1,E_2$ be Banach spaces.
Let $K:E_1\to E_2$ map every bounded subset of $E_1$ into a relatively compact subset of $E_2$.
Let $U\subset L^1(0,T;E_1)$ be bounded and suppose that each $v(t)=K(u(t))$, $u\in U$, is strongly measurable.
Write $V=\{K(u):u\in U\}$ and assume $V\subset L^p(0,T;E_2)$, that for some $1<r\le\infty$
\[
\sup_{v\in V}\|v\|_{L^r(0,T;E_2)}<\infty,
\qquad
\lim_{h\downarrow0}\sup_{v\in V}\|v(\cdot+h)-v\|_{L^p(0,T-h;E_2)}=0.
\]
Then $V$ is relatively compact in $L^p(0,T;E_2)$ for $p<\infty$.
For $p=\infty$, the continuous representatives form a relatively compact set in $C([0,T];E_2)$.
No injectivity, linearity or monotonicity of $K$ is required. The conclusion concerns $K(u)$, not $u$.
```

## Interpretation


Published Theorem 2.1, with operator B renamed K and measurable-composition membership unpacked. The r=infinity case follows from any finite r>1 on a finite interval. The auxiliary r need not equal p. The theorem's r>1 is not asserted to be optimal; see discovery and the boundaries view.
