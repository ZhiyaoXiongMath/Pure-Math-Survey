# Historical v1 reference

This is retained legacy documentation. Native v2 follows ../records-and-delivery.md and the current SKILL.md.

# Worked exposition examples

These examples demonstrate writing and typesetting, not source evidence for a survey. The elementary quadratic example is proved in the [compilable fixture](../../assets/exposition-examples/exposition-smoke.tex). Do not import it into an unrelated mathematical review. See [writing style](writing-style.md) for the governing rules.

## Delete announcements, preserve mathematics

Delete: "We now turn to the assumptions of the theorem, which will play an important role in what follows." The heading and theorem already do this work.

Keep a real inference, preferably in its direct mathematical form:

```latex
If $Av=0$, then $v^{\mathsf T}Av=0$.
Positive definiteness gives $v=0$, so $A$ is invertible.
```

This is a short proof step, not a trivial editorial transition. A section can start with it without a sentence announcing that an argument is about to begin.

## A compact theorem with listed hypotheses

Do not put symmetry, positivity, the formula for the minimizer, a minimum value, an example and discussion of the method in one long theorem sentence. Give the theorem's main answer first:

```latex
\begin{theorem}\label{thm:quadratic}
Let $m\geq 1$, $A\in\mathbb R^{m\times m}$ and $b\in\mathbb R^m$.
Assume both of the following:
\begin{itemize}
\item $A=A^{\mathsf T}$;
\item $v^{\mathsf T}Av>0$ for every $v\in\mathbb R^m\setminus\{0\}$.
\end{itemize}
Define
\[
Q(x)=\frac12 x^{\mathsf T}Ax-b^{\mathsf T}x,
\qquad x\in\mathbb R^m.
\]
Then $Q$ has the unique minimizer $x_*=A^{-1}b$ on $\mathbb R^m$.
\end{theorem}
```

The two hypotheses are jointly required; "Assume both" states their logical relationship. The number of list items is incidental. A one-condition statement may use an ordinary sentence. Use `enumerate` instead when referring to conditions as (i), (ii), or listing equivalent statements or alternative cases; specify which logic applies.

Place secondary formulas after the theorem, with their applicability clear:

```latex
With the hypotheses of Theorem~\ref{thm:quadratic}, the minimum is
\[
Q(x_*)=-\frac12 b^{\mathsf T}A^{-1}b.
\]
```

These are not unsupported extra assertions. The fixture proves invertibility and the identity

```latex
\[
Q(x)-Q(A^{-1}b)
=\frac12(x-A^{-1}b)^{\mathsf T}A(x-A^{-1}b).
\]
```

The identity proves the theorem and its secondary minimum-value formula. In a survey, cite the controlling source or give the required derivation. Do not move a necessary hypothesis outside a theorem, silently weaken a registered claim, or split an essential equivalence into disconnected results merely to shorten a statement.

## Definition-and-theorem introduction

The introduction can use this structure directly:

```latex
\section{Introduction}
% State the setting and central question, using a display when clearer.
\begin{definition}
% Define the specialized object needed for the principal theorem.
\end{definition}
\begin{theorem}
% State the local setting, complete necessary hypotheses and core conclusion.
\end{theorem}
% A further definition or theorem may follow immediately.
% Add a sentence only for a nontrivial relation or necessary clarification.
```

The comments above are drafting instructions, not publishable content. No section roadmap or transition paragraph is needed merely to separate the environments. The completed quadratic fixture illustrates the form with actual mathematics. Select and order principal results by the central question rather than copying an exhaustive source list.

## Canonical repetition without label conflicts

Save the shared mathematical body in `canonical/quadratic.tex`, without a theorem wrapper or any `\label`. Lists and formulas stay in this body. The primary statement is:

```latex
\begin{theorem}\label{thm:quadratic}
\input{canonical/quadratic.tex}
\end{theorem}
```

A later section that benefits from the full local setting may use:

```latex
\begin{theoremrecall}{thm:quadratic}
\input{canonical/quadratic.tex}
\end{theoremrecall}
```

The shared style prints the original theorem number followed by "(recalled)", without advancing the theorem counter. Do not put a new `\label` inside the recall; refer to the primary label. The publication map still has one primary location for this result in that document. The validator accepts both full-body inputs but still rejects duplicate labels, missing bodies and body inputs at omitted or reference-only placements.

This is useful repetition, not a second theorem with a new mathematical identity. Repeating a short setting or needed definition is also allowed. Delete an adjacent word-for-word prose translation only when it adds no understanding. No recall quota, approval step or extra audit ledger is required. For a lemma, proposition or Problem, use the appropriate locally defined recall wrapper or a precise reference with usable assumptions rather than mislabelling it as a theorem.

## Naming results is not stating conclusions

Bad introduction: “We discuss minimization and gradient descent; see the main results below.” Names and section pointers provide no usable answer.

For the example's declared task, two independent conclusions are required: the unique point minimizing the positive-definite quadratic and the convergence of the iteration that constructs it. After local definitions, the first statement gives `x_*=A^{-1}b`. The second gives, for symmetric positive-definite `A`, arbitrary `x_0` and `0<\tau<2/\lambda_{\max}(A)`,

```latex
x_{j+1}=x_j-\tau(Ax_j-b),\qquad
\|x_j-x_*\|_2\le q^j\|x_0-x_*\|_2,\qquad
q=\max_{\lambda\in\operatorname{Spec}(A)}|1-\tau\lambda|<1.
```

See the complete assumptions, separate theorem bodies and proofs in [the elementary example](../../assets/exposition-examples/exposition-smoke.tex). Naming both theorems fails; fully stating only the minimizer also fails this two-output scope. A genuinely one-result article can pass without inventing a second result. Copying the example's number of theorems into every survey is not the rule.

## Structural identity before the equation

In the dHYM reference, fixed data and eigenvalues precede the phase identity, which precedes the equation with its unknown. Compatibility then follows from the positive integral. The reference's equations (1.1)–(1.6) demonstrate the dependency; they are not optional prose added after an unexplained equation. Consult [the frozen reference](../../assets/reference-samples/dhym-v6/README.md) for its actual mathematical definitions and source scope; do not transfer its subject-specific notation blindly.

A comparison between general Kähler ray conditions and projective endpoint conditions must state the actual implication and the assumptions that make it true. The reference's Section 5 supplies the polynomial expansion and hyperplane-section mechanism. “Projectivity provides a connection” does not explain that mechanism. No fixed paragraph formula is required when the mathematics already orders itself.

## Organizing question and limited progress

Bad: “There are two interesting local flow and divisor problems.” That can omit the organizing existence/stability question even when the local questions are legitimate.

Better: identify the organizing question with a precise source, separate existence from the chosen flow assertion, state a verified limited positive result and the applicable counterexample, then locate the local questions within the remaining range. A neighboring conjecture can supply motivation but cannot substitute for discovering the selected field's own gap. Historical sample discussions are not evidence of complete frontier coverage. Compare the strongest known answer with the effective, structural or boundary question that remains, and verify that question outside the initially selected bibliography.
