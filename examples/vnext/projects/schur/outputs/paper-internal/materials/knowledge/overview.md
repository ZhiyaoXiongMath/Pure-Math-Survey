# Eliminating a coupled quadratic form

The problem is not to memorize a new matrix, but to remove the cross term
from Q(x,y). The reader already knows scalar square completion. Its matrix analogue
chooses z=x+A^{-1}By, because this cancels exactly the coefficient B in the cross term.
The residual form is y^T S y with S=C-B^T A^{-1}B. See [[N-square]], “Square completion
and inverse map,” for the expansion, and [[N-inverse]] for why nonzero pairs remain nonzero.

These two inputs are joint: the identity alone does not establish positivity unless
the change is invertible and the two remaining forms have the needed signs.
[[N-main]], “Both directions,” proves sufficiency and the special test x=-A^{-1}By
needed for necessity. Positivity of A supplies both its inverse and the correct sign.

A related question asks what remains after minimizing over x with y fixed.
The same identity answers min_x Q=y^T S y. A second description uses congruence,
T^T M T=diag(A,S); [[N-comparison]], “Congruence and minimization,” shows that this
is the same elimination in new coordinates, not a stronger criterion. The project
therefore has several related questions and viewpoints, not just an article outline.

For A=-1,B=0,C=1 the residual S is positive but M is indefinite. [[N-boundary]]
explains this boundary and the singular case excluded by the inverse. No pseudoinverse
extension or originality claim is made. Individual outputs choose their own points and
proof detail; this overview is not Minimal's third section.
