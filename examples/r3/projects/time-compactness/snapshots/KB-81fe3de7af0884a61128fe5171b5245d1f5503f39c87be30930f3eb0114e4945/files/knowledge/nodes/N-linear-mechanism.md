---
{
  "schema_version": "2.0.0",
  "id": "N-linear-mechanism",
  "kind": "mechanism",
  "title": "Linear Ehrling estimate and a compactness upgrade",
  "facets": [
    "methods"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-simon",
      "locator": "Lemmas 8--9 and proof of Theorem 5, pp. 84--85",
      "role": "support",
      "version": "Journal text, Ann. Mat. Pura Appl. 146, pp. 65--96, DOI 10.1007/BF01762360; publisher issue date December 1986 (frequently cited as 1987)"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-simon-criterion"
    }
  ]
}
---

# Linear Ehrling estimate and a compactness upgrade

## Fast route and inputs

The [linear theorem](N-simon.md) fixes $X\Subset B\hookrightarrow Y$. Write
\[
M=\sup_{f\in F}\|f\|_{L^p(0,T;X)}<\infty.
\]
Uniform translations are known in $L^p(Y)$, whereas the desired convergence is in $L^p(B)$. First obtain compactness in $Y$, then transfer a Cauchy subsequence to $B$ by an adjustable estimate.

## Slow route: compact averages

For an interior interval $I=(a,b)$, Hölder gives
\[
\left\|\int_I f(t)\,dt\right\|_X\le |I|^{1-1/p}M.
\]
The fixed compact injection makes these integrals relatively compact in $B$, hence in $Y$. The exact imported [interval-integral criterion](N-simon-criterion.md), applied in $Y$, supplies an $L^p(Y)$-Cauchy subsequence. At $p=\infty$ it supplies continuous $Y$ representatives and uniform convergence.

## Slow route: the norm upgrade

For every $\eta>0$, compactness and injectivity give
\[
\|z\|_B\le\eta\|z\|_X+C_\eta\|z\|_Y,\qquad z\in X.
\]
To verify this, suppose it fails at $\eta_0$. Normalize a violating sequence by its positive $X$ norm. Its $X$ norm is one, its $B$ norm exceeds $\eta_0$, and its $Y$ norm tends to zero, since the $B$ norms are uniformly bounded. Compactness gives a $B$ limit; continuity and injectivity force that limit to be zero, a contradiction.

Apply the estimate to $f_n(t)-f_m(t)$ and use Minkowski:
\[
\|f_n-f_m\|_{L^p(B)}\le 2\eta M+C_\eta\|f_n-f_m\|_{L^p(Y)}.
\]
For $M>0$, choose $\eta<\varepsilon/(4M)$ first, then $n,m$ so that the second term is below $\varepsilon/2$. If $M=0$, the family vanishes. Completeness gives the required strong limit.

At $p=\infty$, continuous $B$ representatives can be recovered from the same estimate: on the full-measure dense set where $\|f(t)\|_X\le M$, first choose $\eta$ and then use continuity in $Y$ to obtain uniform continuity in $B$. Extend by completeness and identify the $Y$ representative through the injection. Thus continuity is not assumed of arbitrary $L^\infty$ equivalence classes.

## Consumption and boundary

This argument proves the mechanism behind [N-simon](N-simon.md). Additivity is consumed twice: in the $X$-valued integral and in $f_n-f_m\in X$. For nonlinear images the replacement is [truncation](N-truncation.md); for cones the replacement is [two-point Ehrling](N-cone-ehrling.md).
