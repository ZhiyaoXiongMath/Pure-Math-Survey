---
{
  "schema_version": "2.0.0",
  "id": "N-E-cylinder",
  "kind": "example",
  "title": "Flat quotients separate cut points from conjugate points",
  "facets": [
    "boundaries",
    "foundations"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume",
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-distance"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    }
  ]
}
---

# Flat quotients separate cut points from conjugate points

## Explanation and evidence

On the flat cylinder M=S^1_a×R with circle radius a, use a lifted angular arclength coordinate theta and coordinate z. From p=(0,0),
\[
r([\theta],z)=\min_{m\in\mathbb Z}\sqrt{(\theta+2\pi a m)^2+z^2}.
\]
At theta=pi a there are two minimizing lifts. At z=0 the one-sided angular derivatives are +1 and -1, so r is not differentiable. Yet every normal Jacobi field with J(0)=0 is t times a parallel vector, and there are no conjugate points. The cut time in the circle direction is pi a; exp_p is a covering, not injective.

This single calculation tests both the regular-distance hypothesis of Hessian comparison and the simple-connectivity hypothesis for the diffeomorphism conclusion in Cartan–Hadamard. It does not refute either correctly stated theorem.
