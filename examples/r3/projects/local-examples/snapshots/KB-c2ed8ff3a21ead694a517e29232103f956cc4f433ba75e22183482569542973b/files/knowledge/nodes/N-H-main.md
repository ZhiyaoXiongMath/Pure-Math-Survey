---
{
  "schema_version": "2.0.0",
  "id": "N-H-main",
  "kind": "result",
  "title": "Conditional closedness with strict admissibility",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-holder"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
    {
      "target": "N-H-norm",
      "relation": "uses_definition"
    },
    {
      "target": "N-H-compact",
      "relation": "proof_input"
    }
  ]
}
---

# Conditional closedness with strict admissibility

## Canonical statement

```latex
Fix the compact smooth manifold and norms just defined, integers $d,r\geq1$,
and $0<\beta<\alpha<1$. Let
\[
 A:C^{2,\beta}(M)\longrightarrow C^0(M;\Sym_r(\mathbb R))
\]
be continuous for the uniform operator norm in the target. Define
\[
 \mathcal U=\{u\in C^{2,\beta}(M):A(u)(x)>0\ \text{for every }x\in M\},
 \qquad \mathcal F:[0,1]\times\mathcal U\longrightarrow C^0(M),
\]
and assume $\mathcal F$ is jointly continuous. Suppose $t_j\to t_*$ and
$u_j\in C^{2,\alpha}(M)\cap\mathcal U$ satisfy, with fixed $C<\infty$ and $\delta>0$,
\[
 \mathcal F(t_j,u_j)=0,\qquad \|u_j\|_{2,\alpha}\leq C,\qquad
 A(u_j)(x)\geq\delta I_r\quad\text{for every }j,x.
\]
Then some subsequence converges in $C^{2,\beta}(M)$ to $u_*\in C^{2,\alpha}(M)$, with
\[
 \|u_*\|_{2,\alpha}\leq C,\quad A(u_*)(x)\geq\delta I_r\quad(x\in M),
 \quad u_*\in\mathcal U,\quad\mathcal F(t_*,u_*)=0.
\]
This is conditional on the displayed bounds and continuity; it asserts neither
existence of such solutions nor higher regularity or convergence in $C^{2,\alpha}$.
```

## Domain before equation
Use [extraction and interpolation](N-H-compact.md#derivative-extraction) to obtain strong C^{2,beta} convergence. Continuity of A now gives uniform matrix convergence. For each x and v in R^r, pass to the limit in v^T A(u_j)(x)v>=delta|v|^2. Thus A(u_*)(x)>=delta I_r, so u_* lies in U. Only now may the joint continuity of F on [0,1]xU be applied. It gives F(t_*,u_*)=lim F(t_j,u_j)=0 in C^0.

## Other constraints and actual PDE continuity
If each u_j has integral zero, then |integral(u_j-u_*)|<=Vol(M)||u_j-u_*||_infty proves normalization passes. The present M has no boundary; boundary data require separate hypotheses and are not silently added.

For a concrete continuity check on a flat torus, F(t,u)=tr(D^2u)+u^3-t h with fixed continuous h maps C^{2,beta} jointly continuously to C^0. Indeed the second derivatives converge uniformly, while on a common bounded range |u_j^3-u^3|<=3R^2|u_j-u| and |t_j-t| ||h||_infty->0. This is an illustration of checking continuity, not a proof of solution estimates for this equation. For a continuous jet expression H(t,x,u,Du,D^2u), the jets remain in a compact bounded set, and uniform continuity of H there proves the same assertion. Expressions singular at a cone boundary require the previously checked margin.
