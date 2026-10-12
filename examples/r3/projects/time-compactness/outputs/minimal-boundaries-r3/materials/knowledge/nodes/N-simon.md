---
{
  "schema_version": "2.0.0",
  "id": "N-simon",
  "kind": "result",
  "title": "Compact linear embeddings with weak-space translations",
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
      "source_id": "S-simon",
      "locator": "Theorem 5, pp. 84--85",
      "role": "support",
      "version": "Journal text, Ann. Mat. Pura Appl. 146, pp. 65--96, DOI 10.1007/BF01762360; publisher issue date December 1986 (frequently cited as 1987)"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-translation-definition"
    },
    {
      "relation": "explained_by",
      "target": "N-linear-mechanism"
    }
  ]
}
---

# Compact linear embeddings with weak-space translations

## Canonical statement

```latex
Let $T>0$, $1\le p\le\infty$, and let $X,B,Y$ be Banach spaces with continuous linear injections
\[
X\Subset B\hookrightarrow Y,
\]
where the first injection is compact. Let $F\subset L^p(0,T;X)$ satisfy
\[
\sup_{f\in F}\|f\|_{L^p(0,T;X)}<\infty,
\qquad
\lim_{h\downarrow0}\sup_{f\in F}\|f(\cdot+h)-f\|_{L^p(0,T-h;Y)}=0.
\]
Then $F$ is relatively compact in $L^p(0,T;B)$ for $p<\infty$.
For $p=\infty$, the $B$-valued continuous representatives of the elements of $F$ form a relatively compact set in $C([0,T];B)$.
```

## Interpretation


All embeddings and T are fixed. No reflexivity is assumed. Uniform weak-space time control and spatial boundedness are joint premises. The theorem does not infer time regularity of an input u from that of a nonlinear image K(u).
