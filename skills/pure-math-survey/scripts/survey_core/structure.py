"""Literal TeX inventories used by current output and sample checks."""
from __future__ import annotations
import hashlib
import re
from .common import native_path, resolved_path
from collections import Counter
from pathlib import Path, PurePosixPath

RESULTS = {'theorem', 'proposition', 'lemma', 'corollary'}
STATEMENTS = RESULTS | {'definition', 'example', 'problem', 'remark', 'conjecture',
                        'claim', 'observation', 'assumption', 'question', 'exercise'}
LABEL = re.compile(r'\\label\s*\{([^{}]+)\}')
BEGIN = re.compile(r'\\begin\s*\{(theorem|proposition|lemma|corollary|proof|theoremrecall)\}')
SECTION = re.compile(r'\\section(\*)?\s*(?:\[[^\]]*\]\s*)?\{')
CITE = re.compile(r'\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^{}]+)\}')
REFERENCE = re.compile(r'\\(?:eqref|ref|pageref|nameref|autoref|cref|Cref)\s*\{([^{}]+)\}')
PLACEHOLDER = re.compile(r'\\placeholder\b|\b(?:PENDING|TODO|TBD)\b|\[INSERT', re.I)


INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")

def statement_title_errors(inspection) -> list[dict]:
    """Bounded literal title check, using the existing reachability scan.

    Custom amsthm environments are included. Arbitrary heading macros/styles
    require actual manual inspection rather than a claim of automatic safety.
    Proof-target headings and the supported recall status are not statement names.
    No citation quota or mathematical attribution decision is made here.
    """
    from .common import diagnostic
    from .tex import TOKEN, _space, _group_end
    body = inspection.text.split(r'\begin{document}', 1)[-1].split(r'\end{document}', 1)[0]
    declared = inspection.statement_environments
    environments = STATEMENTS | set(declared)
    environments |= {name+'*' for name in STATEMENTS}
    environments -= {'theoremrecall', 'proof'}
    errors = []; used = set()
    for token in TOKEN.finditer(body):
        if token[0] != r'\begin':
            continue
        start = _space(body,token.end()); end = _group_end(body,start)
        if start >= len(body) or body[start] != '{':
            continue
        env = body[start+1:end-1]
        if env in inspection.custom_environment_heads:
            location = inspection.custom_environment_heads[env]
            errors.append(diagnostic('STATEMENT_HEADING_REVIEW_REQUIRED',
                f'Line {location["line"]}: called custom environment {env} has a nonliteral heading/body wrapper; inspect its actual PDF for statement names and numbering or simplify it.', location['path']))
        if env not in environments:
            continue
        used.add(env)
        if env in inspection.unnumbered_statements or (env.endswith('*') and env[:-1] in STATEMENTS):
            errors.append(diagnostic('STATEMENT_NUMBERING_REQUIRED',
                f'{env}: use the numbered mathematical statement type; retain automatic numbering and labels.', 'manuscript/main.tex'))
        if body[_space(body,end):].startswith('['):
            errors.append(diagnostic('STATEMENT_DESCRIPTIVE_TITLE',
                f'{env}: remove the optional descriptive title; keep the type, automatic number and label. Put terminology and accurate attribution in adjacent visible prose.',
                'manuscript/main.tex'))
        heading = declared.get(env, env)
        if re.search(r'[\[\]()]', heading):
            errors.append(diagnostic('STATEMENT_DESCRIPTIVE_TITLE',
                f'{env}: literal declaration embeds a parenthesized/bracketed descriptive heading. Retain only its statement type.', 'manuscript/main.tex'))
        elif heading.lower() not in STATEMENTS | {'fact', 'result', 'assertion'}:
            errors.append(diagnostic('STATEMENT_HEADING_REVIEW_REQUIRED',
                f'{env}: custom heading cannot be certified by the literal scanner; inspect its actual numbered PDF heading and remove any descriptive name.', 'manuscript/main.tex'))
    if used:
        for location in inspection.heading_customizations:
            if location['style'] is not None and not any(inspection.statement_styles.get(env) == location['style'] for env in used):
                continue
            errors.append(diagnostic('STATEMENT_HEADING_REVIEW_REQUIRED',
                f'Line {location["line"]}: custom theorem heading/style requires actual PDF inspection for numbering and absence of descriptive names; simplify to a literal type for automatic validation.', location['path']))
    return errors

def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        chars, slashes = [], 0
        for c in line:
            if c == '%' and slashes % 2 == 0:
                break
            chars.append(c)
            slashes = slashes + 1 if c == '\\' else 0
        lines.append(''.join(chars))
    return '\n'.join(lines)

def group_end(text: str, start: int) -> int:
    """Return the end of a braced argument whose opening brace is at start."""
    level = 0
    for i in range(start, len(text)):
        if text[i] in '{}':
            k = i - 1
            while k >= 0 and text[k] == '\\':
                k -= 1
            if (i - 1 - k) % 2:
                continue
            level += 1 if text[i] == '{' else -1
            if level == 0:
                return i + 1
    raise ValueError('unclosed braced section heading')

