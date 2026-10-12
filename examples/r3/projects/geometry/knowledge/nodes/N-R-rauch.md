---
{
  "schema_version": "2.0.0",
  "id": "N-R-rauch",
  "kind": "result",
  "title": "Rauch comparison against a constant-curvature model",
  "facets": [
    "results",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-local"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Eschenburg-1994",
      "locator": "Rauch I, p. 14; Theorems 3.1 and 3.3, pp. 12\u201313",
      "role": "support"
    }
  ],
  "links": [
    {
      "relation": "uses_definition",
      "target": "N-D-jacobi"
    },
    {
      "relation": "uses_definition",
      "target": "N-D-model"
    },
    {
      "relation": "explained_by",
      "target": "N-M-riccati"
    },
    {
      "relation": "proof_input",
      "target": "N-M-riccati"
    }
  ]
}
---

# Rauch comparison against a constant-curvature model

## Canonical statement

```latex
Let \((M^n,g)\) be a smooth Riemannian manifold, \(n\ge2\), and \(\gamma:[0,T]\to M\) a unit speed geodesic. Let \(J\) be a normal Jacobi field with \(J(0)=0\) and \(|D_tJ(0)|=a>0\). For \(k\in\mathbb R\) let \(s\) solve
\(s''+ks=0,\ s(0)=0,\ s'(0)=1\), and set \(D_k=\pi/\sqrt{k}\) if \(k>0\) and \(D_k=+\infty\) otherwise.
If every two-plane containing \(\dot\gamma(t)\) has sectional curvature at most \(k\) for all \(t\in[0,T]\), then
\[
|J(t)|\ge a\,s(t)\qquad(0<t<\min\{T,D_k\}).
\]
If instead all those sectional curvatures are at least \(k\), and \(\gamma\) has no point conjugate to \(\gamma(0)\) in \((0,T]\), then
\[
|J(t)|\le a\,s(t)\qquad(0<t<\min\{T,D_k\}).
\]
```

## Explanation and evidence

This deliberately records a safe constant-model version, rather than all variable-curvature or focal versions. In the sec>=k case the interval is restricted before the first conjugate point of the actual geodesic. In the sec<=k case the model has no conjugate point before D_k and comparison gives the lower bound there. Cut points do not stop a Jacobi field comparison along a specified geodesic; they stop its interpretation as the globally smooth distance Hessian. Historical Rauch 1951 is provenance only until its original text is checked.

## Reading and first use

The [fast sectional route](../overview.md#sectional-bounds-to-jacobi-length-and-hessian) explains the comparison experiment. The [logarithmic-length calculation](N-M-riccati.md#jacobi-length-and-exponential-map-use) supplies the proof transition and the upper-curvature continuation argument. For \(k=0\), the lower-sectional-curvature case gives \(|J(t)|\le at\) on its stated interval. Interpreting \(J\) as an angular derivative gives an actual sphere-curve length estimate there. The model zero and the actual conjugate restriction must still be checked separately.
