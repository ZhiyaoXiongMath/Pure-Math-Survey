---
{
  "schema_version": "2.0.0",
  "id": "N-image-only",
  "kind": "example",
  "title": "Compact nonlinear images do not recover the input",
  "facets": [
    "boundaries"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-maitre",
      "locator": "Theorem 2.1 and Remark 2.2(3), p. 1726",
      "role": "support",
      "version": "Published IJMMS 2003:27, pp. 1725--1730, DOI 10.1155/S0161171203106175"
    }
  ],
  "links": []
}
---

# Compact nonlinear images do not recover the input

On (0,1), let u_n(t)=(-1)^{floor(2^n t)} (values at dyadic endpoints do not matter), E1=E2=R and K(x)=x^2. Bounded subsets of R have relatively compact K-images. Every u_n has L1 norm one, but for m>n the functions differ on a set of measure 1/2. Hence ||u_n-u_m||L1=1, and the input family has no L1-convergent subsequence. Nevertheless K(u_n)=1 identically, so the output family is a singleton, satisfies every Lr bound and has zero translations. This directly checks why Maitre's conclusion is for v=K(u), with no conclusion for u. K is not injective; replacing K by a formal inverse is invalid.
