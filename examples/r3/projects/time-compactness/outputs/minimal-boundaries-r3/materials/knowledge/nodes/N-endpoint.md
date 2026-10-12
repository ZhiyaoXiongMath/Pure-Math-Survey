---
{
  "schema_version": "2.0.0",
  "id": "N-endpoint",
  "kind": "example",
  "title": "A bounded L1 derivative does not give supremum compactness",
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
      "source_id": "S-simon",
      "locator": "Corollary 4, pp. 85--86; Proposition 3, p. 94",
      "role": "support",
      "version": "Journal text, Ann. Mat. Pura Appl. 146, pp. 65--96, DOI 10.1007/BF01762360; publisher issue date December 1986 (frequently cited as 1987)"
    }
  ],
  "links": []
}
---

# A bounded L1 derivative does not give supremum compactness

Let T=1, E=R, and n>=3. Define a continuous nonnegative ramp

v_n(t)=0 for 0<=t<=1/2; v_n(t)=n(t-1/2) for 1/2<t<1/2+1/n; v_n(t)=1 afterwards.

Then ||v_n||L-infinity=1 and ||v_n'||L1=1. Pointwise for t!=1/2, v_n tends to the step 1_{(1/2,1]}. No uniformly convergent subsequence exists because a uniform limit of continuous functions is continuous and any subsequence has that discontinuous pointwise limit. For continuous functions the L-infinity essential norm equals the sup norm, so there is no L-infinity-convergent subsequence either. More quantitatively, for m>=2n, at t=1/2+1/m, v_m(t)=1 and v_n(t)=n/m<=1/2; a subsequence with indices doubling is pairwise separated by at least 1/2.

Yet ||v_n-1_{(1/2,1]}||Lp^p=int_0^{1/n}(1-ns)^p ds=1/(n(p+1)) for every finite p. Thus all finite-p convergence coexists with failure at infinity. This is a local elementary example testing Simon's Corollary 4 endpoint (and later the cone theorem), not a new counterexample claim. With cone [0,infinity) and gauge |x| it obeys all spatial cone assumptions. A mere L1 derivative bound cannot replace q>1 at p=infinity.
