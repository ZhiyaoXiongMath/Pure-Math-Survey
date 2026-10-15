"""PR04 literal policy tests and finite synthetic reading cases.

Compilation is real; semantic mutations are prompts for independent review, not
machine verdicts about provenance, reading order or mathematical correctness.
"""
from __future__ import annotations
import os
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

import test_vnext as v
from test_v2 import SKILL
from survey_core.exports import prepare_output, validate_structure
from survey_core.profiles import POLICY, VIEW_TASKS
from survey_core.structure import STATEMENTS, statement_title_errors
from survey_core.tex import inspect_tex, validate_locations

FIXTURE = Path(__file__).parent/'fixtures/pr04-editorial'
OPENING = ('The following borrowed statement is Synthetic Note A,\n'
           'version v1, Theorem~1.1~\\cite[Theorem~1.1]{note-a}.')
COMPOSITE = ('The next consequence combines Synthetic Note A, version v1,\n'
             'Theorem~1.1~\\cite[Theorem~1.1]{note-a} with Synthetic Note B, version v2,\n'
             'Theorem~2.1~\\cite[Theorem~2.1]{note-b}. Neither source alone states this\n'
             'composite formulation.')


def semantic_cases(text):
    """Exact reviewable edits; no citation regex pretends to judge support."""
    assert OPENING in text and COMPOSITE in text
    return {
        'bibliography_only': text.replace(OPENING, 'Consider the following claim.'),
        'wrong_version': text.replace(OPENING, OPENING.replace('version v1', 'version v0')),
        'unsupported_hypothesis': text.replace('For real $x$ and $\\varepsilon>0$',
            'For real $x$ and $\\varepsilon\\geq0$').replace('given strictly\npositive $\\varepsilon$',
            'given nonnegative $\\varepsilon$'),
        'missing_composite_input': text.replace(COMPOSITE,
            'This is a local consequence of Synthetic Note A, version v1,\n'
            'Theorem~1.1~\\cite[Theorem~1.1]{note-a}.').replace(
            "Apply Synthetic Note B's cited theorem", 'Apply the imported positivity theorem').replace(
            'Synthetic Note B, version v2, Theorem~2.1~\\cite[Theorem~2.1]{note-b}', 'the imported positivity theorem'),
        'imported_as_original': text.replace(OPENING,
            'The following theorem is our original result, proved from scratch here.'),
        'hidden_attribution': text.replace(OPENING, '\\iffalse\n'+OPENING+'\n\\fi'),
        'optional_source_title': text.replace(OPENING, '').replace(
            r'\begin{theorem}\label{thm:square}',
            r'\begin{theorem}[Synthetic Note A, v1, Theorem 1.1]\label{thm:square}'),
        'unused_template_lemma': text.replace(r'\section{Connecting the Ingredients}',
            r'\begin{lemma}For every real $z$, $z=z$.\end{lemma}'
            r'\begin{proof}Reflexivity.\end{proof}'+'\n'+r'\section{Connecting the Ingredients}'),
        'unresolved_complete': text.replace(
            "Apply Synthetic Note B's cited theorem to this $a$ and the given strictly\n"
            'positive $\\varepsilon$; its output is $(x+1)^2+\\varepsilon>0$.',
            'The addition step is unresolved. We nevertheless declare the proof complete.'),
    }


