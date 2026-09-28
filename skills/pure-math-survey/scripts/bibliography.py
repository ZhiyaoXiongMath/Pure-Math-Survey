#!/usr/bin/env python3
"""Generate bibliography companions; fingerprints only detect stale source review."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

IDENTITY_FIELDS = ('key', 'author', 'title', 'year', 'arxiv', 'version', 'doi', 'url', 'locator')

def review_fingerprint(record: dict) -> str:
    """Bind reviewed identity/version/locator, not the truth of the cited result."""
    payload = {key: record.get(key, '') for key in IDENTITY_FIELDS}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()

def validate_records(records: object, *, require_review: bool = True) -> list[dict]:
    if not isinstance(records, list) or not records:
        raise ValueError('Bibliography must be a nonempty JSON list')
    keys: set[str] = set()
    for r in records:
        if not isinstance(r, dict):
            raise ValueError('Each bibliography entry must be an object')
        for field in ('key', 'author', 'title', 'year'):
            if not isinstance(r.get(field), str) or not r[field].strip():
                raise ValueError(f'Missing textual bibliography field: {field}')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9:_-]*', r['key']):
            raise ValueError(f'Unsafe citation key: {r["key"]}')
        if r['key'] in keys:
            raise ValueError(f'Duplicate citation key: {r["key"]}')
        keys.add(r['key'])
        for field in IDENTITY_FIELDS + ('journal', 'volume', 'number', 'pages', 'note', 'display_author'):
            if field in r and not isinstance(r[field], str):
                raise ValueError(f'Bibliography field {field} must be text: {r["key"]}')
        arxiv = r.get('arxiv', '')
        if arxiv and not re.fullmatch(r'(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})v\d+', arxiv):
            raise ValueError(f'Pin an exact arXiv version: {r["key"]}')
        if arxiv and r.get('version') and not arxiv.endswith(r['version']):
            raise ValueError(f'Inconsistent arXiv version: {r["key"]}')
        if require_review:
            review = r.get('verification', {})
            if not isinstance(review, dict):
                raise ValueError(f'Source verification must be an object: {r["key"]}')
            try:
                if date.fromisoformat(review.get('date', '')).isoformat() != review.get('date'):
                    raise ValueError('non-ISO date')
            except (ValueError, TypeError):
                raise ValueError(f'Source review needs an actual ISO date: {r["key"]}')
            if not r.get('locator') or not isinstance(review.get('scope'), str) or not review['scope'].strip():
                raise ValueError(f'Missing source-review locator/date/scope: {r["key"]}')
            if review.get('fingerprint') != review_fingerprint(r):
                raise ValueError(f'Source review is stale: {r["key"]}; recheck identity/version/locator')
    return records

def generate(project: Path, *, require_review: bool = True) -> dict[str, str]:
    records = validate_records(json.loads((project/'references.json').read_text(encoding='utf-8')),
                               require_review=require_review)
    bib = ['% Generated from references.json; do not edit by hand.']
    bbl = [r'\begin{thebibliography}{99}']
    for r in records:
        fields = ('author', 'title', 'journal', 'volume', 'number', 'year', 'pages', 'doi', 'url', 'note')
        entries = [f'  {f} = {{{r[f]}}}' for f in fields if r.get(f)]
        if r.get('arxiv'):
            entries += [f'  eprint = {{{r["arxiv"]}}}', '  archivePrefix = {arXiv}']
        bib.append('@'+('article' if r.get('journal') else 'misc')+'{'+r['key']+',\n'+',\n'.join(entries)+'\n}')
        item = r'\bibitem{'+r['key']+'} '+r.get('display_author',r['author'])+', '
        item += r'\emph{'+r['title']+'}.'
        if r.get('journal'):
            item += ' '+r['journal']
            if r.get('volume'): item += r' \textbf{'+r['volume']+'}'
            item += ' ('+r['year']+')'
            if r.get('pages'): item += ', '+r['pages']
            item += '.'
        else:
            item += ' Preprint ('+r['year']+').'
        if r.get('arxiv'):
            item += r' \href{https://arxiv.org/abs/'+r['arxiv']+'}{\\nolinkurl{arXiv:'+r['arxiv']+'}}.'
        elif r.get('doi'):
            item += r' \href{https://doi.org/'+r['doi']+'}{\\nolinkurl{doi:'+r['doi']+'}}.'
        elif r.get('url'):
            item += r' \href{'+r['url']+'}{Source}.'
        if r.get('note'): item += ' '+r['note']
        bbl.append(item)
    bbl.append(r'\end{thebibliography}')
    result = {'references.bib':'\n\n'.join(bib)+'\n', 'references.bbl':'\n\n'.join(bbl)+'\n'}
    for name, content in result.items(): (project/name).write_text(content,encoding='utf-8')
    return result

def main() -> int:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from survey_core.adapters import dispatch
    native = dispatch('bibliography.py', sys.argv[1:])
    if native is not None: return native
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('project',type=Path)
    p.add_argument('--check',action='store_true',help='Validate fingerprints without writing companions')
    args=p.parse_args()
    try:
        if args.check:
            refs=validate_records(json.loads((args.project/'references.json').read_text(encoding='utf-8')))
            print(f'{len(refs)} source-review fingerprints match; NOT a mathematical verification')
        else:
            generate(args.project)
            print('Generated references.bib and references.bbl from reviewed records')
    except (OSError, ValueError, TypeError) as exc:
        p.exit(1, f'Bibliography check failed: {exc}\n')
    return 0
if __name__=='__main__': raise SystemExit(main())
