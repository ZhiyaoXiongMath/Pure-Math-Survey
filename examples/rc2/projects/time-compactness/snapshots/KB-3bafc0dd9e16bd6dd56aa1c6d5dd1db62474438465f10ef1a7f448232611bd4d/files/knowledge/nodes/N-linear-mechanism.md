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

Inputs: fixed X compactly embedded in B, B continuously injected into Y; F bounded by M in Lp(X), and uniform translations in Lp(Y). The imported interval-integral criterion is N-simon-criterion.

For every eta>0 there is C_eta such that ||z||B <= eta||z||X + C_eta||z||Y, z in X (Simon Lemma 8, pp.84--85). A direct contradiction proof normalizes a violating sequence to X norm one. Compactness gives a B-convergent subsequence; violation forces its Y norm to zero, hence its B limit is zero, contradicting a positive B lower bound.

For an interior interval I, int_I f is bounded in X by |I|^{1-1/p} M. Thus these integrals are relatively compact in Y, and Simon's criterion makes F relatively compact in Lp(Y) (C(Y) for p=infinity). For a Y-Cauchy subsequence f_n, Minkowski applied to the Ehrling estimate yields

||f_n-f_m||Lp(B) <= 2 eta M + C_eta ||f_n-f_m||Lp(Y).

Given epsilon, first fix eta<epsilon/(4M) when M>0; then choose n,m to make the second term below epsilon/2. Completeness gives strong Lp(B) convergence. When p=infinity the same estimate transfers the uniform convergence; the limit and approximants have the continuous B representatives supplied by Simon's theorem. A proof of that representative issue is imported, not claimed from mere L-infinity equivalence classes.

Output: a route from weak-space time control to strong-space compactness using linear interval averages and an adjustable norm inequality. This is distinct from nonlinear truncation because int K(u) need not equal K(int u).
