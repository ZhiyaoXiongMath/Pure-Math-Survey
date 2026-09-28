"""Shared diagnostics, safe paths, deterministic bytes and atomic single-writer I/O."""
from __future__ import annotations
import contextlib
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
from typing import Any, Iterator

# VERSION is the stable on-disk contract, not the executable release.
VERSION = '2.0.0'
SOFTWARE_VERSION = '2.0.2'
SKILL_ROOT = Path(__file__).resolve().parents[2]
FONT_SUFFIXES = {'.ttf', '.otf', '.ttc', '.woff', '.woff2', '.pfb', '.pfa'}

class SurveyError(Exception):
    def __init__(self, code: str, message: str, path: str = '', node_id: str | None = None, exit_code: int = 2):
        super().__init__(message)
        self.diagnostic = diagnostic(code, message, path, node_id)
        self.exit_code = exit_code

def diagnostic(code: str, message: str, path: str = '', node_id: str | None = None) -> dict:
    return {'code': code, 'path': str(path), 'node_id': node_id, 'message': message}

def require(ok: Any, code: str, message: str, path: str = '', node_id: str | None = None) -> None:
    if not ok:
        raise SurveyError(code, message, path, node_id)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def _pairs(pairs: list) -> dict:
    out = {}
    for k, v in pairs:
        require(k not in out, 'DUPLICATE_JSON_KEY', f'Duplicate JSON key: {k}')
        out[k] = v
    return out

def decode(text: str, path: str = '') -> Any:
    try:
        return json.loads(text, object_pairs_hook=_pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
    except (ValueError, TypeError) as e:
        raise SurveyError('JSON_INVALID', str(e), path) from e

def read_json(path: Path) -> Any:
    return decode(path.read_text(encoding='utf-8'), path.name)

def relative(value: Any) -> str:
    require(isinstance(value, str) and value and '\\' not in value and ':' not in value and '\x00' not in value,
            'UNSAFE_PATH', 'Expected a nonempty relative POSIX path', str(value))
    p = PurePosixPath(value)
    require(not p.is_absolute() and all(s not in ('', '.', '..') for s in value.split('/')), 'UNSAFE_PATH', 'Path escapes or aliases project', value)
    return value

def safe(root: Path, value: str, exists: bool = False) -> Path:
    value = relative(value)
    root = root.absolute()
    require(not root.is_symlink(), 'UNSAFE_PATH', 'Project root is a symlink', root.name)
    p = root
    for part in PurePosixPath(value).parts:
        p /= part
        require(not p.is_symlink(), 'UNSAFE_PATH', 'Symlink is not allowed', value)
    require(root.resolve() == p.resolve() or root.resolve() in p.resolve().parents,
            'UNSAFE_PATH', 'Resolved path escapes root', value)
    if exists:
        require(p.is_file(), 'UNKNOWN_REFERENCE', 'Referenced file is missing', value)
    return p

def relpath(root: Path, value: str | Path) -> str:
    p = Path(value)
    if p.is_absolute():
        try:
            value = p.absolute().relative_to(root.absolute()).as_posix()
        except ValueError as e:
            raise SurveyError('UNSAFE_PATH', 'File is outside project', p.name) from e
    else:
        # Existing cwd-relative CLI paths may include the project folder.
        try:
            if p.is_file():
                value = p.absolute().relative_to(root.absolute()).as_posix()
        except ValueError:
            pass
    return relative(str(value))

def file_hash(root: Path, path: str) -> str:
    return sha(safe(root, path, True).read_bytes())

def file_inventory(root: Path, paths: list[str]) -> list[dict]:
    return [{'path': p, 'sha256': file_hash(root, p), 'bytes': safe(root, p, True).stat().st_size} for p in sorted(set(paths))]

def all_files(root: Path, prefix: str = '') -> list[str]:
    base = safe(root, prefix) if prefix else root
    if not base.exists():
        return []
    result = []
    for p in sorted(base.rglob('*')):
        require(not p.is_symlink(), 'UNSAFE_PATH', 'Symlink found', p.relative_to(root).as_posix())
        if p.is_file():
            result.append(p.relative_to(root).as_posix())
    return result

def atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(data); out.flush(); os.fsync(out.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def write_json(path: Path, value: Any) -> None:
    atomic_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))

@contextlib.contextmanager
def writer(root: Path) -> Iterator[None]:
    """An interrupted process can leave a lock; investigate PID before removing it."""
    root.mkdir(parents=True, exist_ok=True)
    lock = root / '.survey-write.lock'
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as e:
        raise SurveyError('WRITER_LOCKED', 'Another writer or interrupted lock exists; inspect before removal', lock.name, exit_code=4) from e
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(json.dumps({'pid': os.getpid(), 'started_at': now()}))
        yield
    finally:
        lock.unlink(missing_ok=True)

def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()

def valid_date(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            return dt.date.fromisoformat(value) <= (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=14)).date()
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed <= dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5)
    except ValueError:
        return False

def identifier(value: Any, prefix: str | None = None) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', value)) and (prefix is None or value.startswith(prefix))

def result(operation: str, status: str, artifacts: Any = None, errors: list | None = None, warnings: list | None = None) -> dict:
    return {'operation': operation, 'status': status, 'errors': errors or [], 'warnings': warnings or [], 'artifacts': artifacts or {}}
