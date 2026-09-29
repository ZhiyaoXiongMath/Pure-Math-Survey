#!/usr/bin/env python3
"""Export the balanced article as a standalone TeX and its unchanged PDF."""
from __future__ import annotations

import argparse
from pathlib import Path
import stat
import zipfile

SAMPLE = Path(__file__).resolve().parents[1] / "skills/pure-math-survey/assets/reference-samples/dhym-balanced"
STEM = "dhym-survey-revised"


def standalone_tex() -> bytes:
    source = (SAMPLE / f"{STEM}.tex").read_text(encoding="utf-8")
    style = (SAMPLE / "math-review.sty").read_text(encoding="utf-8")
    bibliography = (SAMPLE / f"{STEM}.bbl").read_text(encoding="utf-8")
    # Package declarations and unused authoring scaffolds do not belong in an article.
    style = style.split(r"\newcommand{\placeholder}", 1)[0]
    style = "\n".join(
        line for line in style.splitlines()
        if not line.lstrip().startswith(("%", r"\NeedsTeXFormat", r"\ProvidesPackage"))
    ).strip()
    package = r"\usepackage{math-review}"
    bib_commands = "\\bibliographystyle{amsplain}\n\\bibliography{references}"
    if source.count(package) != 1 or source.count(bib_commands) != 1:
        raise ValueError("Unexpected article dependencies; review the standalone export")
    embedded_style = "\\makeatletter\n" + style + "\n\\makeatother"
    embedded_bibliography = "\\bibliographystyle{amsplain}\n" + bibliography.rstrip()
    exported = source.replace(package, embedded_style).replace(bib_commands, embedded_bibliography)
    # Only dependency inclusion changes: all original article text is recoverable.
    recovered = exported.replace(embedded_style, package).replace(embedded_bibliography, bib_commands)
    if recovered != source:
        raise ValueError("The export changed article text")
    return exported.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(SAMPLE.resolve()):
        raise ValueError("Keep exports outside the frozen sample directory")
    members = {
        f"{STEM}.tex": standalone_tex(),
        f"{STEM}.pdf": (SAMPLE / f"{STEM}.pdf").read_bytes(),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 29, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, data)
    print(f"Created {output}: {', '.join(members)}")


if __name__ == "__main__":
    main()
