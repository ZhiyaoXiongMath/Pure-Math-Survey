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

Weak convergence alone does not pass squares. On the same circle sin(nx) converges weakly to zero in L^2 (Fourier coefficients of L^2 test functions tend to zero), but the integrals of sin^2(nx) equal pi. Its squares cannot converge weakly to zero. This failure model is separate from the strong Holder theorem and never invoked to justify its nonlinear step.

For the local/global distinction, choose a nonzero smooth compactly supported eta on R and u_j(x)=eta(x-j). On each fixed compact set u_j eventually vanishes, but its global sup norm stays ||eta||_infty. Local convergence therefore supplies no global uniform convergence. Each example identifies the first missing input instead of claiming the entire theorem generalizes.
