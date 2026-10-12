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

## Fast route

The time-control input for [the nonlinear map](N-maitre.md) and [cone](N-cone.md) routes can be obtained from derivatives. A derivative in the output space supplies a uniform amplitude and finite-$p$ translations; a derivative exponent above one also supplies a supremum modulus.

## Slow route: amplitude and finite exponents

Let $v\in W^{1,1}(0,T;E)$. Choose $s$ with $\|v(s)\|_E\le T^{-1}\|v\|_{L^1(E)}+\varepsilon$. The fundamental theorem gives
\[
\|v\|_{L^\infty(E)}\le T^{-1}\|v\|_{L^1(E)}+\|v'\|_{L^1(E)}
\]
after letting $\varepsilon\downarrow0$. Thus bounds on the two right-hand terms supply a uniform amplitude $K_0$.

If $\|v'\|_{L^1(E)}\le D$, Fubini gives
\[
\int_0^{T-h}\|v(t+h)-v(t)\|_E\,dt
\le\int_0^{T-h}\int_t^{t+h}\|v'(s)\|_E\,ds\,dt\le hD.
\]
Since every difference is bounded by $2K_0$, for $1\le p<\infty$,
\[
\|\tau_hv-v\|_{L^p(E)}\le(2K_0)^{1-1/p}(hD)^{1/p}.
\]
This exponent is $h^{1/p}$, not $h$, when only an $L^1$ derivative bound is known.

## Slow route: the supremum endpoint

If $\|v'\|_{L^q(E)}\le D_q$ with $q>1$, Hölder on $(t,t+h)$ gives
\[
\|v(t+h)-v(t)\|_E\le h^{1-1/q}D_q.
\]
For $q=\infty$, take $1/q=0$. At $q=1$ the exponent vanishes, so this estimate gives no uniform small modulus. The [ramp example](N-endpoint.md) proves that the missing endpoint conclusion can actually fail.

## Where the output is used

[N-cone-mechanism](N-cone-mechanism.md) uses these estimates in $E=A_1$. [N-homogeneous-transfer](N-homogeneous-transfer.md) uses them in $E=E_2$. A derivative controlled only in a larger ambient space cannot be substituted into the $E_2$ estimate without additional work.
