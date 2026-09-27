#!/usr/bin/env python3
"""Check publication files and evidence links, not mathematical truth or completeness.

Only literal, braced \\input/\\include commands are supported. Input paths are
resolved relative to the main document directory, as when TeX runs there.
"""
from __future__ import annotations

import argparse
import importlib.util
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath

SCHEMA_VERSION = "1.0.0"
EDITIONS = {"concise", "standard"}
COMBINATIONS = {(part, edition) for part in range(1, 6) for edition in EDITIONS}
MAP_FIELDS = {
    "node_id", "kind", "owner_part", "canonical_component", "source_ids", "proof_ids",
    "concise_file", "concise_label", "standard_file", "standard_label",
    "concise_treatment", "standard_treatment", "limitation_note",
}
INTEGRATED_MAP_FIELDS = {
    f"integrated_{edition}_{field}"
    for edition in EDITIONS for field in ("file", "label", "treatment")
}
TREATMENTS = {"FULL_STATEMENT", "REFERENCE_ONLY", "OMITTED_WITH_REASON"}
PASS_STATUSES = {"PASS", "VERIFIED", "COMPLETE"}
REQUIRED_AUDITS = {"source_identity", "statement_verification", "proof_depth",
                   "reader_outcomes", "edition_depth",
                   "edition_semantic_consistency", "frontier_status", "archive_integrity"}
REQUESTED_DOCUMENT_AUDITS = {"build_requested_documents", "visual_requested_documents"}
PART_III_AUDITS = {"proof_framework", "decisive_mechanisms"}
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\s*\{([^}]+)\}")
PLACEHOLDER_RE = re.compile(
    r"\\placeholder\s*\{|\\templatereferences\b|<(?:TOPIC|TITLE|INSERT|REPLACE)[^>]*>|"
    r"\[(?:INSERT|REPLACE|TODO|TBD|TITLE|TOPIC|Review topic|Author name|Prepared date)(?:\b|:)[^]]*\]|"
    r"\b(?:TODO|TBD|Lorem ipsum)\b",
    re.I,
)
AUDIT_ENV_RE = re.compile(
    r"\\begin\{(?:anchortheorembox|theoremdossierbox|anchorstatement|anchormetadata|"
    r"dossiermetadata|evidencebox|auditcard)\}|\\(?:MetadataField|StatementField)\s*\{",
    re.I,
)
AUDIT_FIELD_RE = re.compile(
    r"(?mi)^\s*(?:\\(?:textbf|textit)\{)?(?:Verification depth|Publication status|"
    r"Logical type|Source ID|Proof ID|Theorem ID|Provenance status|Audit status)"
    r"(?:\})?\s*[:.]"
)


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


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        result = []
        slashes = 0
        for char in line:
            if char == "%" and slashes % 2 == 0:
                break
            result.append(char)
            slashes = slashes + 1 if char == "\\" else 0
        lines.append("".join(result))
    return "\n".join(lines)


def read_csv(path: Path, required: set[str], errors: list[str]) -> list[dict[str, str]]:
    if not path.is_file():
        errors.append(f"missing required file: {path.name}")
        return []
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            header = reader.fieldnames or []
            if len(header) != len(set(header)):
                errors.append(f"{path.name}: duplicate CSV columns")
            if not required.issubset(header):
                errors.append(f"{path.name}: missing columns {sorted(required - set(header))}")
            rows = list(reader)
        for number, row in enumerate(rows, 2):
            if None in row or any(value is None for value in row.values()):
                errors.append(f"{path.name}:{number}: row width does not match header")
        return rows
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(f"{path.name}: {exc}")
        return []


def ids(value: str) -> set[str]:
    return {x.strip() for x in re.split(r"[;,]", value or "") if x.strip()}


def registry_ids(rows: list[dict[str, str]], field: str, filename: str, errors: list[str]) -> set[str]:
    found: set[str] = set()
    for row in rows:
        value = (row.get(field) or "").strip()
        if not value:
            errors.append(f"{filename}: empty {field}")
        elif value in found:
            errors.append(f"{filename}: duplicate {field} {value}")
        found.add(value)
    return found - {""}


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


