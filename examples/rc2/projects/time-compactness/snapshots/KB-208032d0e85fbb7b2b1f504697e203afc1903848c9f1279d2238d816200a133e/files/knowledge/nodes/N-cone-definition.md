---
{
  "schema_version": "2.0.0",
  "id": "N-cone-definition",
  "kind": "definition",
  "title": "A seminormed nonnegative cone",
  "facets": [
    "foundations",
    "boundaries"
  ],
  "question_ids": [
    "N-question"
  ],
  "mathematical_status": "established",
  "origin": "primary_source",
  "sources": [
    {
      "source_id": "S-barrett-suli",
      "locator": "Section 1, pp. 2--3, equation (1.1) and conditions (i)--(ii)",
      "role": "support",
      "version": "arXiv:1101.1990v2, submitted 16 April 2011, 17 pages"
    }
  ],
  "links": []
}
---

# A seminormed nonnegative cone

## Canonical statement

```latex
Let $A$ be a real Banach space. A seminormed nonnegative cone in $A$ is a subset $\mathcal M_+\subset A$ equipped with a function $[\cdot]_{\mathcal M_+}:\mathcal M_+\to[0,\infty)$ such that, for all $z\in\mathcal M_+$ and $c\ge0$,
\[
c z\in\mathcal M_+,
\qquad [z]_{\mathcal M_+}=0\ \Longleftrightarrow\ z=0,
\qquad [cz]_{\mathcal M_+}=c[z]_{\mathcal M_+}.
\]
The embedding into $A$ is continuous if $\|z\|_A\le C[z]_{\mathcal M_+}$ for one fixed $C$ and all $z$ in the cone.
It is compact if it is continuous and every sequence with bounded gauge has a subsequence converging in $A$.
Neither additivity of the cone nor a triangle inequality for its gauge is required.
```

## Interpretation


Positive homogeneity concerns scalar multiplication inherited from the ambient space. Differences can leave the cone, so an expression [u-v] is not generally defined. Strong measurability of trajectories and measurability of the gauge are imposed in the trajectory theorem, rather than inferred from these axioms.
