---
{
  "schema_version": "2.0.0",
  "id": "N-S-main",
  "kind": "result",
  "title": "Classical Schur-complement criterion",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-schur"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Boyd",
      "locator": "Appendix A.5.5, pp.650-651",
      "role": "support"
    }
  ],
  "links": [
    {
      "target": "N-S-square",
      "relation": "proof_input"
    }
  ]
}
---

# Classical Schur-complement criterion

## Canonical statement

```latex
Let $p,q\geq1$, let $A\in\mathbb R^{p\times p}$ and $C\in\mathbb R^{q\times q}$
be symmetric, and let $B\in\mathbb R^{p\times q}$. Assume $A>0$, where
$H>0$ means $v^THv>0$ for every nonzero real vector $v$ of the appropriate size.
Set
\[
 M=\begin{pmatrix}A&B\\B^T&C\end{pmatrix},\qquad S=C-B^TA^{-1}B.
\]
Then $M>0$ if and only if $S>0$. Moreover, for every fixed $y\in\mathbb R^q$,
\[
 \min_{x\in\mathbb R^p}(x,y)^TM(x,y)=y^TSy,
 \qquad x_{\min}=-A^{-1}By.
\]
The minimizer is unique. This is a classical quadratic-form identity and criterion.
```

## Both directions
The [square expansion](N-S-square.md#derivation) gives Q=z^TAz+y^TSy. If S>0, every nonzero (z,y) has a nonzero component, so Q>0. Conversely, for each nonzero y set x=-A^{-1}By. The pair is nonzero and Q=y^TSy, hence positivity of M implies S>0. The same expansion proves the stated minimization. Strict positivity of A also implies its invertibility: Ax=0 would give x^TAx=0.

## Return to the question
The decisive object S is constructed by canceling the cross term. No spectral diagonalization of M is required. The argument's precise limit is [mere invertibility](N-S-boundary.md#models-and-failure).
