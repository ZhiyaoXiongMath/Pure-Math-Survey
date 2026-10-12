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

Inputs are exactly those of N-cone. Let G=sup ||[v]||Lp and D=sup ||v'||Lq(A1), and let C_1 be the inclusion norm A0->A1. Holder and the cone embedding yield a uniform L1(A1) bound C_1 C_0 T^{1-1/p}G. The W11 estimate of N-translations therefore gives a uniform A1 supremum bound

K=T^{-1} C_1 C_0 T^{1-1/p} G + T^{1-1/q} D.

Representatives in A1 are continuous. Cone membership and gauge bounds remain assertions at almost every time; no closedness of the cone is needed.

For R>0 let E_R(v)={t:[v(t)]>R}; then |E_R|<=T^{1-1/p}G/R. Put v_R=v off E_R and zero on E_R. Its values lie in a gauge-bounded set, whose closure Q_R is compact in A0 and hence A1. The uniform A1 amplitude gives

||v-v_R||L1(A1)<=K T^{1-1/p}G/R.

By the finite-net/compact-convex-hull argument in N-truncation, all interval integrals of v_R form a relatively compact set in A1. Uniform approximation gives that property for v. This proves spatial compactness of averages without either addition inside the cone or a compact parametrizing map.

If q=1 and p<infinity, N-translations gives ||tau_h v-v||Lp(A1)<=(2K)^{1-1/p}(hD)^{1/p}. Simon's criterion makes F relatively compact in Lp(A1). If q>1, it gives the uniform estimate h^{1-1/q}D in A1 and Simon's criterion gives relative compactness in C([0,T];A1), regardless of the gauge exponent p.

Take a subsequence Cauchy in the needed weak-space time norm. By N-cone-ehrling and Minkowski,

||v_n-v_m||Lp(A0)<=2 eta G+C_eta||v_n-v_m||Lp(A1).

Choose eta so that the first term is small, then n,m for the second; completeness gives Lp(A0) convergence, including p=infinity. If G=0 all trajectories vanish almost everywhere. At p=infinity, continuous A0 representatives can also be recovered: on a full-measure dense set of times with gauge<=G, the two-point inequality bounds time differences by 2 eta G+C_eta||v(t)-v(s)||A1. Let eta be small and then |t-s| small, and extend by completeness to all times. The A1 representative is unchanged by uniqueness through the injection. The stated theorem requires only L-infinity compactness, so this extra explanation does not strengthen its canonical conclusion.

This is a local reconstruction of the theorem's proof interface. Source Lemma 1 and the statement of Theorem 1 are verified, but the passage following source (2.8), p.6, is not used. The detailed source note records that scoped proof concern. No claim of an original theorem or independent review is made.
