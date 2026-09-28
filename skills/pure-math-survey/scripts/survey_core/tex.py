"""Conservative literal TeX inspection, shared by structure and impact analysis.

Paths follow the real compiler's manuscript working directory, not the directory
of the including file. Preamble, comments, verbatim material, uncalled macro
bodies and literal false branches cannot establish visible canonical use.
This is not a TeX interpreter or a hostile-code sandbox; semantic/page review
remains necessary even when a canonical input is syntactically present.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .common import diagnostic, require, safe

INPUT = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
BLOCK = re.compile(r"\\begin\{(verbatim\*?|Verbatim|comment|lstlisting|minted)\}.*?\\end\{\1\}", re.S)
DEFINITION = re.compile(r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand)\*?\s*|\\(?:gdef|edef|xdef|def)\s*")


def _group_end(text: str, start: int, left: str = '{', right: str = '}') -> int:
    """Index after a balanced literal group. No expansion is attempted."""
    if start >= len(text) or text[start] != left:
        return start
    depth = 0
    i = start
    while i < len(text):
        if text[i] == '\\':
            i += 2
            continue
        if text[i] == left:
            depth += 1
        elif text[i] == right:
            depth -= 1
            if not depth:
                return i + 1
        i += 1
    return len(text)


def _blank(text: str) -> str:
    return ''.join('\n' if c == '\n' else ' ' for c in text)


def visible_source(text: str) -> str:
    """Mask known nonexecuted literal material while preserving line numbers."""
    from check_mathematical_structure import strip_comments
    text = strip_comments(text)
    text = BLOCK.sub(lambda m: _blank(m[0]), text)
    # Nested conditionals inside a literal false branch are not visible.
    start = 0
    while True:
        match = re.search(r'\\iffalse\b', text[start:])
        if not match:
            break
        a = start + match.start()
        depth = 1
        b = len(text)
        for token in re.finditer(r'\\(?:if[a-zA-Z]*|fi)\b', text[start + match.end():]):
            absolute = start + match.end() + token.start()
            depth += -1 if token[0] == r'\fi' else 1
            if depth == 0:
                b = absolute + len(token[0])
                break
        text = text[:a] + _blank(text[a:b]) + text[b:]
        start = b
    # An input inside an uncalled macro definition is not a body statement.
    start = 0
    while True:
        match = DEFINITION.search(text, start)
        if not match:
            break
        i = match.end()
        while i < len(text) and text[i].isspace():
            i += 1
        if i < len(text) and text[i] == '{':
            i = _group_end(text, i)
        else:
            name = re.match(r'\\[a-zA-Z@]+|\\.', text[i:])
            i += len(name[0]) if name else 0
        # Optional argument-count/default groups, or primitive def parameters.
        while i < len(text) and text[i] != '{':
            if text[i] == '[':
                i = _group_end(text, i, '[', ']')
            else:
                i += 1
        end = _group_end(text, i)
        if end <= match.end():
            start = match.end()
            continue
        text = text[:match.start()] + _blank(text[match.start():end]) + text[end:]
        start = end
    return text


def input_path(out: Path, value: str) -> Path:
    value = value.strip()
    require(value and not any(c in value for c in '\\:\x00{}') and not Path(value).is_absolute(),
            'TEX_INPUT_UNSUPPORTED', 'Use literal output-local TeX input paths', value)
    if not Path(value).suffix:
        value += '.tex'
    base = out / 'manuscript'
    candidate = base
    for component in Path(value).parts:
        candidate = candidate / component
        require(not candidate.is_symlink(), 'UNSAFE_PATH', 'Symlinked TeX input is not allowed', value)
    target = candidate.resolve()
    require(target.is_relative_to(out.resolve()), 'UNSAFE_PATH', 'TeX input escapes the output directory', value)
    relative = target.relative_to(out.resolve()).as_posix()
    return safe(out, relative, True)


@dataclass
class Inspection:
    text: str
    inputs: set[str]
    body_inputs: set[str]
    locations: list[dict]
    errors: list[dict]


def inspect_tex(out: Path) -> Inspection:
    out = out.resolve()
    main = safe(out, 'manuscript/main.tex', True)
    errors: list[dict] = []
    locations: list[dict] = []
    all_used: set[str] = {'manuscript/main.tex'}
    body_used: set[str] = set()

    def visit(path: Path, active: tuple[Path, ...], body: bool, main_file: bool = False) -> str:
        require(path not in active, 'TEX_INPUT_CYCLE', 'Recursive literal TeX input', path.relative_to(out).as_posix())
        text = visible_source(path.read_text(encoding='utf-8'))
        if main_file and body:
            begins = list(re.finditer(r'\\begin\s*\{document\}', text))
            ends = list(re.finditer(r'\\end\s*\{document\}', text))
            if len(begins) != 1 or len(ends) != 1 or begins[0].end() > ends[0].start():
                errors.append(diagnostic('TEX_DOCUMENT_INVALID', 'Exactly one ordered document body is required', 'manuscript/main.tex'))
                return ''
            a, b = begins[0].end(), ends[0].start()
            text = _blank(text[:a]) + text[a:b] + _blank(text[b:])
        def replace(match: re.Match) -> str:
            target = input_path(out, match[1])
            relative = target.relative_to(out).as_posix()
            all_used.add(relative)
            if body:
                body_used.add(relative)
                locations.append({'path': path.relative_to(out).as_posix(),
                                  'line_start': text.count('\n', 0, match.start()) + 1,
                                  'line_end': text.count('\n', 0, match.end()) + 1,
                                  'input': relative})
            return '\n' + visit(target, active + (path,), body) + '\n'
        expanded = INPUT.sub(replace, text)
        require(not re.search(r'\\(?:input|include)\b', expanded), 'TEX_INPUT_UNSUPPORTED',
                'Dynamic or unbraced TeX inputs cannot be certified by the literal inspector', path.relative_to(out).as_posix())
        return expanded

    expanded = visit(main, (), False)
    visit(main, (), True, main_file=True)
    return Inspection(expanded, all_used, body_used, locations, errors)


def validate_locations(out: Path, locations: object, *, node_id: str | None = None,
                       canonical: bool = False) -> list[dict]:
    """Validate exact authored line ranges; optionally locate a canonical input."""
    errors = []
    if not isinstance(locations, list) or not locations:
        return [diagnostic('REVIEW_LOCATION_INVALID', 'Supply nonempty structured path/line_start/line_end locations', 'evidence', node_id)]
    for loc in locations:
        valid = isinstance(loc, dict) and {'path', 'line_start', 'line_end'} <= loc.keys()
        if not valid:
            errors.append(diagnostic('REVIEW_LOCATION_INVALID', 'Expected a structured authored location', 'evidence', node_id))
            continue
        rel = loc['path']
        try:
            require(isinstance(rel, str) and rel.startswith('manuscript/'), 'REVIEW_LOCATION_INVALID', 'Location must be in authored manuscript', str(rel))
            path = safe(out, rel, True)
            lines = path.read_text(encoding='utf-8').splitlines()
            lo, hi = loc['line_start'], loc['line_end']
            require(type(lo) is int and type(hi) is int and 1 <= lo <= hi <= len(lines),
                    'REVIEW_LOCATION_INVALID', 'Location line range does not exist', rel)
            if canonical:
                scan = inspect_tex(out)
                require(any(x['path'] == rel and lo <= x['line_start'] <= hi and
                            x['input'] == f'generated/statements/{node_id}.tex' for x in scan.locations),
                        'REVIEW_LOCATION_INVALID', 'Location does not contain this visible canonical input', rel)
        except (OSError, ValueError) as exc:
            errors.append(diagnostic('REVIEW_LOCATION_INVALID', str(exc), str(rel), node_id))
        except Exception as exc:
            from .common import SurveyError
            if not isinstance(exc, SurveyError):
                raise
            errors.append(diagnostic('REVIEW_LOCATION_INVALID', str(exc), str(rel), node_id))
    return errors
