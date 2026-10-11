---
{
  "schema_version": "2.0.0",
  "id": "N-comparison",
  "kind": "relation",
  "title": "Congruence and variational elimination",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-guide",
      "locator": "Appendix A",
      "role": "provenance"
    }
  ],
  "links": [
    {
      "target": "N-square",
      "relation": "proof_input"
    },
    {
      "target": "N-inverse",
      "relation": "proof_input"
    }
  ]
}
---

# Congruence and variational elimination

## Canonical statement

```latex
Let $A\in\mathbb R^{p\times p}$ be symmetric and invertible,
$B\in\mathbb R^{p\times q}$ and $C\in\mathbb R^{q\times q}$ symmetric.
For
\[
 M=\begin{pmatrix}A&B\\B^{\mathsf T}&C\end{pmatrix},\quad
 T=\begin{pmatrix}I_p&-A^{-1}B\\0&I_q\end{pmatrix},\quad
 S=C-B^{\mathsf T}A^{-1}B,
\]
one has $T^{\mathsf T}MT=\operatorname{diag}(A,S)$.
Because $T$ is invertible, $M>0$ is equivalent to $A>0$ and $S>0$ jointly;
$S>0$ alone is not sufficient without $A>0$.
```

## Square completion and inverse map
Let Q(x,y)=x^T A x+2x^T B y+y^T C y. Since A is symmetric and invertible,
(A^{-1})^T=A^{-1}. Expanding z=x+A^{-1}By yields
z^T A z=x^T A x+2x^T B y+y^T B^T A^{-1}By. Subtract the final term
and add y^T C y to get the canonical square identity. The map inverse is
x=z-A^{-1}By; it preserves the nonzero condition jointly in the two variables.

## Both directions and actual hypothesis use
If A>0 and S>0, every nonzero pair (z,y) has at least one nonzero component,
so z^T A z+y^T S y>0. If M>0, for each nonzero y choose x=-A^{-1}By;
the pair (x,y) is nonzero and the square term vanishes, so y^T S y>0.
This is necessity for every nonzero y, not just one test vector.

## Congruence and minimization
Block multiplication gives MT=[[A,0],[B^T,S]], and then T^T MT=diag(A,S).
Congruence preserves positivity because v->Tv is a bijection on nonzero vectors.
For fixed y, the square term has unique minimum zero at x=-A^{-1}By when A>0.
Thus min_x Q(x,y)=y^T S y. If A merely invertible but indefinite, the identity
still holds but the square term need not have a minimum or positive sign.

## Boundary and model
For p=q=1, A=(a)>0, S=c-b^2/a. For a=2,b=1,c=1, S=1/2>0.
A=-1,B=0,C=1 gives S=1>0 but M=diag(-1,1) is indefinite. If A is singular,
the stated inverse is unavailable; no pseudoinverse criterion is claimed.
This is known classical linear algebra rederived in full, not a novelty assertion.
