---
{
  "schema_version": "2.0.0",
  "id": "N-L-connection",
  "kind": "mechanism",
  "title": "Integrating curvature and retaining the trace",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-lich"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Datar",
      "locator": "Lemma 29.2.3 and lower-bound proof, pp.218-219",
      "role": "support"
    }
  ],
  "links": [
    {
      "target": "N-L-inputs",
      "relation": "proof_input"
    }
  ]
}
---

# Integrating curvature and retaining the trace

## Fast route
Bochner relates the Hessian and Ricci terms to an eigenvalue times gradient energy. The Hessian trace contains the eigenfunction itself, so dropping the Hessian wastes the extra factor m/(m-1). Keep its trace using Cauchy-Schwarz, then compare both expressions for gradient energy.

## Integration and trace
For smooth h,k on a closed manifold, integrate div(h grad k)=<grad h,grad k>-h Delta k. The divergence integral is zero, hence
\[
\int_M\langle\nabla h,\nabla k\rangle\,dV_g=\int_M h\Delta k\,dV_g.
\]
In particular integral Delta q=0 for smooth q. A density version of divergence integration works without an orientability assumption. Substitute Delta f=lambda f in Bochner and integrate:
\[
\lambda\int_M|\nabla f|^2=\int_M(|\Hess f|^2+\Ric(\nabla f,\nabla f)),
\qquad\int_M|\nabla f|^2=\lambda\int_M f^2.
\]
At a point take a g-orthonormal frame and write H_ab=Hess f(e_a,e_b). Cauchy-Schwarz on the m diagonal entries gives
\[
(\tr H)^2=(\sum_a H_{aa})^2\leq m\sum_a H_{aa}^2\leq m\sum_{a,b}H_{ab}^2=m|H|^2.
\]
Since tr H=-Delta f, |Hess f|^2>=(Delta f)^2/m. These are actual usable identities; their consumption is the [closing estimate](N-L-main.md#closing-the-estimate).
