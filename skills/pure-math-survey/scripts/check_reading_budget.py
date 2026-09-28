#!/usr/bin/env python3
"""Report reading length without making default guidance a publication gate.

Exit 0: valid measurement (including REVIEW_NEEDED); 1: an explicitly configured
user max_pages is exceeded; 2: invalid inputs or unavailable PDF measurement.
The historical command name and page_review_limit input remain supported.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

# These are editorial review triggers, never targets, quotas or automatic limits.
CONCISE = {1: 5, 2: 6, 3: 6, 4: 5, 5: 10}
STANDARD = {1: 8, 2: 10, 3: 10, 4: 8, 5: 16}


def safe_file(root: Path, value: str) -> Path:
    if (not isinstance(value, str) or not value or '\\' in value or ':' in value
            or '\x00' in value or PurePosixPath(value).is_absolute()
            or any(x in {'', '.', '..'} for x in value.split('/'))):
        raise ValueError('Expected a portable, nonempty project-relative PDF path')
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or path.suffix.lower() != '.pdf':
        raise ValueError('PDF must be within the project and have a .pdf extension')
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def positive_integer(value: object, name: str) -> int:
    if type(value) is not int or value < 1:
        raise ValueError(f'{name} must be a positive integer, not a boolean')
    return value


def document_key(doc: object) -> tuple[int, str]:
    if not isinstance(doc, dict):
        raise ValueError('Each document selection must be an object')
    part, edition = doc.get('part'), doc.get('edition')
    if type(part) is not int or part not in CONCISE or edition not in ('concise', 'standard'):
        raise ValueError('Unknown part or edition')
    return part, edition


def review_threshold(doc: dict) -> int:
    part, edition = document_key(doc)
    default = (CONCISE if edition == 'concise' else STANDARD)[part]
    new = doc.get('page_review_threshold', default)
    old = doc.get('page_review_limit', default)
    if 'page_review_threshold' in doc:
        positive_integer(new, 'page_review_threshold')
    if 'page_review_limit' in doc:
        positive_integer(old, 'page_review_limit')
    if ('page_review_threshold' in doc and 'page_review_limit' in doc and new != old):
        raise ValueError('Conflicting page_review_threshold and legacy page_review_limit')
    return positive_integer(new if 'page_review_threshold' in doc else old,
                            'page_review_threshold')


def check(root: Path) -> dict:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError('Reading-length measurement requires PyMuPDF; no PDF was measured') from exc
    root = root.resolve()
    manifest = json.loads((root / 'project-manifest.json').read_text(encoding='utf-8-sig'))
    if not isinstance(manifest, dict):
        raise ValueError('project-manifest.json must be an object')
    documents = manifest.get('documents')
    if not isinstance(documents, list) or not documents:
        raise ValueError('documents must be a nonempty list')
    keys = [document_key(doc) for doc in documents]
    if len(keys) != len(set(keys)):
        raise ValueError('Repeated part/edition')
    if 'requested_documents' in manifest:
        requested = manifest['requested_documents']
        if not isinstance(requested, list) or not requested:
            raise ValueError('requested_documents must be a nonempty list of objects')
        if any(not isinstance(d, dict) or set(d) != {'part', 'edition'} for d in requested):
            raise ValueError('requested_documents entries contain exactly part and edition')
        pairs = [document_key(doc) for doc in requested]
        if len(pairs) != len(set(pairs)) or set(keys) != set(pairs):
            raise ValueError('Document selection differs from requested_documents or is repeated')
    rows, seen_paths = [], set()
    for doc, (part, edition) in zip(documents, keys):
        threshold = review_threshold(doc)
        maximum = doc.get('max_pages')
        if 'max_pages' in doc:
            positive_integer(maximum, 'max_pages (explicit user limit)')
        path = safe_file(root, doc.get('pdf_file'))
        if path in seen_paths:
            raise ValueError('Distinct requested documents must not reuse the same PDF')
        seen_paths.add(path)
        try:
            with fitz.open(path) as pdf:
                if not pdf.is_pdf or pdf.is_encrypted or pdf.page_count < 1:
                    raise ValueError('Expected a nonempty, readable, unencrypted PDF')
                pages = pdf.page_count
                repaired = pdf.is_repaired
        except RuntimeError as exc:
            raise ValueError(f'PDF could not be read: {doc.get("pdf_file")}: {exc}') from exc
        over = pages > threshold
        exceeded = maximum is not None and pages > maximum
        rows.append({'part': part, 'edition': edition, 'pdf': doc['pdf_file'],
                     'pdf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'pages': pages, 'page_review_threshold': threshold,
                     # Read-only output alias for existing report consumers.
                     'page_review_limit': threshold, 'max_pages': maximum,
                     'review_needed': over, 'blocking': exceeded,
                     'status': ('PAGE_LIMIT_EXCEEDED' if exceeded else
                                'REVIEW_NEEDED' if over else 'WITHIN_GUIDANCE'),
                     'warnings': ['PDF structure was repaired by the reader; rebuild and inspect it'] if repaired else []})
    blocked = any(row['blocking'] for row in rows)
    return {'schema_version': '1.0.0',
            'scope': 'Total PDF pages including references; not a content or visual grade',
            'status': ('PAGE_LIMIT_EXCEEDED' if blocked else
                       'REVIEW_NEEDED' if any(r['review_needed'] for r in rows) else 'WITHIN_GUIDANCE'),
            'blocking': blocked,
            'guidance': ('Default thresholds request an editorial reread, not fewer mathematical statements. '
                         'Only max_pages explicitly supplied by the user is a page-count gate.'),
            'documents': rows}


def exit_code(report: dict) -> int:
    return 1 if report['blocking'] else 0


def main() -> int:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from survey_core.adapters import dispatch
    native = dispatch('check_reading_budget.py', sys.argv[1:])
    if native is not None: return native
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    try:
        report = check(args.project)
    except (OSError, ValueError, KeyError, TypeError, ImportError, RuntimeError) as exc:
        print(json.dumps({'status': 'ERROR', 'blocking': True, 'error': str(exc)}))
        return 2
    print(json.dumps(report, indent=2))
    return exit_code(report)


if __name__ == '__main__':
    raise SystemExit(main())
