---
{
  "schema_version": "2.0.0",
  "id": "N-cone",
  "kind": "result",
  "title": "Compactness from a cone gauge and a weak derivative",
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
      "source_id": "S-barrett-suli",
      "locator": "Theorem 1 and Remark 2, pp. 3--4",
      "role": "support",
      "version": "arXiv:1101.1990v2, submitted 16 April 2011, 17 pages"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-cone-definition"
    },
    {
      "relation": "explained_by",
      "target": "N-cone-mechanism"
    }
  ]
}
---

# Compactness from a cone gauge and a weak derivative

## Canonical statement

```latex
Let $T>0$, let $A_0,A_1$ be real Banach spaces with a continuous linear injection $A_0\hookrightarrow A_1$, and let $\mathcal M_+\subset A_0$ be closed under multiplication by nonnegative scalars.
Suppose its gauge $[\cdot]:\mathcal M_+\to[0,\infty)$ satisfies
\[
[z]=0\Longleftrightarrow z=0,\qquad [cz]=c[z]\quad(c\ge0),
\qquad \|z\|_{A_0}\le C_0[z],
\]
and every gauge-bounded sequence in $\mathcal M_+$ has a subsequence converging in $A_0$.
Fix $1\le p,q\le\infty$ with either $q>1$, or $q=1$ and $p<\infty$.
Let $F$ be a family of strongly measurable $A_0$-valued functions $v$ on $(0,T)$ with $v(t)\in\mathcal M_+$ almost everywhere and measurable $t\mapsto[v(t)]$.
Assume the distributional derivatives $v'$ are $A_1$-valued and
\[
\sup_{v\in F}\left(\|[v(\cdot)]\|_{L^p(0,T)}+
\|v'\|_{L^q(0,T;A_1)}\right)<\infty.
\]
Then $F$ is relatively compact in $L^p(0,T;A_0)$.
The assertion includes $p=\infty$ only when $q>1$; it does not assert that limits belong to a nonclosed cone.
```

## Interpretation


Theorem 1 in the 2011 arXiv v2, with p1 renamed q and the cone definition repeated to make the principal self-contained. This is a bounded-family reformulation of compact embedding. N-cone-mechanism supplies a local proof using Simon's criterion and the verified two-point Ehrling lemma, without relying on the unresolved passage around source (2.8).
