---
{
  "schema_version": "2.0.0",
  "id": "N-main",
  "kind": "result",
  "title": "Conditional sequential closedness",
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
      "locator": "Appendix B",
      "role": "provenance"
    }
  ],
  "links": [
    {
      "target": "N-compactness",
      "relation": "proof_input"
    },
    {
      "target": "N-margin",
      "relation": "proof_input"
    }
  ]
}
---

# Conditional sequential closedness

## Canonical statement

```latex
Fix integers $d,r\geq1$ and $0<\beta<\alpha<1$.
On the flat torus $\mathbb T^d=\mathbb R^d/\mathbb Z^d$, let
\[
 A:C^{2,\beta}(\mathbb T^d)\longrightarrow
 C^0(\mathbb T^d;\operatorname{Sym}_r(\mathbb R))
\]
be continuous, where the target has the uniform operator norm, and set
\[
 \mathcal U=\{u\in C^{2,\beta}(\mathbb T^d):
       A(u)(x)>0\text{ for every }x\in\mathbb T^d\}.
\]
Let $\mathcal F:[0,1]\times\mathcal U\to C^0(\mathbb T^d)$ be continuous.
Suppose $t_j\in[0,1]$, $t_j\to t_\infty$, and
$u_j\in C^{2,\alpha}(\mathbb T^d)\cap\mathcal U$ satisfy, for constants
$C<\infty$ and $\delta>0$ independent of $j$,
\[
 \mathcal F(t_j,u_j)=0,\qquad
 \|u_j\|_{C^{2,\alpha}}\leq C,\qquad
 A(u_j)(x)\geq\delta I_r\quad\text{for every }j,x.
\]
Then a subsequence converges in $C^{2,\beta}$ to a function
$u_\infty\in C^{2,\alpha}\cap\mathcal U$, with
\[
 A(u_\infty)(x)\geq\delta I_r\quad\text{for every }x,
 \qquad \mathcal F(t_\infty,u_\infty)=0.
\]
The norms are the fixed periodic derivative/H\"older norms defined immediately
before this statement. This is a conditional sequential closedness assertion,
not an existence theorem or a smoothness assertion.
```

## Diagonal extraction and derivatives
All periodic derivatives through order two are uniformly bounded. The second
ones are uniformly alpha-Holder; the lower ones have a common Lipschitz bound
from the next derivative. At the countable rational grid, iterated bounded real
subsequence extraction and a diagonal choice give convergence for every one of
these finitely many derivatives at every grid point. A finite epsilon-net and
the common modulus of continuity upgrade this convergence to uniform convergence.
For each coordinate interval, pass to the limit in the fundamental-theorem identity
D^nu u_j(x+h e_i)-D^nu u_j(x)=integral_0^h D^{nu+e_i}u_j(x+s e_i) ds
for |nu|<=1. The uniform limits are compatible derivatives of a C^2 limit u.
Passing fixed-point difference quotients to the limit preserves the uniform
alpha-Holder bounds of the second derivatives, so u is C^{2,alpha}.

## The strong topology
For any alpha-Holder w, the two inequalities
|w(x)-w(y)|<=2||w||_infty and <=[w]_alpha rho(x,y)^alpha give
[w]_beta <= (2||w||_infty)^{1-beta/alpha} [w]_alpha^{beta/alpha}.
This follows by splitting distances at the equality of the two bounds; zero
seminorm cases are immediate. Apply to each second-derivative difference.
Its sup norm tends to zero and its alpha seminorm is uniformly bounded.
Thus the subsequence converges in C^{2,beta}, not just C^2.

## Admissibility and passage through the equation
Continuity of A yields uniform H_j=A(u_j)->A(u). For every fixed x and unit
vector v, v^T H(x)v=lim v^T H_j(x)v>=delta, so H(x)>=delta I everywhere.
In particular u belongs to U, the domain on which F is continuous. Then
F(t_infty,u)=lim F(t_j,u_j)=0 in C^0. There is no assertion that such a sequence,
the uniform bound or the margin delta exists for an arbitrary PDE. No higher
regularity or whole-sequence convergence is proved.

## Equivalent margin and two sharp boundaries
For positive definite H, orthogonal diagonalization gives ||H^{-1}||_op
=1/lambda_min(H), proving the inverse-bound equivalence. Mere positivity does
not suffice: u_j=t_j=1/j, A(u)=u I, F(t,u)=u-t on positive functions gives
uniform Holder bounds and solutions, but the limit u=0 leaves U.
For u_n(x)=n^{-(2+alpha)}cos(2 pi n x_1), second derivatives have sup norm
(2 pi)^2 n^{-alpha}. Using min(2,2 pi n rho) gives uniformly bounded alpha
seminorms, and beta seminorm O(n^{beta-alpha})->0. At x_1=0,y_1=1/(2n),
the alpha quotient of the second derivative is 2(2 pi)^2 2^alpha, not zero.
Hence convergence in C^{2,alpha} cannot replace the proven weaker convergence.
These are elementary classical compactness arguments, not an original PDE result.