def inventory(expanded: str) -> dict:
    from .tex import TOKEN
    text = strip_comments(expanded)
    # Inventory numbers are offsets in the body, not source-file line claims.
    body = text.split(r'\begin{document}', 1)[-1].split(r'\end{document}', 1)[0]
    command_offsets = {m.start() for m in TOKEN.finditer(body)}
    sections = []
    for m in SECTION.finditer(body):
        if m.start() not in command_offsets:
            continue
        end = group_end(body, m.end()-1)
        title = body[m.end():end-1]
        lm = re.match(r'\s*\\label\s*\{([^{}]+)\}', body[end:])
        sections.append({'title': title, 'label': lm.group(1) if lm else '',
                         'starred': bool(m.group(1)), 'start': m.start(), 'heading_end': end})
    for i, sec in enumerate(sections):
        sec['index'] = i
        sec['end'] = sections[i+1]['start'] if i+1 < len(sections) else len(body)
    blocks = []
    for m in BEGIN.finditer(body):
        if m.start() not in command_offsets:
            continue
        env = m.group(1)
        close = re.search(r'\\end\s*\{' + re.escape(env) + r'\}', body[m.end():])
        if not close:
            raise ValueError('unclosed ' + env + ' environment')
        end = m.end() + close.end()
        content = body[m.end():m.end()+close.start()]
        labels = LABEL.findall(content)
        sec = next((s for s in sections if s['start'] <= m.start() < s['end']), None)
        blocks.append({'environment':env, 'label': labels[0] if labels else '',
                       'labels':labels, 'section':sec['label'] if sec else '',
                       'section_index':sec['index'] if sec else -1,
                       'start':m.start(), 'end':end, 'text':content})
    return {'source_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'body_text':body,
            'sections':sections, 'results':[b for b in blocks if b['environment'] in RESULTS],
            'proofs':[b for b in blocks if b['environment']=='proof'],
            'recalls':[b for b in blocks if b['environment']=='theoremrecall'],
            'labels':LABEL.findall(body),
            'citation_keys':sorted({k.strip() for m in CITE.finditer(body) for k in m.group(1).split(',')}),
            'has_placeholder':bool(PLACEHOLDER.search(body)),
            'statement_reference_sites':[{'result':b['label'], 'section':b['section'],
                'targets':sorted({v.strip() for m in REFERENCE.finditer(b['text']) for v in m.group(1).split(',')})}
                for b in blocks if b['environment'] in RESULTS and REFERENCE.search(b['text'])]}

def shape_issues(inv: dict) -> list[str]:
    """A targeted regression screen, with no per-section or total result quota."""
    secs = inv['sections']
    if len(secs) < 2:
        return []
    first = secs[0]['index']
    introductory = [r for r in inv['results'] if r['section_index']==first]
    body = [r for r in inv['results'] if r['section_index'] > first]
    if introductory and not body:
        return ['BODY_RESULTS_ABSENT: introductory results exist, but the substantive body has no explicit result; a context-only or proof-only exception requires a located review.']
    return []

def public_inventory(inv: dict) -> dict:
    return {k:v for k,v in inv.items() if k not in {'labels','citation_keys','body_text'}} | {
        'results':[{k:v for k,v in r.items() if k!='text'} for r in inv['results']],
        'proofs':[{k:v for k,v in r.items() if k!='text'} for r in inv['proofs']],
        'recalls':[{k:v for k,v in r.items() if k!='text'} for r in inv['recalls']]}

def safe_relative(value: str) -> bool:
    """Use one portable POSIX spelling; reject Windows drive/ADS and traversal."""
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and all(x not in {"", ".", ".."} for x in value.split("/"))

def checked_path(root: Path, value: str, context: str, errors: list[str]) -> Path | None:
    if not safe_relative(value):
        errors.append(f"{context}: unsafe relative path {value!r}")
        return None
    path = root / value
    try:
        resolved_path(path).relative_to(resolved_path(root))
    except ValueError:
        errors.append(f"{context}: path escapes project root: {value}")
        return None
    if not native_path(path).is_file():
        errors.append(f"{context}: missing file {value}")
        return None
    if native_path(path).stat().st_size == 0:
        errors.append(f"{context}: empty file {value}")
    return native_path(resolved_path(path))

def expand_tex(path: Path, project: Path, errors: list[str], main_dir: Path | None = None,
               stack: tuple[Path, ...] = ()) -> tuple[str, Counter[Path]]:
    path = native_path(resolved_path(path))
    main_dir = main_dir or path.parent
    if path in stack:
        errors.append(f"cyclic TeX input: {path.name}")
        return "", Counter()
    text = strip_comments(path.read_text(encoding="utf-8-sig"))
    consumed: Counter[Path] = Counter()

    def replace(match: re.Match[str]) -> str:
        value = match.group(1).strip()
        value = value if Path(value).suffix in {".tex", ".bbl"} else value + ".tex"
        if not safe_relative(value):
            errors.append(f"{path.name}: unsafe or nonliteral TeX input {value!r}")
            return ""
        target = main_dir / value
        try:
            relative = resolved_path(target).relative_to(resolved_path(project)).as_posix()
        except ValueError:
            errors.append(f"{path.name}: TeX input escapes project: {value}")
            return ""
        checked = checked_path(project, relative, path.name, errors)
        if checked is None:
            return ""
        consumed[checked] += 1
        nested, counts = expand_tex(checked, project, errors, main_dir, (*stack, path))
        consumed.update(counts)
        return "\n" + nested + "\n"

    expanded = INPUT_RE.sub(replace, text)
    if re.search(r"\\(?:input|include)\b", expanded):
        errors.append(f"{path.name}: unsupported input syntax; use literal braced input paths")
    return expanded, consumed
