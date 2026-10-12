---
{
  "schema_version": "2.0.0",
  "id": "N-M-trace",
  "kind": "mechanism",
  "title": "Tracing Riccati controls radial volume density",
  "facets": [
    "methods",
    "results"
  ],
  "question_ids": [
    "N-Q-local",
    "N-Q-volume"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Section 4, Theorems 4.1 and 4.3, pp. 15–16",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "proof_input",
      "target": "N-M-riccati"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-curvature"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "proof_input",
      "target": "N-M-geometric-inputs"
    }
  ]
}
---

# Tracing Riccati controls radial volume density

## Input and intended output

Fix a unit-speed ray from \(p\) in a smooth \(n\)-manifold, \(n\ge2\). Work on \(0<t<\min\{\tau_p(v),D_k\}\), with \(\operatorname{Ric}(\dot\gamma,\dot\gamma)\ge(n-1)k\). The [Riccati calculation](N-M-riccati.md#symmetry-and-the-riccati-equation) supplies a symmetric \(S\) and \(S'+S^2+\mathcal R=0\).

The output is a bound on relative volume expansion. The [Hessian identification](N-M-geometric-inputs.md#current-vectors-and-the-distance-hessian) also makes it a smooth Laplacian bound, using \(\Delta=\operatorname{div}\operatorname{grad}\).

### Why the trace is the controlled quantity

Put \(m=\operatorname{tr}S\). Taking the trace uses exactly \(\operatorname{tr}\mathcal R=\operatorname{Ric}(\dot\gamma,\dot\gamma)\):
\[
m'+\operatorname{tr}(S^2)+\operatorname{Ric}(\dot\gamma,\dot\gamma)=0.
\]
If \(\sigma_1,\ldots,\sigma_{n-1}\) are the real eigenvalues of \(S\), Cauchy--Schwarz gives
\[
\operatorname{tr}(S^2)=\sum_i\sigma_i^2
\ge\frac{(\sum_i\sigma_i)^2}{n-1}=\frac{m^2}{n-1}.
\]
Consequently \(a=m/(n-1)\) satisfies \(a'+a^2+k\le0\), with \(a=t^{-1}+O(t)\). We have controlled one sum, not every eigenvalue; a Ricci lower bound is not a Hessian operator bound.

### Singular scalar comparison by an integrating factor

The model has \(c_k'+c_k^2+k=0\), \(c_k=t^{-1}+O(t)\). Set \(u=a-c_k\). On the common positive interval,
\[
u'+(a+c_k)u\le0,\qquad
\mu(t)=\exp\!\left(\int_{t_*}^t(a(s)+c_k(s))\,ds\right)>0
\]
for any fixed interior \(t_*\). Since \(a+c_k=2/t+O(t)\), \(\mu(t)\sim Ct^2\) with \(C>0\); also \(u=O(t)\), so \(\mu u\to0\).
\[
(\mu u)'\le0,\qquad
\mu(t)u(t)\le\mu(\varepsilon)u(\varepsilon)\longrightarrow0
\quad(\varepsilon\downarrow0).
\]
Thus \(a\le c_k\), or \(m\le(n-1)c_k\). We did not insert infinite initial values into a regular comparison theorem.

### Normalized density and the small-radius limit

The [Gram calculation](N-D-jacobi.md#from-the-radial-differential-to-volume-density) has established that \(j=\det A>0\) is the geometric polar density. Jacobi's determinant formula now gives
\[
j'=j\,\operatorname{tr}(A^{-1}A')=jm,\qquad
\left(\log\frac{j}{s_k^{n-1}}\right)'=m-(n-1)c_k\le0.
\]
We divide by \(s_k^{n-1}\) because the model calculation gives precisely that density. Its own expansion has been removed, so the quotient records excess or deficient expansion relative to the model.

From \(A=tI+O(t^3)\) and \(s_k=t+O(t^3)\),
\[
\lambda(t,v)=\frac{j(t,v)}{s_k(t)^{n-1}}\longrightarrow1,\qquad
0<\lambda(t,v)\le1,\qquad \partial_t\lambda\le0.
\]
These statements concern each uncut ray. [Cut truncation and angular averaging](N-M-cut-integration.md#zero-extension-and-angular-averaging) turn them into a global ball statement.

### What the hypotheses do not give

Writing \(Q=\operatorname{tr}(S^2)-m^2/(n-1)\ge0\) makes the first failed inference for a Ricci upper bound explicit:
\[
m'=-\frac{m^2}{n-1}-Q-\operatorname{Ric}(\dot\gamma,\dot\gamma).
\]
An upper bound on Ricci does not control the uncontrolled negative term \(-Q\) from below. Therefore it does not reverse this scalar comparison. This is a failure of this inference, not by itself a counterexample to every possible Ricci-upper assertion.

The [product example](N-E-product.md) separately gives a verified failure of replacing sectional hypotheses by a Ricci lower bound in directional and triangle comparisons. Equality throughout an interval in the present comparison forces \(Q=0\), hence \(S\) scalar there; no extra global rigidity is inferred.

Return to the [Ricci-to-volume route](../overview.md#ricci-lower-bounds-to-ball-volume). Its inputs and positive-radius restrictions are the same in the fast and slow readings.