def public_leaks(text: str) -> list[str]:
    body = text.split(r"\begin{document}", 1)[-1]
    # Labels, references, citations and input paths are coordinates, not visible IDs.
    visible = re.sub(r"\\(?:label|ref|eqref|pageref|autoref|cite|input|include)\s*(?:\[[^]]*\])?\{[^}]*\}", "", body)
    problems = []
    if AUDIT_ENV_RE.search(body) or AUDIT_FIELD_RE.search(body):
        problems.append("reader-facing audit card or metadata field")
    id_heading = re.compile(
        r"\\(?:part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\{[^}]*\b[TPS]\d{2,}\b[^}]*\}"
        r"|\\begin\{(?:theorem|lemma|proposition|corollary|definition|example|counterexample|remark|conjecture|question|problem)\}\s*\[[^]]*\b[TPS]\d{2,}\b[^]]*\]"
        r"|\\(?:ProofID|SourceID|TheoremID|NodeID)\s*\{[^}]+\}"
    )
    if id_heading.search(visible):
        problems.append("reader-facing internal T/P/S coordinate in a heading or audit-ID macro")
    return problems


def requested_combinations(manifest: dict, errors: list[str]) -> set[tuple[int, str]]:
    """Default to all ten documents; never infer the request from existing files."""
    if "requested_documents" not in manifest:
        return set(COMBINATIONS)
    selection = manifest["requested_documents"]
    if not isinstance(selection, list) or not selection:
        errors.append("requested_documents must be a nonempty list of part/edition objects")
        return set()
    requested: set[tuple[int, str]] = set()
    for number, item in enumerate(selection, 1):
        if not isinstance(item, dict) or set(item) != {"part", "edition"}:
            errors.append(f"requested_documents item {number} must contain exactly part and edition")
            continue
        part, edition = item["part"], item["edition"]
        if (type(part) is not int or part not in range(1, 6) or
                not isinstance(edition, str) or edition not in EDITIONS):
            errors.append(f"invalid requested_documents part/edition: {part!r}/{edition!r}")
            continue
        key = (part, edition)
        if key in requested:
            errors.append(f"duplicate requested_documents combination: {key}")
        requested.add(key)
    return requested


