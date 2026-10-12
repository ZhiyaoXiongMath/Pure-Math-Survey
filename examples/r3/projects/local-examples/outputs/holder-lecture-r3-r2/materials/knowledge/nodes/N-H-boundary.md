---
{
  "schema_version": "2.0.0",
  "id": "N-H-boundary",
  "kind": "example",
  "title": "What the compactness argument does not preserve",
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
      "target": "N-H-main",
      "relation": "explains"
    }
  ]
}
---

# What the compactness argument does not preserve

## Failure models
On a fixed compact M let A(u)=u I_r, U={u>0}, F(t,u)=u-t, t_j=1/j and u_j=1/j. All Holder norms are uniformly bounded and F(t_j,u_j)=0, yet u_*=0 leaves U. The missing assumption is a single delta>0 independent of j, not continuity of F.

On the circle R/(2pi Z), u_n(x)=n^{-2-alpha}cos(nx) has uniformly bounded C^{2,alpha} norm. The second derivative is -n^{-alpha}cos(nx); using min(2,n|h|) bounds its alpha seminorm uniformly. At x=0,y=pi/n the quotient is 2/pi^alpha, so it does not tend to zero. Lower derivatives and u_n'' converge uniformly to zero. Thus no C^{2,alpha}-convergent subsequence exists, while C^{2,beta} convergence does hold. Fixed cutoffs preserve this conclusion.

## Weak convergence and squaring

Use the real Hilbert space $L^2(0,2\pi;\mathbb R)$ with inner product
$\langle f,g\rangle=\int_0^{2\pi}f(x)g(x)\,dx$ and norm
$\|g\|_2^2=\langle g,g\rangle$. By definition, $f_n\rightharpoonup0$
weakly in this space means $\int_0^{2\pi}f_n g\,dx\to0$ for every
$g\in L^2(0,2\pi;\mathbb R)$.

For positive integers $n$, put $e_n(x)=\sin(nx)/\sqrt\pi$. The identity
$2\sin(nx)\sin(mx)=\cos((n-m)x)-\cos((n+m)x)$ gives
$\langle e_n,e_m\rangle=0$ when $n\ne m$ and $1$ when $n=m$.
Thus this sequence is orthonormal; no completeness of a Fourier system is needed.

Fix any $g\in L^2(0,2\pi;\mathbb R)$ and put $a_n=\langle g,e_n\rangle$.
Expanding the squared norm of a finite sum using orthonormality gives, for every $N$,
$$
0\leq\left\|g-\sum_{n=1}^N a_ne_n\right\|_2^2
=\|g\|_2^2-\sum_{n=1}^N|a_n|^2.
$$
The nonnegative partial sums on the right are bounded by $\|g\|_2^2$,
so $a_n\to0$. Consequently
$\int_0^{2\pi}\sin(nx)g(x)\,dx=\sqrt\pi\,a_n\to0$.
This proves the asserted weak convergence of $\sin(nx)$ for every $L^2$ test function,
without invoking an unproved Fourier-coefficient theorem.

The squares are also in this $L^2$ space. The constant test function $g=1$ belongs
to it, but $\int_0^{2\pi}\sin^2(nx)\,dx=\pi$ for every $n$.
Thus $\sin^2(nx)$ does not converge weakly to zero. This failure model is separate
from the strong Holder theorem and never justifies its nonlinear passage.

## Local versus global

For the local/global distinction, choose a nonzero smooth compactly supported eta on R and u_j(x)=eta(x-j). On each fixed compact set u_j eventually vanishes, but its global sup norm stays ||eta||_infty. Local convergence therefore supplies no global uniform convergence. Each example identifies the first missing input instead of claiming the entire theorem generalizes.
