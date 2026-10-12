---
{
  "schema_version": "2.0.0",
  "id": "N-translation-definition",
  "kind": "definition",
  "title": "Uniform translation control and compact embeddings",
  "facets": [
    "foundations"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-simon",
      "locator": "Section 3, pp. 71--73; Section 8, p. 84",
      "role": "support",
      "version": "Journal text, Ann. Mat. Pura Appl. 146, pp. 65--96, DOI 10.1007/BF01762360; publisher issue date December 1986 (frequently cited as 1987)"
    }
  ],
  "links": []
}
---

# Uniform translation control and compact embeddings

## Canonical statement

```latex
Let $E$ be a Banach space, $T>0$, and $1\le p\le\infty$.
For $f\in L^p(0,T;E)$ and $0<h<T$, set $(\tau_h f)(t)=f(t+h)$ for $0<t<T-h$.
A family $F\subset L^p(0,T;E)$ has uniform $L^p(E)$ translation control if
\[
\lim_{h\downarrow0}\sup_{f\in F}\|\tau_hf-f\|_{L^p(0,T-h;E)}=0.
\]
Here $L^p$ consists of strongly measurable functions modulo almost-everywhere equality, with its usual Bochner norm (essential supremum for $p=\infty$).
A continuous linear injection $X\hookrightarrow E$ is compact, written $X\Subset E$, if every norm-bounded sequence in $X$ has a subsequence convergent in $E$.
```

## Interpretation


The translation estimate must be uniform over the family; translation continuity of each individual function is insufficient. Compactness of X->E concerns bounded sets, not all points of an unbounded image. The limit may lie outside X.
