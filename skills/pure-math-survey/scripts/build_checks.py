#!/usr/bin/env python3
"""Compile supplied templates and retained examples; not a survey-quality grader.

Requires pdfLaTeX and its document packages. Uses no shell escape, works only on
copied inputs, and reports final log problems separately from PDF rendering.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
BLOCKING_PATTERNS = {
    "undefined_reference": r"(?:Reference|Citation) .+? undefined|There were undefined references",
    "duplicate_label": r"multiply[- ]defined|destination with the same identifier",
    "missing_glyph": r"Missing character:",
    "overflow": r"Overfull \\[hv]box",
    "fatal": r"^! |Fatal error|Emergency stop",
    "unstable_references": r"Rerun to get|Rerun LaTeX|Please \(re\)run",
}

def log_issues(text: str) -> dict[str, list[str]]:
    return {kind: [line for line in text.splitlines() if re.search(pattern, line)]
            for kind, pattern in BLOCKING_PATTERNS.items()
            if any(re.search(pattern, line) for line in text.splitlines())}

def log_warnings(text: str) -> dict[str, list[str]]:
    patterns = {
        'underfull_box': r'Underfull \\[hv]box',
        'font_substitution': r'Font Warning|Font shape .+not available|Some font shapes were not available|size substitutions',
        'package_warning': r'(?:LaTeX|Package \S+) Warning',
    }
    return {kind: found for kind, pattern in patterns.items()
            if (found := [line for line in text.splitlines() if re.search(pattern, line)])}


def auxiliary_digest(folder: Path, stem: str) -> str:
    h = hashlib.sha256()
    for suffix in (".aux", ".toc", ".out"):
        p = folder / (stem + suffix)
        h.update(suffix.encode())
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()

def compile_one(folder: Path, entrypoint: str, engine: str, timeout: int = 120) -> dict:
    path = folder / entrypoint
    if not path.is_file() or path.suffix != ".tex":
        raise ValueError(f"Missing TeX entrypoint: {path}")
    command = [engine, "-no-shell-escape", "-interaction=nonstopmode",
               "-halt-on-error", "-file-line-error", entrypoint]
    previous = None
    stable = False
    passes = 0
    for passes in range(1, 6):
        proc = subprocess.run(command, cwd=folder, text=True, encoding="utf-8",
                              errors="replace", capture_output=True, timeout=timeout)
        (folder / f"build-pass-{passes}.txt").write_text(proc.stdout + proc.stderr, encoding="utf-8")
        if proc.returncode:
            raise RuntimeError(f"TeX failed for {entrypoint} on pass {passes}; see {folder}")
        digest = auxiliary_digest(folder, path.stem)
        if passes >= 2 and previous == digest:
            stable = True
            break
        previous = digest
    log = (folder / (path.stem + ".log")).read_text(encoding="utf-8", errors="replace")
    issues = log_issues(log)
    if not stable:
        issues["unstable_auxiliary_files"] = ["Auxiliary files changed through five passes"]
    pdf = folder / (path.stem + ".pdf")
    if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
        issues["missing_pdf"] = [str(pdf)]
    pages = re.search(r"Output written on .*?\((\d+) pages?", log, re.S)
    recalls = {}
    for key in ("PMS-RECALL", "PMS-GRADIENT-RECALL"):
        before = re.findall(re.escape(key) + r"-BEFORE=(\d+)", log)
        after = re.findall(re.escape(key) + r"-AFTER=(\d+)", log)
        if before or after:
            recalls[key] = {"before": before, "after": after}
            if before != after:
                issues.setdefault("recall_counter", []).append(key + " changed its theorem counter")
    return {"entrypoint": entrypoint, "passes": passes, "auxiliary_stable": stable,
            "pages_from_log": int(pages.group(1)) if pages else None,
            "pdf": str(pdf), "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None,
            "blocking_log_issues": issues,
            "nonblocking_log_warnings": log_warnings(log),
            "warning_disposition": "REQUIRES_CONTEXTUAL_REVIEW" if log_warnings(log) else "NONE_REPORTED",
            "font_fallback": "STIX2 unavailable" in log,
            "underfull_box_count": len(re.findall(r"Underfull \\[hv]box", log)),
            "recall_counters": recalls,
            "status": "PASS" if not issues else "FAIL"}

def stage_balanced_sample(root: Path, destination: Path, *, mode: Literal["current", "frozen"]) -> Path:
    """Stage explicit dependencies; do not confuse regression with reproduction."""
    if mode not in ("current", "frozen"):
        raise ValueError(f"Unsupported style mode: {mode}")
    sample = root / "assets/reference-samples/dhym-balanced"
    style = (root / "assets/templates/math-review.sty" if mode == "current"
             else sample / "math-review.sty")
    inputs = [sample / "dhym-survey-revised.tex", sample / "dhym-survey-revised.bbl",
              sample / "references.bib", style]
    for source in inputs:
        if not source.is_file():
            raise FileNotFoundError(source)
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"Staging destination must be empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    for source in inputs:
        shutil.copy2(source, destination / source.name)
    return destination / "dhym-survey-revised.tex"

def run_checks(output: Path, engine: str = "pdflatex") -> dict:
    engine_path = shutil.which(engine)
    if not engine_path:
        raise FileNotFoundError(f"TeX engine not found: {engine}")
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Output directory must be new or empty; prior evidence is not overwritten")
    if output.resolve().is_relative_to(ROOT):
        raise ValueError("Build output must be outside the installed skill tree")
    output.mkdir(parents=True, exist_ok=True)
    version = subprocess.run([engine_path, "--version"], capture_output=True, text=True,
                             check=True, timeout=20).stdout.splitlines()[0]
    report = {"scope": "maintenance builds; not new research-survey generation or mathematical review",
              "engine": version, "command_flags": ["-no-shell-escape", "-interaction=nonstopmode",
                                                    "-halt-on-error", "-file-line-error"],
              "visual_review": "NOT_PERFORMED_BY_THIS_SCRIPT", "builds": []}
    style = ROOT / "assets/templates/math-review.sty"
    tasks: list[tuple[Path, str]] = []
    folder = output / "exposition-smoke"
    folder.mkdir()
    for fixture in (ROOT / "assets/exposition-examples").glob("*.tex"):
        shutil.copy2(fixture, folder / fixture.name)
    shutil.copy2(style, folder / style.name)
    tasks.append((folder, "exposition-smoke.tex"))
    for mode in ("current", "frozen"):
        folder = output / f"balanced-{mode}"
        entry = stage_balanced_sample(ROOT, folder, mode=mode)
        tasks.append((folder, entry.name))
    for folder, entry in tasks:
        print(f"Building {entry}", flush=True)
        try:
            result = compile_one(folder, entry, engine_path)
        except (OSError, ValueError, subprocess.SubprocessError, RuntimeError) as exc:
            result = {"entrypoint": entry, "status": "FAIL", "error": str(exc)}
        result["artifact_kind"] = ("elementary_example" if entry.startswith("exposition") else
                                   "shared_style_regression" if folder.name == "balanced-current" else
                                   "frozen_sample_reproduction")
        result["target"] = folder.name
        if entry == "dhym-survey-revised.tex":
            result["style_mode"] = folder.name.rsplit("-", 1)[-1]
            result["style_sha256"] = hashlib.sha256((folder / "math-review.sty").read_bytes()).hexdigest()
        # Findings are reader-review pointers, not a mathematical build verdict.
        # Use the same literal-input expansion path as project validation.
        try:
            from survey_core import structure
            input_errors = []
            expanded, _ = structure.expand_tex(folder / entry, folder, input_errors)
            inv = structure.inventory(expanded)
            result["source_structure_screen"] = {
                "scope": "syntax and reference sites only; whole-body reader review remains necessary",
                "input_errors": input_errors,
                "findings": structure.shape_issues(inv),
                "statement_reference_sites": inv["statement_reference_sites"],
                "source_sha256": inv["source_sha256"],
            }
        except (OSError, ValueError, TypeError) as exc:
            result["source_structure_screen"] = {"error": str(exc)}
        report["builds"].append(result)
        (output / "build-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    report["status"] = "PASS" if all(x["status"] == "PASS" for x in report["builds"]) else "FAIL"
    (output / "build-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--engine", default="pdflatex", choices=["pdflatex"])
    args = parser.parse_args()
    try:
        report = run_checks(args.output.resolve(), args.engine)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Build checks unavailable: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": report["status"], "build_count": len(report["builds"]),
                      "report": str(args.output / "build-report.json")}, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
