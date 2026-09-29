#!/usr/bin/env python3
"""Create and re-open a single-root skill ZIP with member and archive checksums.

Does not install the skill or mutate the source tree. No font files are bundled.
"""
from __future__ import annotations
import argparse
import hashlib
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
FONT_SUFFIXES = {".otf", ".ttf", ".ttc", ".woff", ".woff2", ".pfa", ".pfb"}
IGNORED_DIRS = {".git", "__pycache__", ".pytest_cache", ".DS_Store"}
GENERATED_SUFFIXES = {".pyc", ".aux", ".log", ".toc", ".out", ".fls", ".fdb_latexmk", ".synctex.gz"}
CHECKSUM_NAME = "artifact-checksums.txt"
REQUIRED_FILES = {
    'LICENSE',
    'README.md',
    'SKILL.md',
    'agents/openai.yaml',
    'assets/exposition-examples/README.md',
    'assets/exposition-examples/exposition-smoke.tex',
    'assets/exposition-examples/gradient-body.tex',
    'assets/exposition-examples/quadratic-body.tex',
    'assets/rebuild/rebuild.py',
    'assets/reference-samples/dhym-balanced/README.md',
    'assets/reference-samples/dhym-balanced/dhym-survey-revised.bbl',
    'assets/reference-samples/dhym-balanced/dhym-survey-revised.pdf',
    'assets/reference-samples/dhym-balanced/dhym-survey-revised.tex',
    'assets/reference-samples/dhym-balanced/math-review.sty',
    'assets/reference-samples/dhym-balanced/provenance.json',
    'assets/reference-samples/dhym-balanced/references.bib',
    'assets/templates/math-review.sty',
    'assets/templates/profile-lecture.tex',
    'assets/templates/profile-minimal.tex',
    'assets/templates/profile-thematic.tex',
    'assets/v2/empty-project/knowledge/conventions.tex',
    'assets/v2/empty-project/knowledge/coverage.json',
    'assets/v2/empty-project/knowledge/discovery.md',
    'assets/v2/empty-project/knowledge/overview.md',
    'assets/v2/empty-project/project.json',
    'assets/v2/empty-project/scope.md',
    'references/architecture.md',
    'references/contracts.md',
    'references/core-problems.md',
    'references/editions.md',
    'references/exposition-examples.md',
    'references/introduction.md',
    'references/layout-and-build.md',
    'references/length-and-selection.md',
    'references/output-review.md',
    'references/part-v-benchmark.md',
    'references/problem-formulation.md',
    'references/proofs-and-boundaries.md',
    'references/records-and-delivery.md',
    'references/research-and-evidence.md',
    'references/template-maintenance.md',
    'references/validation.md',
    'references/writing-style.md',
    'scripts/build_checks.py',
    'scripts/compare_pdf.py',
    'scripts/package_release.py',
    'scripts/survey.py',
    'scripts/survey_core/__init__.py',
    'scripts/survey_core/build.py',
    'scripts/survey_core/cli.py',
    'scripts/survey_core/common.py',
    'scripts/survey_core/dependencies.py',
    'scripts/survey_core/exports.py',
    'scripts/survey_core/history.py',
    'scripts/survey_core/knowledge.py',
    'scripts/survey_core/models.py',
    'scripts/survey_core/plans.py',
    'scripts/survey_core/readiness.py',
    'scripts/survey_core/release.py',
    'scripts/survey_core/reviews.py',
    'scripts/survey_core/snapshots.py',
    'scripts/survey_core/structure.py',
    'scripts/survey_core/tex.py',
    'scripts/validate_assets.py',
}


def runtime_member(name: str) -> bool:
    """Only explicitly supported current runtime resources are distributable."""
    return name in REQUIRED_FILES or name == CHECKSUM_NAME


def safe_name(name: str) -> bool:
    return (bool(name) and "\\" not in name and ":" not in name and "\x00" not in name
            and not PurePosixPath(name).is_absolute()
            and all(p not in {"", ".", ".."} for p in name.split("/")))


