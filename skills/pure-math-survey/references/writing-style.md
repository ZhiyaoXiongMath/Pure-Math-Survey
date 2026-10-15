# Mathematical writing and self-contained results

Prefer ordinary explanatory prose around **about 2–3 normal actual typeset
lines** in every mode. Review longer blocks for hidden objects, conditions, estimates or transformations;
improve them when the mathematical argument benefits.
Measure normal font size, line width and margins in the actual PDF, not TeX source lines.
For Markdown/HTML knowledge use an agreed normal reading width, not any narrow window. At a natural mathematical turn, display the decisive object,
condition, equation, transformation, estimate or output and explain its role nearby.
It is not a source-line count, mandatory formula frequency or readability score.

A display should reveal why this quantity matters now and what it supplies next.
Define its major new symbols locally. Do not show long unmotivated formula galleries.
Do not insert decorative equations, force line breaks, shrink typography, fragment a
proof or remove hypotheses to satisfy the target. Complete statements, necessary lists
and continuous proofs may exceed it after considering a better mathematical arrangement.
This is neither an automatic failure for every four-line block nor a formula every three
lines. Bibliographies, code, tables and title/author matter use their own readability checks.
Record actual PDF page/block and source locations for significant readability findings,
repairs and necessary exceptions, with their mathematical purpose and considered alternatives.
Bind observations and repairs to the final PDF SHA-256 and reinspection scope. Inspect
every page; do not claim a blanket theorem/mode exception or an automatic readability
score. Use existing semantic/page findings, not a new approval database.

## Principal statement-self-contained contract

A reader with the declared background must recognize the whole mathematical claim
from the principal statement and immediately adjacent necessary terminology, without
chasing remote numbered formulas. Explicitly identify:

- objects, domain/dimension/rank/boundary/parameter range, fixed data and variables;
- all decisive hypotheses, equations or quantities, quantifiers and constant dependence;
- the exact conclusion and its established, conditional or conjectural status.

“Assume (1.2)–(1.5), then (1.8),” “the above equation,” “standard positivity,” and
“the conclusion of Theorem 2.3” cannot replace essential content. Standard mathematical
concepts need not be redefined from scratch. An unusually long nonstandard definition
may be stated completely and immediately adjacent; the reviewer must explain why no
remote chase is required. The main equation and decisive parameters still need visibility.
Supporting propositions should be locally self-contained; technical lemmas may inherit
explicit subsection data without ambiguous quantifiers. Ordinary proof `\eqref` uses
are not automatically errors.

First repair a deficient canonical statement in the KB, perform mathematical/source
and self-contained readings, freeze a new snapshot, and import its exact bytes. Never
“improve” a generated fragment or silently replace it with a second theorem in the
output. Review neighboring prose too: a correct fragment does not license converting
some to every, semipositive to positive, or conditional to unconditional.

Use English mathematical prose and appropriate established author attributions. Do
not invent decorative names. Examples must calculate, distinguish hypotheses or expose
a real boundary. Primary sources and current templates govern new work. Historical generated samples are not current writing authorities or acceptance evidence. Follow the mode-specific opening and body duties in editions.md; all modes share the same canonical fast/slow knowledge.

## Numbered statement types without descriptive names

Apply to theorem, lemma, proposition, corollary, definition, example, problem, remark, conjecture and custom claim/observation/assumption/question/exercise equivalents. Keep the existing counters, automatic numbering, labels and supported ref/autoref links. Do not use optional descriptive names such as `\begin{definition}[Phase]`, or hide a name in a custom theorem head. Do not convert numbered environments to unnumbered ones. Ordinary unnumbered layout environments gain no artificial numbers.

Write a term inside its definition, or explain a result's purpose/source in adjoining prose. The phrase “Calabi--Yau theorem” in prose and an external locator “Theorem 1.5” are legal. `\begin{proof}[Proof of Theorem~\ref{thm:main}]` names the proof target and remains legal; theoremrecall's “(recalled)” is a status cue. Equation/align/itemize/abstract/figure/table options are outside this rule. The literal scanner checks reachable statement uses and literal newtheorem declarations; unsupported custom heading code needs actual manual PDF review, never a claim that a regex proved its typography safe.

Prefer local self-contained important auxiliaries before their first consuming proof; the opening may announce principal results early. Use real labels and references rather than hand-typed result numbers. After reordering inspect proof headings, above/below/following/previous, PDF links and page references. Use itemize for parallel hypotheses, conclusions or independent routes; keep one continuous argument in connected prose. Paragraph length is a preference, not a reason to fragment a continuous proof. A title names the mathematical problem, without mode/KB/fast/slow development terms.