def validate(root: Path, template_mode: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    root = root.resolve()
    manifest_path = root / "project-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"project-manifest.json: {exc}"], notes
    if not isinstance(manifest, dict):
        return ["project-manifest.json must be an object"], notes
    if manifest.get("schema_version") != SCHEMA_VERSION:
        return [f"schema_version must be {SCHEMA_VERSION}"], notes
    if manifest.get("language") != "en":
        errors.append("language must be en")
    selection_error_count = len(errors)
    requested = requested_combinations(manifest, errors)
    if len(errors) != selection_error_count:
        return errors, notes
    documents = manifest.get("documents")
    if not isinstance(documents, list) or not documents:
        return errors + ["documents must be a nonempty list of the requested part/edition combinations"], notes
    seen: set[tuple[int, str]] = set()
    filenames: set[str] = set()
    doc_by_key: dict[tuple[int, str], str] = {}
    expanded_by_file: dict[str, tuple[str, Counter[Path]]] = {}
    for doc in documents:
        if not isinstance(doc, dict):
            errors.append("each document must be an object")
            continue
        part, edition = doc.get("part"), doc.get("edition")
        if (type(part) is not int or part not in range(1, 6) or
                not isinstance(edition, str) or edition not in EDITIONS):
            errors.append(f"invalid document part/edition: {part!r}/{edition!r}")
            continue
        key = (part, edition)
        if key in seen:
            errors.append(f"duplicate document combination: {key}")
        seen.add(key)
        context = f"part {part} {edition}"
        tex_name = str(doc.get("tex_file", ""))
        pdf_name = str(doc.get("pdf_file", ""))
        for name in (tex_name, pdf_name):
            if name.casefold() in filenames:
                errors.append(f"{context}: duplicate document filename {name}")
            filenames.add(name.casefold())
        if not tex_name.endswith(".tex") or not pdf_name.endswith(".pdf"):
            errors.append(f"{context}: tex_file/pdf_file need .tex/.pdf extensions")
        tex = checked_path(root, tex_name, context, errors)
        pdf = checked_path(root, pdf_name, context, errors)
        if pdf:
            with pdf.open("rb") as handle:
                if handle.read(5) != b"%PDF-":
                    errors.append(f"{context}: PDF does not have a PDF signature")
        doc_by_key[key] = tex_name
        if tex:
            try:
                expanded, counts = expand_tex(tex, root, errors)
            except (OSError, UnicodeError) as exc:
                errors.append(f"{tex_name}: {exc}")
                continue
            expanded_by_file[tex_name] = (expanded, counts)
            labels = LABEL_RE.findall(expanded)
            duplicate_labels = [label for label, count in Counter(labels).items() if count > 1]
            if duplicate_labels:
                errors.append(f"{tex_name}: duplicate labels {duplicate_labels}")
            for leak in public_leaks(expanded):
                errors.append(f"{tex_name}: {leak}")
            if not template_mode and PLACEHOLDER_RE.search(expanded):
                errors.append(f"{tex_name}: unresolved manuscript placeholder")
            if re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", expanded):
                errors.append(f"{tex_name}: non-English CJK manuscript text")
    # Load by absolute sibling path so importing this validator in tests is safe.
    structure_spec = importlib.util.spec_from_file_location("math_structure_check", Path(__file__).with_name("check_mathematical_structure.py"))
    structure = importlib.util.module_from_spec(structure_spec)
    structure_spec.loader.exec_module(structure)
    skill_version = str(manifest.get("skill_version", ""))
    vmatch = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", skill_version)
    if 'skill_version' in manifest and not vmatch:
        return errors + ['skill_version must be an explicit semantic version X.Y.Z'], notes
    new_contract = bool(vmatch and tuple(map(int, vmatch.groups())) >= (1, 5, 0))
    scope_contract = bool(vmatch and tuple(map(int, vmatch.groups())) >= (1, 6, 0))
    selection_contract = bool(vmatch and tuple(map(int, vmatch.groups())) >= (1, 7, 0))
    body_contract = bool(vmatch and tuple(map(int, vmatch.groups())) >= (1, 8, 0))
    if scope_contract:
        scope_spec = importlib.util.spec_from_file_location("problem_scope_check", Path(__file__).with_name("check_problem_formulation.py"))
        scope_check = importlib.util.module_from_spec(scope_spec)
        scope_spec.loader.exec_module(scope_check)
    for doc in documents:
        if not isinstance(doc, dict):
            continue
        name = str(doc.get("tex_file", ""))
        if name not in expanded_by_file:
            continue
        expanded = expanded_by_file[name][0]
        try:
            if new_contract:
                found, _ = structure.validate_document(root, name, expanded, str(doc.get("structure_review", "")),
                                                       require_schema="1.1.0" if body_contract else None)
            else:
                found = structure.shape_issues(structure.inventory(expanded))
            if scope_contract:
                found.extend(scope_check.validate_document(root, doc, expanded))
            (notes if template_mode else errors).extend(f"{name}: {x}" for x in found)
        except (OSError, ValueError, TypeError) as exc:
            (notes if template_mode else errors).append(f"{name}: structure check: {exc}")

    if seen != requested or len(documents) != len(requested):
        contract = ("requested_documents" if "requested_documents" in manifest
                    else "the default ten part/edition combinations")
        errors.append(f"documents must match {contract} exactly; "
                      f"missing={sorted(requested - seen)}, extra={sorted(seen - requested)}")

    length_contract = bool(vmatch and tuple(map(int, vmatch.groups())) >= (1, 8, 1))
    if length_contract:
        length_spec = importlib.util.spec_from_file_location("reading_length_check", Path(__file__).with_name("check_reading_budget.py"))
        length_check = importlib.util.module_from_spec(length_spec)
        length_spec.loader.exec_module(length_check)
        try:
            length_report = length_check.check(root)
            for row in length_report['documents']:
                if row['blocking']:
                    errors.append(f"{row['pdf']}: PAGE_LIMIT_EXCEEDED: {row['pages']} pages exceeds explicit user max_pages={row['max_pages']}")
                elif row['review_needed']:
                    notes.append(f"{row['pdf']}: REVIEW_NEEDED: {row['pages']} pages exceeds advisory threshold {row['page_review_threshold']}; not a release failure. Record the content-first reread without deleting necessary mathematics.")
                notes.extend(f"{row['pdf']}: {warning}" for warning in row['warnings'])
        except (OSError, ValueError, TypeError, KeyError, ImportError, RuntimeError) as exc:
            (notes if template_mode else errors).append(f"reading-length measurement unavailable: {exc}")

    source_rows = read_csv(root / "bibliographic-identity.csv", {"source_id"}, errors)
    proof_rows = read_csv(root / "proof-mechanism-registry.csv", {"proof_id"}, errors)
    sources = registry_ids(source_rows, "source_id", "bibliographic-identity.csv", errors)
    proofs = registry_ids(proof_rows, "proof_id", "proof-mechanism-registry.csv", errors)
    if not sources:
        errors.append("bibliographic-identity.csv must contain source identities")
    for row in proof_rows:
        unknown = ids(row.get("source_ids", "")) - sources
        if unknown:
            errors.append(f"proof {row.get('proof_id')}: unknown source IDs {sorted(unknown)}")

    map_fields = MAP_FIELDS | INTEGRATED_MAP_FIELDS
    mappings = read_csv(root / "publication-map.csv", map_fields, errors)
    if not mappings:
        errors.append("publication-map.csv must contain mathematical node mappings")
    node_ids: set[str] = set()
    components: set[Path] = set()
    for row in mappings:
        node = (row.get("node_id") or "").strip()
        if not node or node in node_ids:
            errors.append(f"empty or duplicate publication node: {node!r}")
        node_ids.add(node)
        if not (row.get("kind") or "").strip():
            errors.append(f"{node}: missing mathematical kind")
        try:
            owner = int(row.get("owner_part", ""))
        except (ValueError, TypeError):
            owner = 0
        if owner not in range(1, 5):
            errors.append(f"{node}: owner_part must be 1, 2, 3 or 4")
        if not any((part, edition) in requested
                   for part in (owner, 5) for edition in EDITIONS):
            errors.append(f"{node}: owner_part has no requested document")
        component_name = row.get("canonical_component", "") or ""
        inline_statement = selection_contract and not component_name
        component = None if inline_statement else checked_path(root, component_name, node, errors)
        if not inline_statement and not component_name.endswith(".tex"):
            errors.append(f"{node}: canonical_component must be a .tex file")
        if component:
            if component in components:
                errors.append(f"{node}: canonical component assigned to multiple nodes")
            components.add(component)
            body = strip_comments(component.read_text(encoding="utf-8-sig"))
            if re.search(r"\\documentclass\b|\\begin\{(?:document|theorem|lemma|proposition|corollary|definition|example|counterexample|conjecture|question|problem|theoremrecall|mathreviewrecalledtheorem)\}", body):
                errors.append(f"{node}: canonical component must contain mathematical body only")
            if LABEL_RE.search(body):
                errors.append(f"{node}: canonical component must be label-free; put labels in the primary manuscript wrapper")
            if public_leaks(body):
                errors.append(f"{node}: canonical component contains audit metadata or internal coordinates")
            if not template_mode and PLACEHOLDER_RE.search(body):
                errors.append(f"{node}: unresolved canonical component placeholder")
        for field, known in (("source_ids", sources), ("proof_ids", proofs)):
            unknown = ids(row.get(field, "")) - known
            if unknown:
                errors.append(f"{node}: unknown {field} {sorted(unknown)}")
        has_requested_placement = False
        placements = [(owner, edition, edition) for edition in sorted(EDITIONS)]
        placements += [(5, edition, f"integrated_{edition}") for edition in sorted(EDITIONS)]
        for placement_part, edition, prefix in placements:
            filename = row.get(f"{prefix}_file", "") or ""
            label = row.get(f"{prefix}_label", "") or ""
            treatment = row.get(f"{prefix}_treatment", "") or ""
            if (placement_part, edition) not in requested:
                if treatment != "NOT_REQUESTED" or filename or label:
                    errors.append(f"{node}: unrequested {prefix} must use NOT_REQUESTED with empty file/label")
                continue
            if treatment == "NOT_REQUESTED":
                errors.append(f"{node}: requested {prefix} cannot use NOT_REQUESTED")
                continue
            if treatment == "OMITTED_WITH_REASON":
                if (placement_part != 5 and edition != "concise") or filename or label or not (row.get("limitation_note") or "").strip():
                    errors.append(f"{node}: OMITTED_WITH_REASON requires a concise or Part V placement, empty file/label and a limitation_note")
                placed_document = doc_by_key.get((placement_part, edition), "")
                if component and placed_document in expanded_by_file and expanded_by_file[placed_document][1][component]:
                    errors.append(f"{node}: omitted {prefix} node still inputs its canonical component")
                continue
            if filename != doc_by_key.get((placement_part, edition)):
                target = "Part V" if placement_part == 5 else "owner part"
                errors.append(f"{node}: {prefix}_file does not match {target} in manifest")
            if treatment not in TREATMENTS:
                errors.append(f"{node}: invalid {prefix}_treatment {treatment!r}; use {sorted(TREATMENTS)}")
            if placement_part != 5 and edition == "standard" and treatment != "FULL_STATEMENT":
                errors.append(f"{node}: {prefix} edition must use FULL_STATEMENT")
            if treatment == "REFERENCE_ONLY" and not (row.get("limitation_note") or "").strip():
                errors.append(f"{node}: REFERENCE_ONLY needs a limitation_note")
            if filename not in expanded_by_file:
                errors.append(f"{node}: mapped manuscript unavailable: {filename}")
                continue
            if (filename == doc_by_key.get((placement_part, edition)) and
                    treatment in {"FULL_STATEMENT", "REFERENCE_ONLY"}):
                has_requested_placement = True
            text, counts = expanded_by_file[filename]
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9:._-]*", label) or re.search(r"(?:^|[:._-])[TPS]\d{2,}(?:$|[:._-])", label, re.I):
                errors.append(f"{node}: {prefix} needs a semantic label rather than an internal ID")
            if not label or LABEL_RE.findall(text).count(label) != 1:
                errors.append(f"{node}: {prefix} semantic label {label!r} must occur exactly once")
            count = counts[component] if component else 0
            if treatment == "FULL_STATEMENT":
                if inline_statement:
                    pass  # One-off located statements need no artificial component file.
                elif count < 1:
                    errors.append(f"{node}: {prefix} canonical component input count {count}; expected at least 1")
                elif count > 1:
                    notes.append(f"{node}: {prefix} reuses its canonical body {count} times; useful local recalls are allowed. Review their purpose and printed numbering; repetition alone is not a defect.")
            elif count != 0:
                errors.append(f"{node}: {prefix} canonical component input count {count}; expected 0")
        if inline_statement:
            full_placements = sum(row.get(p+"_treatment") == "FULL_STATEMENT"
                                  for p in ("concise","standard","integrated_concise","integrated_standard"))
            if full_placements > 1:
                errors.append(f"{node}: shared statements require a canonical body")
        if not has_requested_placement:
            errors.append(f"{node}: no public placement in a requested document")

    if selection_contract:
        selection_spec = importlib.util.spec_from_file_location("survey_selection_check", Path(__file__).with_name("check_survey_selection.py"))
        selection_check = importlib.util.module_from_spec(selection_spec)
        selection_spec.loader.exec_module(selection_check)
        try:
            selected_errors, selected_notes = selection_check.validate_selection(root, manifest, {name: value[0] for name, value in expanded_by_file.items()})
            (notes if template_mode else errors).extend(selected_errors)
            notes.extend(selected_notes)
        except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
            (notes if template_mode else errors).append(f"selection check: {exc}")

    audit = root / "release-audit.csv"
    proof_explanation_requested = any(part == 3 for part, _ in requested)
    frontier_requested = any(part in {4, 5} for part, _ in requested)
    if audit.is_file():
        rows = read_csv(audit, {"check", "status", "evidence", "note"}, errors)
        if not rows:
            errors.append("release-audit.csv has no checks")
        seen_checks: set[str] = set()
        for row in rows:
            check = row.get("check", "") or ""
            if not check or check in seen_checks:
                errors.append(f"release-audit.csv: empty or duplicate check {check!r}")
            seen_checks.add(check)
            status = (row.get("status") or "").strip().upper()
            na_allowed = ((check == "frontier_status" and not frontier_requested) or
                          (check in PART_III_AUDITS and not proof_explanation_requested))
            conditional_na = (na_allowed and status == "NOT_APPLICABLE" and
                              bool((row.get("note") or "").strip()))
            if status not in PASS_STATUSES and not conditional_na:
                message = f"release-audit.csv: {check} is {status or 'EMPTY'}, not an accepted completed status"
                (notes if template_mode else errors).append(message)
            if status in PASS_STATUSES and not (row.get("evidence") or "").strip():
                message = f"release-audit.csv: {check} has a completed status but no evidence record"
                (notes if template_mode else errors).append(message)
        missing_checks = (REQUIRED_AUDITS | REQUESTED_DOCUMENT_AUDITS) - seen_checks
        if proof_explanation_requested:
            missing_checks |= PART_III_AUDITS - seen_checks
        if missing_checks:
            message = f"release-audit.csv: missing required checks {sorted(missing_checks)}"
            (notes if template_mode else errors).append(message)
    else:
        message = "Missing release-audit.csv: mathematical/semantic/visual review is incomplete."
        (notes if template_mode else errors).append(message)
    notes.append("These checks do not establish mathematical truth, exhaustive source coverage, proof validity, or semantic equivalence of different prose.")
    notes.append("Completed release-audit statuses are declared review records; this checker does not perform those human/build/archive reviews.")
    notes.append("Reader-outcome, proof-framework, decisive-mechanism, and edition-depth checks inspect record presence/status/evidence only, not explanatory quality or whether evidence covers the requested scope.")
    notes.append("Only requests including Part III require proof_framework and decisive_mechanisms. Part V methods are reviewed under reader_outcomes and edition_depth; Part V still requires frontier_status within its own selected scope. Substantive adequacy is not machine-checked.")
    notes.append("Writing quality is not machine-certified: assess trivial transitions, theorem focus, formula use, hypothesis lists and useful repetition in the existing substantive reviews.")
    notes.append("TeX parsing covers literal braced input/include and labels only; compile logs and PDF inspection remain required.")
    notes.append("Internal-ID leakage checks target headings and audit fields; legitimate mathematical symbols are not rejected merely for matching T/P/S digits.")
    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--template-mode", action="store_true", help="Allow template placeholders; never a publication-ready verdict")
    args = parser.parse_args()
    try:
        errors, notes = validate(args.project, args.template_mode)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        errors, notes = [str(exc)], []
    for note in notes:
        print(f"NOTE: {note}")
    if errors:
        print("PROJECT STRUCTURAL VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    mode = "TEMPLATE STRUCTURE ONLY" if args.template_mode else "PROJECT STRUCTURAL CHECKS"
    print(f"{mode} PASSED; no mathematical or publication-readiness certification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
