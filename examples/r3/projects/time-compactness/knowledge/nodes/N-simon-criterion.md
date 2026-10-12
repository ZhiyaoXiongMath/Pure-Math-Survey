---
{
  "schema_version": "2.0.0",
  "id": "N-simon-criterion",
  "kind": "result",
  "title": "Interval integrals and translations",
  "facets": [
    "foundations",
    "methods"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-simon",
      "locator": "Theorem 1 and proof, pp. 71--73",
      "role": "support",
      "version": "Journal text, Ann. Mat. Pura Appl. 146, pp. 65--96, DOI 10.1007/BF01762360; publisher issue date December 1986 (frequently cited as 1987)"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-translation-definition"
    }
  ]
}
---

# Interval integrals and translations

## Canonical statement

```latex
Let $E$ be a Banach space, $T>0$, $1\le p\le\infty$, and $F\subset L^p(0,T;E)$.
Assume that for every $0<a<b<T$ the set
\[
\left\{\int_a^b f(t)\,dt:f\in F\right\}
\]
is relatively compact in $E$, and that
\[
\lim_{h\downarrow0}\sup_{f\in F}\|f(\cdot+h)-f\|_{L^p(0,T-h;E)}=0.
\]
Then $F$ is relatively compact in $L^p(0,T;E)$ if $p<\infty$.
If $p=\infty$, its elements have continuous representatives on $[0,T]$ and these representatives form a relatively compact subset of $C([0,T];E)$ with the supremum norm.
```

## Interpretation


This is the sufficient direction of Simon's Theorem 1. The complete characterization for finite p is not needed here. In the infinity case it is not a characterization of arbitrary compact subsets of L-infinity. The imported proof uses right means and then time reversal to cover both endpoints.
