"""Literal TeX inventories used by current output and sample checks."""
from __future__ import annotations
import hashlib
import re
from collections import Counter
from pathlib import Path, PurePosixPath

RESULTS = {'theorem', 'proposition', 'lemma', 'corollary'}
LABEL = re.compile(r'\\label\s*\{([^{}]+)\}')
BEGIN = re.compile(r'\\begin\s*\{(theorem|proposition|lemma|corollary|proof|theoremrecall)\}')
SECTION = re.compile(r'\\section(\*)?\s*(?:\[[^\]]*\]\s*)?\{')
CITE = re.compile(r'\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^{}]+)\}')
REFERENCE = re.compile(r'\\(?:eqref|ref|pageref|nameref|autoref|cref|Cref)\s*\{([^{}]+)\}')
PLACEHOLDER = re.compile(r'\\placeholder\b|\b(?:PENDING|TODO|TBD)\b|\[INSERT', re.I)


INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")

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
    text = strip_comments(expanded)
    # Inventory numbers are offsets in the body, not source-file line claims.
    body = text.split(r'\begin{document}', 1)[-1].split(r'\end{document}', 1)[0]
    sections = []
    for m in SECTION.finditer(body):
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
        path.resolve().relative_to(root.resolve())
    except ValueError:
        errors.append(f"{context}: path escapes project root: {value}")
        return None
    if not path.is_file():
        errors.append(f"{context}: missing file {value}")
        return None
    if path.stat().st_size == 0:
        errors.append(f"{context}: empty file {value}")
    return path.resolve()

def expand_tex(path: Path, project: Path, errors: list[str], main_dir: Path | None = None,
               stack: tuple[Path, ...] = ()) -> tuple[str, Counter[Path]]:
    path = path.resolve()
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
            relative = target.resolve().relative_to(project.resolve()).as_posix()
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
