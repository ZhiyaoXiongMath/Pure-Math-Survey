---
{
  "schema_version": "2.0.0",
  "id": "N-M-splitting",
  "kind": "mechanism",
  "title": "Opposite Busemann functions become a parallel coordinate",
  "facets": [
    "methods"
  ],
  "question_ids": [
    "N-Q-global"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-Heintze-1984",
      "locator": "Sections 2\u20134, pp. 142\u2013148; Section 5 Remark 1, p. 148; Section 6, p. 150",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-M-support"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-line"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-support"
    }
  ]
}
---

# Opposite Busemann functions become a parallel coordinate

## Explanation and evidence

For the two rays of a line, b^++b^-<=0 by the triangle inequality and equality holds along the line. Smooth lower supports with Laplacian lower bounds tending to zero give subharmonicity in the support sense under Ric>=0. The Hopf–Calabi maximum principle makes b^++b^-=0.

Use the PDE route explicitly indicated in EH1984 §5 Remark 1, rather than copying its problematic finite-radius trace estimate. Local harmonic replacements and comparison show each b is weakly subharmonic; since b^+=-b^-, b=b^+ is harmonic, hence smooth by elliptic regularity. Its asymptotic rays show |grad b|=1. These existence/regularity and asymptote results are precise imported inputs. Bochner's identity then gives
\[
0=\tfrac12\Delta|\nabla b|^2=|\nabla^2b|^2+
\langle\nabla b,\nabla\Delta b\rangle+\operatorname{Ric}(\nabla b,\nabla b),
\]
so Hess b=0. The unit parallel field grad b is complete and Killing. Every flow line meets N={b=0} exactly once, because b changes with unit speed. Its flow defines the global product isometry N×R→M.

For an asymptotic ray sigma from z, a correctly signed lower support is h_r(x)=b(z)+r-d(x,sigma(r)), since b(sigma(r))=b(z)+r and b is 1-Lipschitz. At the contact point z, the support is smooth near z and its Laplacian is at least -(n-1)/r. At another regular point x the denominator is d(x,sigma(r)); it cannot be replaced by r. The standard asymptotic-ray support construction supplies smoothness near z. The opposite sign printed on EH1984 p.143 fails even on a line. This node records a mechanism with imported analytic inputs, not a self-contained proof of elliptic regularity.
