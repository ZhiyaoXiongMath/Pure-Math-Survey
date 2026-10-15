"""Literal TeX reachability with original-file locations (not a TeX interpreter).

Inputs are resolved from the manuscript compiler working directory. The scanner
supports balanced literal iftrue/iffalse branches and literal input/include;
comments, unused definitions and nonexecuted branches retain their source lines
but cannot supply review evidence. Unsupported execution is diagnosed, never
asserted visible. Body reachability does not establish pixel visibility or proof.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

from .common import native_path, relpath, resolved_path, SurveyError, diagnostic, require, safe, SKILL_ROOT

TOKEN = re.compile(r'\\(?:[A-Za-z@]+|[^A-Za-z@])')
INPUT = re.compile(r'\\(?:input|include)\s*\{([^{}]+)\}')
BLOCK = re.compile(r'\\begin\s*\{(verbatim\*?|Verbatim|comment|lstlisting|minted)\}.*?\\end\{\1\}', re.S)
DEFINITIONS = {'newcommand', 'renewcommand', 'providecommand', 'DeclareRobustCommand',
               'def', 'gdef', 'edef', 'xdef', 'newenvironment', 'renewenvironment'}
DYNAMIC = {'csname', 'expandafter', 'scantokens', 'catcode', 'includeonly', 'let',
           'futurelet', 'aftergroup', 'AtBeginDocument', 'AtEndDocument', 'loop', 'repeat',
           'directlua', 'write', 'read', 'openin', 'openout', 'everypar', 'everymath',
           'everydisplay', 'afterassignment', 'setbox', 'sbox', 'savebox', 'usebox'}
STRUCTURAL = DEFINITIONS | DYNAMIC | {'input', 'include', 'begin', 'end', 'endinput',
                                    'iftrue', 'iffalse', 'else', 'fi', 'newtheorem',
                                    'newtheoremstyle', 'theoremstyle', 'verb'}


def _blank(text: str) -> str:
    return ''.join('\n' if c == '\n' else ' ' for c in text)


def _group_end(text: str, start: int, left: str = '{', right: str = '}') -> int:
    if start >= len(text) or text[start] != left:
        return start
    depth = 0; i = start
    while i < len(text):
        if text[i] == '\\':
            token = TOKEN.match(text, i)
            i = token.end() if token else i + 1
            continue
        if text[i] == left:
            depth += 1
        elif text[i] == right:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def _space(text: str, i: int) -> int:
    while i < len(text) and text[i].isspace():
        i += 1
    return i


def _comments(text: str) -> str:
    chars = list(text); i = 0; command_names = set()
    while i < len(text):
        if text[i] == '\\':
            token = TOKEN.match(text, i)
            if token and token[0][1:] in DEFINITIONS:
                j = _space(text,token.end())
                if text[j:j+1] == '*':
                    j = _space(text,j+1)
                if text[j:j+1] == '{':
                    j = _space(text,j+1)
                name_token = TOKEN.match(text,j)
                if name_token:
                    command_names.add(name_token.start())
            if token and token[0] == r'\verb' and token.start() not in command_names:
                j = token.end()
                if j < len(text) and text[j] == '*':
                    j += 1
                end = text.find(text[j], j+1) if j < len(text) and not text[j].isspace() else -1
                i = end+1 if end >= 0 and '\n' not in text[j:end] else token.end()
            else:
                i = token.end() if token else i + 1
        elif text[i] == '%':
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            chars[i:end] = ' ' * (end - i); i = end
        else:
            i += 1
    return ''.join(chars)


def _definition(text: str, token: re.Match) -> tuple[int, str, str]:
    i = _space(text, token.end())
    if i < len(text) and text[i] == '*':
        i = _space(text, i + 1)
    if i < len(text) and text[i] == '{':
        end = _group_end(text, i); name = text[i+1:end-1].strip().lstrip('\\'); i = end
    else:
        match = TOKEN.match(text, i)
        name = match[0][1:] if match else ''
        i = match.end() if match else i
    while i < len(text) and text[i] != '{':
        i = _group_end(text, i, '[', ']') if text[i] == '[' else i + 1
    end = _group_end(text, i)
    body = text[i+1:end-1] if end > i else ''
    if token[0][1:] in {'newenvironment', 'renewenvironment'}:
        j = _space(text, end); end = _group_end(text, j)
        body += text[j+1:end-1] if end > j else ''
        name = 'environment:' + name
    return max(end, token.end()), name, body


def _lex(text: str) -> tuple[str, list[tuple[int, str, str]], list[tuple[int, str]]]:
    """Mask while preserving every original offset and newline (CRLF is normalized)."""
    text = _comments(text)
    # Inline quoted source/code is not an executed statement. Mask before any
    # command/conditional scan, preserving original offsets and line identities.
    chars = list(text); skip = 0
    for token in TOKEN.finditer(text):
        if token.start() < skip:
            continue
        if token[0][1:] in DEFINITIONS:
            skip = _definition(text,token)[0]; continue
        if token[0] != r'\verb':
            continue
        j = token.end()
        if j < len(text) and text[j] == '*':
            j += 1
        end = text.find(text[j],j+1) if j < len(text) and not text[j].isspace() else -1
        if end >= 0 and '\n' not in text[j:end]:
            skip = end+1; chars[token.start():skip] = _blank(text[token.start():skip])
    text = ''.join(chars)
    begins = {m.start() for m in TOKEN.finditer(text) if m[0] == r'\begin'}
    text = BLOCK.sub(lambda m: _blank(m[0]) if m.start() in begins else m[0], text)
    chars = list(text); definitions = []; issues = []
    # Each frame: outer branch executes, test value (None means unsupported), else seen.
    stack: list[tuple[bool, bool | None, bool]] = []
    active = True; previous = 0; i = 0
    while (token := TOKEN.search(text, i)) is not None:
        if not active:
            chars[previous:token.start()] = _blank(text[previous:token.start()])
        name = token[0][1:]; end = token.end()
        if name in DEFINITIONS:
            end, macro, body = _definition(text, token)
            if active:
                definitions.append((token.start(), macro, body))
            chars[token.start():end] = _blank(text[token.start():end])
        elif name.startswith('if') and name != 'iff':
            known = name in {'iftrue', 'iffalse'}
            if active and not known:
                issues.append((token.start(), f'Unsupported conditional \\{name}; use literal iftrue/iffalse with balanced else/fi'))
            value = name == 'iftrue' if known else None
            stack.append((active, value, False)); active = active and value is True
            chars[token.start():end] = _blank(text[token.start():end])
        elif name == 'else':
            if not stack or stack[-1][2]:
                issues.append((token.start(), 'Unmatched or repeated conditional else'))
            else:
                outer, value, _ = stack[-1]
                stack[-1] = (outer, value, True); active = outer and value is False
            chars[token.start():end] = _blank(text[token.start():end])
        elif name == 'fi':
            if not stack:
                issues.append((token.start(), 'Unmatched conditional fi'))
            else:
                active = stack.pop()[0]
            chars[token.start():end] = _blank(text[token.start():end])
        elif not active:
            chars[token.start():end] = _blank(text[token.start():end])
        previous = end; i = end
    if not active:
        chars[previous:] = _blank(text[previous:])
    if stack:
        issues.append((len(text), 'Unclosed literal conditional; cross-file conditional control is not supported'))
    return ''.join(chars), definitions, issues


def visible_source(text: str) -> str:
    return _lex(text)[0]


def input_path(out: Path, value: str) -> Path:
    value = value.strip()
    require(value and not any(c in value for c in '\\:\x00{}') and not Path(value).is_absolute(),
            'TEX_INPUT_UNSUPPORTED', 'Use literal output-local TeX input paths', value)
    if not Path(value).suffix:
        value += '.tex'
    candidate = out / 'manuscript'
    for component in Path(value).parts:
        candidate = candidate / component
        require(not native_path(candidate).is_symlink(), 'UNSAFE_PATH', 'Symlinked TeX input is not allowed', value)
    target = resolved_path(candidate)
    require(target.is_relative_to(resolved_path(out)), 'UNSAFE_PATH', 'TeX input escapes the output directory', value)
    return safe(out, relpath(resolved_path(out), target), True)


def _meaningful(text: str) -> str:
    """Ignore non-content syntax, not mathematical commands or displayed formulas."""
    chars = list(text); i = 0
    group_commands = {'begin', 'end', 'label', 'index', 'nocite', 'bibliographystyle',
                      'vspace', 'hspace', 'setcounter', 'addtocounter', 'typeout', 'message', 'tag'}
    empty_commands = {'par', 'noindent', 'newpage', 'clearpage', 'pagebreak', 'nopagebreak',
                      'hfill', 'vfill', 'smallskip', 'medskip', 'bigskip', 'centering',
                      'raggedright', 'relax', 'global', 'long', 'nonumber', 'notag', 'quad', 'qquad', '[', ']', '(', ')', '\\', ',', ';', ':', '!', ' '}
    while (token := TOKEN.search(text, i)) is not None:
        name = token[0][1:]; end = token.end()
        if name in group_commands:
            j = _space(text, end)
            if j < len(text) and text[j] == '*':
                j = _space(text, j + 1)
            end = _group_end(text, j)
            if name in {'setcounter', 'addtocounter'}:
                end = _group_end(text, _space(text, end))
        if name in group_commands | empty_commands:
            chars[token.start():end] = _blank(text[token.start():end])
        i = max(end, token.end())
    return re.sub(r'[{}$&_\^~]', ' ', ''.join(chars))


@dataclass
class Inspection:
    text: str
    inputs: set[str]
    body_inputs: set[str]
    locations: list[dict]
    errors: list[dict]
    body_lines: dict[str, set[int]] = field(default_factory=dict)
    content_lines: dict[str, set[int]] = field(default_factory=dict)
    statement_environments: dict[str, str] = field(default_factory=dict)
    heading_customizations: list[dict] = field(default_factory=list)
    statement_styles: dict[str, str] = field(default_factory=dict)
    unnumbered_statements: set[str] = field(default_factory=set)
    custom_environment_heads: dict[str, dict] = field(default_factory=dict)


def inspect_tex(out: Path) -> Inspection:
    out = resolved_path(out); main = safe(out, 'manuscript/main.tex', True)
    scan = Inspection('', {'manuscript/main.tex'}, set(), [], [])
    cache = {}; definitions = {}; executable = []; loaded_styles = set()
    theorem_style = 'plain'

    def issue(rel: str, text: str, pos: int, message: str):
        scan.errors.append(diagnostic('REVIEW_LOCATION_UNVERIFIABLE',
            f'Line {text.count(chr(10),0,pos)+1}: {message}', rel))

    def mark(rel: str, text: str, start: int, end: int, meaningful: str):
        if end <= start:
            return
        lo = text.count('\n', 0, start) + 1
        hi = text.count('\n', 0, end - 1) + 1
        scan.body_lines.setdefault(rel, set()).update(range(lo, hi + 1))
        for line, part in enumerate(meaningful[start:end].split('\n'), lo):
            if part.strip():
                scan.content_lines.setdefault(rel, set()).add(line)

    def visit(path: Path, active: tuple[Path, ...], in_body: bool, is_main=False) -> tuple[str, bool]:
        nonlocal theorem_style
        rel = relpath(out, path)
        require(path not in active, 'TEX_INPUT_CYCLE', 'Recursive literal TeX input', rel)
        scan.inputs.add(rel)
        if path not in cache:
            raw = path.read_text(encoding='utf-8')
            cache[path] = (raw, *_lex(raw))
        raw, text, defs, problems = cache[path]
        tokens = list(TOKEN.finditer(text)); document = []
        for token in tokens:
            if token[0] in {r'\begin', r'\end'}:
                j = _space(text, token.end()); e = _group_end(text, j)
                if text[j:e] == '{document}':
                    document.append((token.start(), e, token[0]))
        if is_main:
            if len(document) != 2 or [x[2] for x in document] != [r'\begin', r'\end']:
                scan.errors.append(diagnostic('TEX_DOCUMENT_INVALID', 'Exactly one ordered literal document body in main.tex is required', rel))
                return text, False
            body_start, body_end = document[0][1], document[1][0]
            stop = document[1][1]
        else:
            require(not document, 'TEX_DOCUMENT_INVALID', 'Document delimiters must be literal in main.tex, not in an included file', rel)
            body_start, body_end, stop = (0, len(text), len(text)) if in_body else (0, 0, len(text))
        endinput = next((t.start() for t in tokens if t[0] == r'\endinput'), len(text))
        stop = min(stop, endinput)
        body_end = min(body_end, stop)
        command_offsets = {t.start() for t in tokens}
        for pos, name, body in defs:
            if pos < stop and name.startswith('environment:') and name != 'environment:theoremrecall':
                if _meaningful(body).strip():
                    scan.custom_environment_heads[name.split(':',1)[1]] = {'path':rel,'line':raw.count('\n',0,pos)+1}
            if pos < stop and name in {'thmhead', 'thmhead@plain', '@begintheorem', '@opargbegintheorem',
                                      'theoremname', 'lemmaname', 'propositionname', 'thetheorem',
                                      'thelemma', 'theproposition', 'thecorollary', 'thedefinition',
                                      'theexample', 'theproblem', 'theremark', 'theconjecture'}:
                scan.heading_customizations.append({'path':rel, 'line':raw.count('\n',0,pos)+1, 'style':None})
        for match in re.finditer(r'\\newtheoremstyle\s*\{([^{}]+)\}', text[:stop]):
            if match.start() in command_offsets:
                scan.heading_customizations.append({'path':rel, 'line':raw.count('\n',0,match.start())+1, 'style':match[1]})
        for pos, name, body in defs:
            if pos < stop:
                definitions.setdefault(name, []).append((rel, pos, body))
                if name in STRUCTURAL:
                    issue(rel, raw, pos, f'Redefinition of scanner control \\{name} is unsupported')
        for pos, message in problems:
            if pos <= stop:
                issue(rel, raw, pos, message)
        significant = _meaningful(text)
        chunks = []; previous = 0; has_content = False
        for token in tokens:
            if token.start() < previous or token.start() >= stop:
                continue
            name = token[0][1:]
            executable.append((rel, raw, token.start(), name))
            # Preserve execution order across literal inputs and local packages.
            # This inventories only amsthm's literal declaration interface.
            if name in {'newtheorem', 'theoremstyle'}:
                j = _space(text, token.end()); starred = text[j:j+1] == '*'
                if starred:
                    j = _space(text,j+1)
                end = _group_end(text,j)
                if j < stop and text[j] == '{' and end <= stop:
                    env = text[j+1:end-1]
                    if name == 'theoremstyle':
                        theorem_style = env
                    else:
                        j = _space(text,end)
                        if j < stop and text[j] == '[':
                            j = _space(text,_group_end(text,j,'[',']'))
                        end = _group_end(text,j)
                        if j < stop and text[j] == '{' and end <= stop:
                            scan.statement_environments[env] = text[j+1:end-1]
                            scan.statement_styles[env] = theorem_style
                            if starred:
                                scan.unnumbered_statements.add(env)
            if name in {'begin', 'end'}:
                j = _space(text, token.end()); end = _group_end(text, j)
                if end > j and text[j] == '{':
                    executable.append((rel, raw, token.start(), 'environment:' + text[j+1:end-1]))
            if name in DYNAMIC:
                issue(rel, raw, token.start(), f'Execution-changing \\{name} is outside the literal model')
            if name in {'usepackage', 'RequirePackage'}:
                j = _space(text, token.end())
                if j < len(text) and text[j] == '[':
                    j = _space(text, _group_end(text,j,'[',']'))
                end = _group_end(text,j)
                if end > j and text[j] == '{':
                    for package in text[j+1:end-1].split(','):
                        package = package.strip()
                        if not package or any(c in package for c in '\\:{}'):
                            issue(rel,raw,token.start(),'Dynamic local package name is not certifiable'); continue
                        local = safe(out,'manuscript/'+package+'.sty')
                        if local.is_file() and local not in loaded_styles:
                            loaded_styles.add(local)
                            visit(local,active+(path,),False)
            if name not in {'input', 'include'}:
                continue
            match = INPUT.match(text, token.start())
            if match is None:
                issue(rel, raw, token.start(), 'Dynamic or unbraced input/include is not certifiable')
                # Keep the token for diagnostics, but never use it as content evidence.
                significant = significant[:token.start()] + _blank(significant[token.start():token.end()]) + significant[token.end():]
                continue
            a, b = match.span()
            start, end = max(previous, body_start), min(a, body_end)
            mark(rel, raw, start, end, significant)
            chunks.append(text[previous:a])
            target = input_path(out, match[1]); target_rel = relpath(out, target)
            child_body = body_start <= a < body_end
            child, child_content = visit(target, active + (path,), child_body)
            if child_body:
                scan.body_inputs.add(target_rel)
                loc = {'path': rel, 'line_start': raw.count('\n',0,a)+1,
                       'line_end': raw.count('\n',0,b-1)+1, 'input': target_rel}
                scan.locations.append(loc)
                scan.body_lines.setdefault(rel,set()).update(range(loc['line_start'],loc['line_end']+1))
                if child_content:
                    scan.content_lines.setdefault(rel,set()).update(range(loc['line_start'],loc['line_end']+1))
            chunks.append('\n' + child + '\n'); previous = b
        mark(rel, raw, max(previous, body_start), body_end, significant)
        chunks.append(text[previous:stop] + _blank(text[stop:]))
        # Only current invocation content counts for a preamble/body double input.
        has_content = bool(scan.content_lines.get(rel)) if (in_body or is_main) else False
        return ''.join(chunks), has_content

    scan.text, _ = visit(main, (), False, True)
    # This shipped literal recall wrapper only sets a heading and opens/closes
    # the unnumbered recalled display. Trust neither a rewritten wrapper nor a
    # same-named replacement helper. Its enclosed input is scanned normally.
    recall_names = {'environment:theoremrecall', 'mathreviewrecallheading'}
    # newenvironment/newtheorem create begin/end commands indirectly. Ordinary
    # command replacement of either pair must revoke this narrow exemption too.
    recall_replacements = {'theoremrecall', 'endtheoremrecall',
                           'mathreviewrecalledtheorem', 'endmathreviewrecalledtheorem',
                           'environment:mathreviewrecalledtheorem'}
    shipped_style = (SKILL_ROOT/'assets/templates/math-review.sty').read_bytes()
    expected_recall = {name:body for _,name,body in _lex(shipped_style.decode('utf-8'))[1] if name in recall_names}
    trusted_recall = (scan.statement_environments.get('mathreviewrecalledtheorem') == r'\mathreviewrecallheading' and
        'mathreviewrecalledtheorem' in scan.unnumbered_statements and
        not recall_replacements.intersection(definitions) and all(len(definitions.get(name,[])) == 1 and
        definitions[name][0][0] == 'manuscript/math-review.sty' and
        definitions[name][0][2] == expected_recall.get(name) for name in recall_names))
    # Ordinary mathematical notation aliases are allowed. Resolve only risk,
    # not TeX expansion: an indirect call into empty/control code is uncertified.
    def risky(name: str, visiting: frozenset[str] = frozenset()) -> bool:
        if name == 'environment:theoremrecall' and trusted_recall:
            return False
        if name in visiting:
            return True
        for _, _, body in definitions.get(name, []):
            names = {m[0][1:] for m in TOKEN.finditer(body)}
            # Empty environment wrappers preserve their enclosed content;
            # empty command expansion cannot itself supply content evidence.
            if ((not name.startswith('environment:') and not _meaningful(body).strip()) or names & STRUCTURAL or
                    any(n.startswith('if') and n != 'iff' for n in names)):
                return True
            if any(risky(n,visiting|{name}) for n in names if n in definitions):
                return True
        return False
    for rel, raw, pos, name in executable:
        if name in definitions and risky(name):
            issue(rel, raw, pos, f'Cannot certify expansion of \\{name}; use literal decisive content')
    return scan


def validate_locations(out: Path, locations: object, *, node_id: str | None = None,
                       canonical: bool = False, inspection: Inspection | None = None) -> list[dict]:
    """Validate EVERY range against one ephemeral scan shared by the caller."""
    errors = []
    if not isinstance(locations, list) or not locations:
        return [diagnostic('REVIEW_LOCATION_INVALID', 'Supply nonempty structured path/line_start/line_end locations', 'evidence', node_id)]
    scan = inspection
    for loc in locations:
        if not isinstance(loc, dict) or not {'path', 'line_start', 'line_end'} <= loc.keys():
            errors.append(diagnostic('REVIEW_LOCATION_INVALID', 'Expected a structured authored location', 'evidence', node_id)); continue
        rel = loc['path']
        try:
            require(isinstance(rel,str) and rel.startswith('manuscript/') and rel.endswith('.tex'),
                    'REVIEW_LOCATION_INVALID', 'Location must be an authored manuscript TeX file', str(rel))
            path = safe(out, rel, True); lines = path.read_text(encoding='utf-8').splitlines()
            lo, hi = loc['line_start'], loc['line_end']
            require(type(lo) is int and type(hi) is int and 1 <= lo <= hi <= len(lines),
                    'REVIEW_LOCATION_INVALID', 'Location line range does not exist', rel)
        except (SurveyError, OSError, ValueError) as exc:
            errors.append(diagnostic('REVIEW_LOCATION_INVALID', str(exc), str(rel), node_id)); continue
        try:
            if scan is None:
                scan = inspect_tex(out)
        except (SurveyError, OSError, ValueError) as exc:
            errors.append(diagnostic('REVIEW_LOCATION_UNVERIFIABLE', str(exc), rel, node_id)); continue
        prefix = f'Lines {lo}-{hi}: '
        code = None; message = ''
        if scan.errors:
            code = 'REVIEW_LOCATION_UNVERIFIABLE'
            message = '; '.join(f'{e["path"]}: {e["message"]}' for e in scan.errors)
        elif rel not in scan.inputs:
            code = 'REVIEW_LOCATION_UNREACHABLE'; message = 'File is not reachable through an executed literal input from main.tex'
        elif not any(lo <= line <= hi for line in scan.body_lines.get(rel, set())):
            code = 'REVIEW_LOCATION_NOT_IN_BODY'; message = 'Range is in the preamble, after document end, or outside the input body context'
        elif not any(lo <= line <= hi for line in scan.content_lines.get(rel, set())):
            code = 'REVIEW_LOCATION_EMPTY'; message = 'No substantive unmasked body content in this range'
        elif canonical and not any(x['path'] == rel and lo <= x['line_start'] <= hi
                and x['input'] == f'generated/statements/{node_id}.tex' for x in scan.locations):
            code = 'REVIEW_LOCATION_INVALID'; message = 'Range does not contain this actual canonical body input'
        if code:
            errors.append(diagnostic(code, prefix + message, rel, node_id))
    return errors
