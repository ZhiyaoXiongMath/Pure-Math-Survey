---
{
  "schema_version": "2.0.0",
  "id": "N-cone-mechanism",
  "kind": "mechanism",
  "title": "Gauge truncation, weak-space compactness and a two-point upgrade",
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
      "source_id": "S-barrett-suli",
      "locator": "Lemma 1, pp. 4--5; Theorem 1 proof, pp. 12--13, equation (2.22)",
      "role": "support",
      "version": "arXiv:1101.1990v2, submitted 16 April 2011, 17 pages"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-cone-ehrling"
    },
    {
      "relation": "proof_input",
      "target": "N-simon-criterion"
    },
    {
      "relation": "proof_input",
      "target": "N-translations"
    },
    {
      "relation": "proof_input",
      "target": "N-truncation"
    }
  ]
}
---

# Gauge truncation, weak-space compactness and a two-point upgrade

## Fast route and exact inputs

Use the complete hypotheses of [the cone theorem](N-cone.md). Let $C_1$ be the norm of $A_0\hookrightarrow A_1$, and put
\[
G=\sup_{v\in F}\|[v]\|_{L^p},\qquad D=\sup_{v\in F}\|v'\|_{L^q(A_1)}.
\]
First construct compact interval integrals in $A_1$ by cutting off large gauge values. Then use translations and [Simon's criterion](N-simon-criterion.md) in $A_1$. Finally [two-point Ehrling](N-cone-ehrling.md) transfers the Cauchy subsequence to $A_0$.

## Slow route: bounded amplitude in the weaker space

Hölder and the cone embedding give
\[
\|v\|_{L^1(A_1)}\le C_1C_0T^{1-1/p}G.
\]
The [fundamental-theorem estimate](N-translations.md) therefore supplies
\[
\|v\|_{L^\infty(A_1)}\le K_1:=C_1C_0T^{-1/p}G+T^{1-1/q}D.
\]
The $A_1$ representatives are continuous. Cone membership and the gauge estimate are still asserted only almost everywhere; no closedness of the cone is assumed.

## Slow route: compact interval integrals

Set $E_R(v)=\{t:[v(t)]>R\}$, and let $v_R=v$ off $E_R$ and zero on $E_R$. Markov and the amplitude estimate give
\[
|E_R(v)|\le T^{1-1/p}G/R,\qquad
\|v-v_R\|_{L^1(A_1)}\le K_1T^{1-1/p}G/R.
\]
All values of $v_R$ lie in one gauge-bounded set, with compact closure in $A_0$ and hence $A_1$. The [finite-net argument](N-truncation.md) makes their interval integrals relatively compact in $A_1$. Choose $R$ first, then a finite net, to obtain the same conclusion for the untruncated family.

## Slow route: translations and the final upgrade

For $q=1$ and $p<\infty$, [N-translations](N-translations.md) yields
\[
\|\tau_hv-v\|_{L^p(A_1)}\le(2K_1)^{1-1/p}(hD)^{1/p}.
\]
For $q>1$ it yields the supremum modulus $h^{1-1/q}D$. Simon's criterion gives a subsequence Cauchy in $L^p(A_1)$ in every allowed case, using its supremum version when $q>1$.

Apply two-point Ehrling at almost every time, then Minkowski:
\[
\|v_n-v_m\|_{L^p(A_0)}\le 2\eta G+C_\eta\|v_n-v_m\|_{L^p(A_1)}.
\]
If $G>0$, choose $\eta<\varepsilon/(4G)$ and then $n,m$ to make the second term below $\varepsilon/2$. If $G=0$, all trajectories vanish. Completeness proves $L^p(A_0)$ convergence, including $p=\infty$ when $q>1$.

At $p=\infty$, a full-measure dense set has $[v(t)]\le G$. Two-point Ehrling bounds time differences there by $2\eta G+C_\eta\|v(t)-v(s)\|_{A_1}$. Choose $\eta$, then $|t-s|$, and extend by completeness to obtain continuous $A_0$ representatives. Injectivity identifies these with the existing $A_1$ representatives. The canonical theorem only asserts $L^\infty$ compactness.

## Source scope and consumption

This proves the selected cone theorem without addition in the cone or a compact parametrizing map. It uses the verified source Lemma 1 and final upgrade (2.22), but does not rely on the unresolved time-dependent subsequence passage after source (2.8), p. 6. That concern is about the cited proof passage, not a claim that the theorem is false.