def selected_files(root: Path) -> dict[str, bytes]:
    if not (root / "SKILL.md").is_file():
        raise ValueError("Source root must contain SKILL.md")
    selected = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if p.is_symlink():
            raise ValueError(f"Symlink is not allowed in release: {rel}")
        if not p.is_file():
            continue
        if not safe_name(rel.as_posix()):
            raise ValueError(f"Unsafe release path: {rel}")
        if p.suffix.lower() in FONT_SUFFIXES:
            raise ValueError(f"Font file must not be shared: {rel}")
        if p.suffix in GENERATED_SUFFIXES or p.name.endswith(".synctex.gz") or p.name == CHECKSUM_NAME:
            continue
        if not runtime_member(rel.as_posix()):
            raise ValueError(f"Unsupported file in skill tree; review before packaging: {rel}")
        selected[rel.as_posix()] = p.read_bytes()
    missing = REQUIRED_FILES - set(selected)
    if missing:
        raise ValueError(f"Missing required resources: {sorted(missing)}")
    return selected


def verify_archive(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate archive member")
        for info in infos:
            if not safe_name(info.filename) or info.is_dir():
                raise ValueError("Unsafe or unexpected directory member")
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Symlink archive member")
            if Path(info.filename).suffix.lower() in FONT_SUFFIXES:
                raise ValueError("Font archive member")
        if not names or {n.split('/')[0] for n in names} != {"pure-math-survey"}:
            raise ValueError("Expected exactly the pure-math-survey top-level folder")
        prefix = "pure-math-survey/"
        checksum_path = prefix + CHECKSUM_NAME
        if checksum_path not in names:
            raise ValueError("Missing member checksums")
        expected = {}
        for line in archive.read(checksum_path).decode("utf-8").splitlines():
            digest, sep, relative = line.partition("  ")
            if not sep or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest) or not safe_name(relative):
                raise ValueError("Invalid checksum line")
            if relative in expected:
                raise ValueError("Duplicate checksum entry")
            expected[relative] = digest
        actual = {n[len(prefix):] for n in names if n != checksum_path}
        if set(expected) != actual:
            raise ValueError("Archive members and checksum list disagree")
        if REQUIRED_FILES - actual:
            raise ValueError("Archive lacks required skill resources")
        if any(not runtime_member(name) for name in actual):
            raise ValueError("Unsupported resource in archive")
        for relative, digest in expected.items():
            if hashlib.sha256(archive.read(prefix + relative)).hexdigest() != digest:
                raise ValueError(f"Checksum mismatch: {relative}")
        if archive.testzip() is not None:
            raise ValueError("Archive CRC failure")
    return {"members": len(names), "verified_member_hashes": len(expected),
            "archive_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def package(root: Path, output: Path, force: bool = False) -> dict:
    root = root.resolve(); output = output.resolve()
    if output.is_relative_to(root):
        raise ValueError("Archive must be outside the source skill tree")
    checksum_output = output.with_suffix(output.suffix + ".sha256")
    if (output.exists() or checksum_output.exists()) and not force:
        raise FileExistsError("Archive exists; use --force for an intentional rebuild")
    selected = selected_files(root)
    checksums = ''.join(f"{hashlib.sha256(data).hexdigest()}  {rel}\n" for rel, data in selected.items())
    selected[CHECKSUM_NAME] = checksums.encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix="." + output.name + ".", suffix=".tmp", dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for relative, data in sorted(selected.items()):
                info = zipfile.ZipInfo("pure-math-survey/" + relative, date_time=(2026, 9, 27, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                z.writestr(info, data)
        report = verify_archive(temporary)
        temporary.replace(output)
    finally:
        if temporary.exists():
            temporary.unlink()
    checksum_output.write_text(
        report["archive_sha256"] + "  " + output.name + "\n", encoding="ascii")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        report = package(args.root, args.output, args.force)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"Package failed: {exc}", file=sys.stderr)
        return 1
    print(f"Verified {report['members']} members; SHA-256 {report['archive_sha256']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
