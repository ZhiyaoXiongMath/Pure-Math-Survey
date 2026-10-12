---
{
  "schema_version": "2.0.0",
  "id": "N-homogeneous-transfer",
  "kind": "relation",
  "title": "A precise overlap between nonlinear maps and cones",
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
      "source_id": "S-barrett-suli",
      "locator": "Section 4, pp. 15--16",
      "role": "support",
      "version": "arXiv:1101.1990v2, submitted 16 April 2011, 17 pages"
    },
    {
      "source_id": "S-maitre",
      "locator": "Theorem 2.1, p. 1726",
      "role": "support",
      "version": "Published IJMMS 2003:27, pp. 1725--1730, DOI 10.1155/S0161171203106175"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-maitre"
    },
    {
      "relation": "proof_input",
      "target": "N-translations"
    },
    {
      "relation": "uses_definition",
      "target": "N-cone-definition"
    },
    {
      "relation": "compares_with",
      "target": "N-cone"
    },
    {
      "relation": "compares_with",
      "target": "N-maitre"
    }
  ]
}
---

# A precise overlap between nonlinear maps and cones

## Canonical statement

```latex
Let $E_1,E_2$ be real Banach spaces, $T>0$, and $\alpha\ge1$.
Suppose $K:E_1\to E_2$ is injective, maps bounded sets into relatively compact sets, and satisfies $K(cu)=c^\alpha K(u)$ for $c\ge0$.
Set $\mathcal M_+=K(E_1)$ and $[v]=\|K^{-1}v\|_{E_1}^{\alpha}$.
Let $1\le p,q\le\infty$, with $q>1$ or with $q=1,p<\infty$.
Suppose a family $F$ of strongly measurable $\mathcal M_+$-valued trajectories has strongly measurable inverse lifts $u=K^{-1}v$, measurable gauges, and
\[
\sup_{v\in F}\bigl(\|[v]\|_{L^p(0,T)}+\|v'\|_{L^q(0,T;E_2)}\bigr)<\infty,
\]
where derivatives are $E_2$-valued distributions.
Then the hypotheses of the compact nonlinear-map theorem stated for $K$, $U=K^{-1}F$, and $V=F$ hold, using any fixed $r>1$ and the target exponent $p$.
Consequently $F$ is relatively compact in $L^p(0,T;E_2)$, and in $C([0,T];E_2)$ when $q>1$.
This reduction concerns the special cone $K(E_1)$ with the same output and derivative space $E_2$; it is not an equivalence for arbitrary cones or arbitrary compact maps.
```

## Interpretation


Proof and normalization. Injectivity and homogeneity give K(0)=0 and positive definiteness of [v]. For c>0, K^{-1}(cv)=c^{1/alpha}K^{-1}v, so the gauge has degree one. Compactness makes C=sup_{||x||<=1}||K(x)|| finite, and scaling gives ||K(x)||<=C||x||^alpha. Gauge-bounded sets map from bounded E1 sets, so the cone compactness and embedding axioms hold.

Write G=sup ||[v]||Lp. Since alpha*p>=1, Holder gives ||u||L1<=T^{1-1/(alpha*p)}G^{1/alpha} (for p=infinity the factor is T). Strong measurability of this inverse lift is explicitly assumed; injectivity alone does not supply it. The gauge bound gives an L1(E2) bound on v, and the derivative bound gives a uniform W11(E2) bound. Thus ||v||L-infinity<=T^{-1}||v||L1+||v'||L1 uniformly, implying every fixed r>1 bound. N-translations gives the target Lp translations for q=1,p finite, and supremum translations for q>1. Apply N-maitre (for q>1 one may apply its p=infinity version).

Barrett--Suli Section 4, pp.15--16, describes this homogeneous-map specialization; these explicit constants and the measurability interface are the local comparison argument. Setting A0=A1=E2 is essential. A weak derivative in some larger A1 cannot simply be renamed an E2 derivative. Conversely, K(x)=x^2 in N-image-only shows Maitre's theorem covers noninjective maps not covered by this inverse-gauge construction. This does not prove that no alternative cone construction exists; it disproves that particular automatic substitution.


## Interface synthesis used by the three reading modes

The linear and nonlinear-map arguments both produce the two inputs of [Simon's criterion](N-simon-criterion.md), but they produce compact interval integrals differently. [N-linear-mechanism](N-linear-mechanism.md) integrates a bounded $X$-valued family directly. [N-truncation](N-truncation.md) first confines nonlinear values to a compact set and then uses a compact closed convex hull. The latter does not require an identity $K(\int u)=\int K(u)$.

The cone route combines these operations: gauge truncation gives compact interval integrals in $A_1$, and a two-point estimate upgrades convergence to $A_0$. Unlike the linear route, it never applies a gauge to a difference. Thus a shared proof interface does not imply that the three sets of hypotheses are equivalent.

The canonical special reduction above can be checked quantitatively. Positive homogeneity gives $K(0)=0$ and
\[
K^{-1}(cv)=c^{1/\alpha}K^{-1}v,\qquad [cv]=c[v],\qquad
\|K(x)\|_{E_2}\le C\|x\|_{E_1}^{\alpha}.
\]
For $G=\sup\|[v]\|_{L^p}$, the strongly measurable lift satisfies
\[
\|K^{-1}v\|_{L^1(E_1)}\le T^{1-1/(\alpha p)}G^{1/\alpha},
\]
with factor $T$ when $p=\infty$. The derivative is in $E_2$, so the amplitude and translation estimates apply there. Maitre's hypotheses follow for any fixed $r>1$. Removing injectivity prevents this particular inverse-gauge construction; removing the matching derivative space prevents this particular reduction. Neither observation proves nonexistence of every alternative construction.