class LiteralStatementPolicy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        (self.out/'manuscript').mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, content, preamble=''):
        (self.out/'manuscript/main.tex').write_text(
            preamble+'\n\\begin{document}\n'+content+'\n\\end{document}\n', encoding='utf-8')
        return statement_title_errors(inspect_tex(self.out))

    def test_all_literal_statement_types_and_custom_titles_rejected(self):
        for env in sorted(STATEMENTS | {'customfact'}):
            with self.subTest(env=env):
                declarations = r'\newtheorem{customfact}{Fact}'
                self.assertIn('STATEMENT_DESCRIPTIVE_TITLE', {e['code'] for e in self.check(
                    '\\begin{'+env+'}[Description] $x=x$.\\end{'+env+'}', declarations)})

    def test_numbered_unnamed_and_proof_target_heading_allowed(self):
        body = '\n'.join('\\begin{'+e+'}\\label{'+e+'} $x=x$.\\end{'+e+'}'
                         for e in sorted(STATEMENTS | {'customfact'}))
        body += r'\begin{proof}[Proof of Theorem~\ref{theorem}]Equality.\end{proof}'
        self.assertEqual(self.check(body, r'\newtheorem{customfact}[theorem]{Fact}'), [])

    def test_comments_false_branches_unused_macros_and_quoted_sources_are_inert(self):
        for quote in (
            '% \\begin{theorem}[Source title] ignored\n',
            r'\iffalse\begin{lemma}[Source title]ignored\end{lemma}\fi',
            r'\newcommand{\unused}{\begin{proposition}[Source title]ignored\end{proposition}}',
            r'\verb|\begin{definition}[Source title] % literal|',
            r'\verb*+\begin{example}[Source title]+',
            r'\begin{verbatim}\begin{problem}[Source title]\end{verbatim}',
            r'\\begin{theorem}[This is text after a linebreak]',
        ):
            with self.subTest(quote=quote):
                self.assertEqual(self.check(quote+'\nActual prose about the Calabi--Yau theorem.'), [])
        self.assertEqual(self.check(r'\begin{equation}[x=x]\end{equation}'
            r'\begin{itemize}[leftmargin=*]\item A\end{itemize}'
            r'\begin{abstract}[Not a statement option]\end{abstract}'), [])

    def test_redefined_inline_literal_control_is_not_certified(self):
        self.check(r'\verb|quoted|', r'\renewcommand{\verb}{Hidden content}')
        self.assertIn('REVIEW_LOCATION_UNVERIFIABLE', {e['code'] for e in inspect_tex(self.out).errors})

    def test_quoted_verbatim_with_legal_opening_whitespace_is_inert(self):
        quoted = (r'\begin{theorem}[Quoted source title] $x=x$.\end{theorem}')
        for opening in (r'\begin {verbatim}', '\\begin\n{verbatim}'):
            with self.subTest(opening=opening):
                source = opening+'\n'+quoted+'\n'+r'\end{verbatim}'
                self.assertEqual(self.check(source), [])
                visible = source+'\n'+r'\begin{theorem}[Visible name] $x=x$.\end{theorem}'
                errors = self.check(visible)
                self.assertEqual([e['code'] for e in errors], ['STATEMENT_DESCRIPTIVE_TITLE'])

    def test_actual_literal_input_title_detected_but_unused_file_not_scanned(self):
        (self.out/'manuscript/part.tex').write_text(
            r'\begin{definition}[Phase]For real $x$, set $p=x$.\end{definition}')
        self.assertEqual(self.check('Actual prose.'), [])
        self.assertIn('STATEMENT_DESCRIPTIVE_TITLE', {e['code'] for e in self.check(r'\input{part.tex}')})

    def test_custom_head_titles_and_complex_heading_manual_scope(self):
        self.assertIn('STATEMENT_DESCRIPTIVE_TITLE', {e['code'] for e in self.check(
            r'\begin{fact}$x=x$.\end{fact}', r'\newtheorem{fact}{Claim (Reduction)}')})
        self.assertIn('STATEMENT_HEADING_REVIEW_REQUIRED', {e['code'] for e in self.check(
            r'\begin{fact}$x=x$.\end{fact}', r'\newtheorem{fact}{\textbf{Claim}}')})
        self.assertIn('STATEMENT_HEADING_REVIEW_REQUIRED', {e['code'] for e in self.check(
            r'\begin{fact}$x=x$.\end{fact}', r'\newtheorem{fact}{Existence}')})
        self.assertIn('STATEMENT_HEADING_REVIEW_REQUIRED', {e['code'] for e in self.check(
            r'\begin{fact}$x=x$.\end{fact}', r'\newenvironment{fact}{\par\textbf{Claim (Reduction)}}{}')})
        style = r'\newtheoremstyle{named}{3pt}{3pt}{}{}{}{}{.5em}{#1 #2 (Hidden name)}'
        preamble = style+r'\theoremstyle{named}\newtheorem{fact}{Claim}'
        self.assertIn('STATEMENT_HEADING_REVIEW_REQUIRED', {e['code'] for e in self.check(
            r'\begin{fact}$x=x$.\end{fact}', preamble)})
        self.assertEqual(self.check(r'\begin{theorem}$x=x$.\end{theorem}', preamble), [])
        self.assertEqual(self.check('No use of custom display.', preamble), [])

    def test_numbering_escape_rejected_and_recall_status_allowed(self):
        for env, preamble in [('lemma*', r'\newtheorem*{lemma*}{Lemma}'),
                              ('fact', r'\newtheorem*{fact}{Fact}')]:
            with self.subTest(env=env):
                self.assertIn('STATEMENT_NUMBERING_REQUIRED', {e['code'] for e in self.check(
                    '\\begin{'+env+'}$x=x$.\\end{'+env+'}', preamble)})
        self.assertEqual(self.check(r'\begin{theoremrecall}{thm:x}$x=x$.\end{theoremrecall}'), [])


