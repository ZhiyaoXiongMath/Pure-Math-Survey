---
{
  "schema_version": "2.0.0",
  "id": "N-translations",
  "kind": "mechanism",
  "title": "Derivative bounds and the exponent of time translations",
  "facets": [
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
      "source_id": "S-simon",
      "locator": "Lemma 4, pp. 77--78; Corollary 4, p. 85",
      "role": "support",
      "version": "Journal text, Ann. Mat. Pura Appl. 146, pp. 65--96, DOI 10.1007/BF01762360; publisher issue date December 1986 (frequently cited as 1987)"
    },
    {
      "source_id": "S-maitre",
      "locator": "Corollary 2.4, p. 1730",
      "role": "support",
      "version": "Published IJMMS 2003:27, pp. 1725--1730, DOI 10.1155/S0161171203106175"
    }
  ],
  "links": []
}
---

# Derivative bounds and the exponent of time translations

For v in W^{1,1}(0,T;E), choose a time s with ||v(s)||E no greater than T^{-1}||v||L1 plus an arbitrarily small error. The fundamental theorem gives

||v||L-infinity(E) <= T^{-1}||v||L1(E)+||v'||L1(E).

If a family has this bound K and derivative L1 bound D, Fubini gives ||tau_h v-v||L1(0,T-h;E)<=hD. Since pointwise differences are <=2K, for each finite p>=1,

||tau_h v-v||Lp <= (2K)^{1-1/p}(hD)^{1/p}.

When v' is bounded by D_q in Lq(E), q>1, Holder on (t,t+h) gives ||tau_h v-v||L-infinity <= h^{1-1/q}D_q, with exponent one for q=infinity. These estimates show why derivatives measured in the output space give Maitre's time hypothesis. The finite-p interpolation bound must not be replaced with a linear-in-h bound at p>1. The first estimate alone has no uniform modulus in the supremum norm, as N-endpoint calculates.
