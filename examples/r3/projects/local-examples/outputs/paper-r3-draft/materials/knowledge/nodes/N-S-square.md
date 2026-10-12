---
{
  "schema_version": "2.0.0",
  "id": "N-S-square",
  "kind": "mechanism",
  "title": "Eliminating the cross term",
  "facets": [
    "foundations",
    "results",
    "methods",
    "boundaries"
  ],
  "question_ids": [
    "N-Q-schur"
  ],
  "mathematical_status": "established",
  "origin": "local_derivation",
  "sources": [
    {
      "source_id": "S-Boyd",
      "locator": "Appendix A.5.5, pp.650-651",
      "role": "support"
    }
  ],
  "links": []
}
---

# Eliminating the cross term

## Fast route
With A symmetric and invertible, use z=x+A^{-1}By. This choice makes Az=Ax+By, so expansion reproduces the original cross term. The remainder is S=C-B^TA^{-1}B. It is the form left after optimizing x only when A>0.

## Derivation
Since A^{-1} is symmetric,
\[
z^TAz=x^TAx+2x^TBy+y^TB^TA^{-1}By.
\]
Consequently Q(x,y)=z^TAz+y^TSy. The inverse coordinate change is x=z-A^{-1}By, with y unchanged. It is a bijection and sends only (0,0) to (0,0). For A>0, z^TAz is nonnegative and vanishes exactly at z=0. Thus the unique minimizer for fixed y is x=-A^{-1}By and its value is y^TSy. This supplies both the criterion and its first use, rather than assuming a Schur rule.