class CurrentFourModeWorkflow(unittest.TestCase):
    def setUp(self):
        self.t = v.VNext(); self.t.setUp()

    def tearDown(self):
        self.t.tearDown()

    def test_twenty_preparations_keep_canonical_opening_and_explicit_workflow(self):
        for profile in ('minimal','thematic','lecture','paper'):
            for view in VIEW_TASKS:
                with self.subTest(profile=profile,view=view):
                    p,plan = self.t.make(profile=profile,oid=profile+'-'+view,view=view)
                    prepare_output(self.t.root,p)
                    body = (p.parent/'manuscript/main.tex').read_text()
                    outline = (p.parent/'outline.md').read_text()
                    self.assertEqual(plan['editorial_policy'], POLICY)
                    for phrase in ('fast passages first', 'precise slow subsections',
                                   'adjacent visible prose', 'before their first proof use',
                                   'no descriptive optional titles'):
                        self.assertIn(phrase,body)
                    self.assertIn('S0 fix reader, snapshot',outline)
                    self.assertIn('S3 open precise slow sections',outline)
                    first = body.index(r'\section{')
                    second = body.index(r'\section{',first+1)
                    self.assertIn('../generated/statements/N-main.tex',body[first:second])
                    self.assertEqual(r'\begin{abstract}' in body, profile=='paper')
                    if profile=='minimal':
                        self.assertEqual(len(re.findall(r'\\section\{',body)),3)
                    for node in ('N-main','N-def'):
                        generated=p.parent/f'generated/statements/{node}.tex'
                        snapshot=self.t.root/'snapshots'/plan['snapshot_id']/'files/knowledge/nodes'/f'{node}.md'
                        self.assertTrue(generated.is_file())
                        self.assertTrue(snapshot.is_file())
                    self.assertNotIn('\\input{../materials/',body)

    def test_optional_title_rejected_by_real_output_structure_gate(self):
        p,_=self.t.authored()
        main=p.parent/'manuscript/main.tex'
        main.write_text(main.read_text().replace(r'\begin{theorem}',r'\begin{theorem}[Existence]',1))
        self.assertIn('STATEMENT_DESCRIPTIVE_TITLE',
            {e['code'] for e in validate_structure(self.t.root,'new')['errors']})


class SyntheticReadingFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.out=Path(self.tmp.name)
        folder=self.out/'manuscript';folder.mkdir()
        for source in FIXTURE.iterdir():
            if source.is_file():shutil.copy2(source,folder/source.name)
        shutil.copy2(SKILL/'assets/templates/math-review.sty',folder/'math-review.sty')
        self.positive=(FIXTURE/'positive.tex').read_text()
        (folder/'main.tex').write_text(self.positive)

    def tearDown(self):
        self.tmp.cleanup()

    def test_shipped_recall_is_reachable_but_rewritten_recall_is_not_trusted(self):
        scan=inspect_tex(self.out)
        self.assertEqual(scan.errors, [])
        self.assertIn('manuscript/N-SQUARE.tex', scan.body_inputs)
        style=self.out/'manuscript/math-review.sty'
        style.write_text(style.read_text().replace(
            r'\newtheorem*{mathreviewrecalledtheorem}{\mathreviewrecallheading}',
            r'\newtheorem*{mathreviewrecalledtheorem}{Theorem (Hidden name)}'))
        self.assertIn('REVIEW_LOCATION_UNVERIFIABLE', {e['code'] for e in inspect_tex(self.out).errors})

    def test_recall_command_replacements_cannot_certify_canonical_locations(self):
        generated=self.out/'generated/statements';generated.mkdir(parents=True)
        shutil.copy2(FIXTURE/'N-SQUARE.tex',generated/'N-SQUARE.tex')
        original=self.positive.replace(r'\input{N-SQUARE.tex}',
            r'\input{../generated/statements/N-SQUARE.tex}')
        main=self.out/'manuscript/main.tex'
        recall_input=original.rindex(r'\input{../generated/statements/N-SQUARE.tex}')
        line=original.count('\n',0,recall_input)+1
        location=[dict(path='manuscript/main.tex',line_start=line,line_end=line)]
        main.write_text(original)
        scan=inspect_tex(self.out)
        self.assertEqual(scan.errors, [])
        self.assertEqual(validate_locations(self.out,location,node_id='N-SQUARE',
            canonical=True,inspection=scan), [])
        replacements={
            'inner_box_pair': r'\renewcommand{\mathreviewrecalledtheorem}{\setbox0=\vbox\bgroup}'
                r'\renewcommand{\endmathreviewrecalledtheorem}{\egroup}',
            'inner_descriptive_head': r'\renewcommand{\mathreviewrecalledtheorem}{\textbf{Theorem (Hidden name).}}'
                r'\renewcommand{\endmathreviewrecalledtheorem}{}',
            'inner_end_only': r'\def\endmathreviewrecalledtheorem{\egroup}',
            'outer_begin': r'\renewcommand{\theoremrecall}[1]{\setbox0=\vbox\bgroup}',
            'outer_end': r'\def\endtheoremrecall{\egroup}',
        }
        for name,replacement in replacements.items():
            with self.subTest(replacement=name):
                # Same line count keeps the canonical-location probe fixed.
                main.write_text(original.replace(r'\begin{document}',replacement+r'\begin{document}'))
                scan=inspect_tex(self.out)
                self.assertIn('REVIEW_LOCATION_UNVERIFIABLE',{e['code'] for e in scan.errors})
                self.assertIn('REVIEW_LOCATION_UNVERIFIABLE',{e['code'] for e in validate_locations(
                    self.out,location,node_id='N-SQUARE',canonical=True,inspection=scan)})

    def test_actual_source_notes_and_semantic_mutations_remain_review_required(self):
        self.assertEqual(statement_title_errors(inspect_tex(self.out)),[])
        cases=semantic_cases(self.positive)
        self.assertEqual(len(cases),9)
        target=os.environ.get('PMS_EDITORIAL_EVIDENCE_DIR')
        for name,body in cases.items():
            with self.subTest(case=name):
                self.assertNotEqual(body,self.positive)
                (self.out/'manuscript/main.tex').write_text(body)
                errors=statement_title_errors(inspect_tex(self.out))
                # The semantic failures intentionally are not machine-approved or
                # rejected by counting citations. Only the title is structural.
                self.assertEqual(bool(errors),name=='optional_source_title',errors)
                if target:
                    dest=Path(target)/'semantic-cases';dest.mkdir(parents=True,exist_ok=True)
                    (dest/(name+'.tex')).write_text(body,encoding='utf-8')
        if target:
            for source in FIXTURE.iterdir():shutil.copy2(source,Path(target)/'semantic-cases'/source.name)

    @unittest.skipUnless(shutil.which('pdflatex') or shutil.which('tectonic'), 'Real TeX engine unavailable')
    def test_compile_numbered_unnamed_linked_types_and_disallowed_named_candidate(self):
        folder=self.out/'manuscript'
        # The negative remains valid TeX but violates policy, making this a
        # discriminating editorial test rather than a syntax-error test.
        named=self.positive
        for env in ('theorem','lemma','proposition','corollary','definition','example','problem','remark','conjecture','observation'):
            named=named.replace('\\begin{'+env+'}', '\\begin{'+env+'}[Description]',1)
        named=named.replace(r'\newtheorem{observation}[theorem]{Observation}',
                            r'\newtheorem{observation}[theorem]{Observation (Custom name)}')
        quoted=self.positive.replace(r'\section{Main Results}',
            '\\section{Main Results}\n\\begin {verbatim}\n'
            '\\begin{theorem}[Quoted source title] $x=x$.\\end{theorem}\n'
            '\\end{verbatim}\n')
        for name,body in [('positive',self.positive),('named-negative',named),
                          ('quoted-source-boundary',quoted)]:
            with self.subTest(candidate=name):
                (folder/'main.tex').write_text(body)
                self.assertEqual(bool(statement_title_errors(inspect_tex(self.out))),name=='named-negative')
                candidate=folder/name;candidate.mkdir()
                for source in (folder/'math-review.sty',folder/'N-SQUARE.tex'):
                    shutil.copy2(source,candidate/source.name)
                (candidate/'main.tex').write_text(body)
                pdflatex=shutil.which('pdflatex')
                if pdflatex:
                    from build_checks import compile_one
                    report=compile_one(candidate,'main.tex',pdflatex)
                    self.assertEqual(report['status'],'PASS',report)
                else:
                    command=[shutil.which('tectonic'),'--keep-logs','--keep-intermediates','main.tex']
                    proc=subprocess.run(command,cwd=candidate,capture_output=True,text=True,timeout=120)
                    (candidate/'compiler-output.txt').write_text(proc.stdout+proc.stderr)
                    self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
                aux=(candidate/'main.aux').read_text()
                self.assertNotIn('undefined', (candidate/'main.log').read_text().lower())
                for label in ('thm:square','lem:local','prop:scaled','cor:positive','def:perturbation',
                              'ex:local','prob:square','rem:boundary','conj:extension','obs:input'):
                    self.assertRegex(aux,r'\\newlabel\{'+re.escape(label)+r'\}\{\{\d+\.\d+\}')
                self.assertTrue((candidate/'main.pdf').read_bytes().startswith(b'%PDF-'))
                target=os.environ.get('PMS_EDITORIAL_EVIDENCE_DIR')
                if target:
                    shutil.copytree(candidate,Path(target)/name,dirs_exist_ok=True)
                    import json
                    (Path(target)/name/'compile-report.json').write_text(json.dumps({
                        'engine': pdflatex or shutil.which('tectonic'),
                        'pdf_sha256':hashlib.sha256((candidate/'main.pdf').read_bytes()).hexdigest(),
                        'source_sha256':hashlib.sha256(body.encode()).hexdigest(),
                        'compile':'PASS', 'semantic_review':'REVIEW_REQUIRED',
                        'pdf_visual_inspection':'NOT_EXECUTED_BY_TEST'},indent=2))
        # Real links/numbering are inspected by the independent reviewer in the
        # retained PDFs; aux binding alone is not a pixel/semantic verdict.


if __name__=='__main__':unittest.main()
