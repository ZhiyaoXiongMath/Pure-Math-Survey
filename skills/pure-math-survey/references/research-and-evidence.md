# Source discovery, reading and evidence

Search from the question, not just the supplied papers: aliases, original formulations, strongest answers, counterexamples and subsequent improvements. Record actual queries/dates, candidates, decisions, omission challenge and stopping reason in discovery.md. Preserve inaccessible texts and ambiguity as explicit gaps. A short requested document is not a research cutoff.

Register primary identities first. Read the actual supporting sections, checking hypotheses, quantifiers, normalizations, locator and controlling version. Write a source-check note. Distinguish retrieved metadata from original-text reading, and unpublished/preprint/published status from mathematical status. Do not claim all of a paper was read when only supporting sections were inspected.

`access.local_path` points to original bytes only when present and legally retainable; it is hashed and snapshotted. When bytes were never obtained, use null `material_sha256` and null `local_path`, record `material_hash_unavailable_reason`, a versioned URL and substantive `reading_note`. The source review must declare `scope.source_reading[S-ID]` with `mode: original_text_online`, the exact `version`, nonempty `locators` and `raw_bytes_unavailable_reason`. This yields a visible warning, not a byte certificate. Never use a reading-note hash as the material hash.

Translate source notation into exact local mathematics and justify the translation. A real-class extension of a line-bundle theorem is a local deduction, not silently an original theorem. Mechanisms have actual inputs, intermediate calculations and outputs. Source review asserts support for the imported theorem statement; it need not reproduce the full external proof. Its scope must say so.

Use `review template PROJECT --kind source --id S-ID --to evidence/reviews/new.json` (similarly mathematical/coverage) to obtain pending bindings. Only after actual reading fill date, author_reread, substantive findings, disposition and remaining limitations. An independent tool invocation by the same author is still self-review. See [validation](validation.md).

If the original was actually downloaded and hashed but cannot be redistributed,
retain the actual `material_sha256` with `local_path:null`. Explain nonretention
truthfully in the existing access-limitation fields and reading note; do not claim
failed access. Validation reports `SOURCE_RAW_BYTES_NOT_RETAINED`: the recorded
hash is not a rechecked in-project byte certificate. The online reading still
requires the exact controlling version, a nonempty list of locators, and actual
input-bound findings. Never invent a hash or substitute a reading-note hash.

## Read explanatory choices as well as facts

When useful, record how the source rewrites its target, chooses/normalizes an auxiliary
object, computes a model, identifies objects, isolates a difficult lemma and reuses the
output. Check those choices against the current reader's operations rather than copying
the source's omissions. A teaching reference and primary support have separate evidence
roles; readable prose does not certify its formulas. Report the exact supporting sections
actually inspected, never a full-course audit inferred from a few later lectures.

## Separate facts and public inputs (PR03)

Software/schema/policy versions stay unchanged. New optional metadata never migrates or certifies old records: absent access/permission/scope evidence remains **UNVERIFIED**. `kb validate` reports structural validity and the fact matrix, not actual reading. URL, material hash and a generated template cannot grant reading or a license.

Record the following in `access` using actual evidence:

```json
{
  "availability": {"status": "unknown", "checked_at": null, "basis": "Access has not been checked."},
  "material_visibility": "private",
  "redistribution": {"status": "unknown", "checked_at": null, "basis": "Original-byte redistribution has not been authorized."},
  "permission_note": null
}
```

Availability statuses are `accessible`, `unavailable`, `unknown`; original-byte redistribution statuses are `granted`, `denied`, `unknown`. Positive/negative verified facts require an actual date and substantive basis. Unknown/missing evidence yields UNVERIFIED, while dated explicit unavailability/denial yields REJECTED. Publication, citation, access and permission to redistribute the original are different facts. References to literature facts do not automatically require delivery of its original bytes, nor grant permission to redistribute those bytes. License authenticity and reading are human/agent assertions; engineering checks only inspect their recorded scope and byte bindings.

The accepted source review must record `scope.source_reading[S-ID]`: exact `version`, `mode` (`original_text_local`, `original_text_online`, or `original_text_private`), nonempty `locators` covering the actual consumed node support locators, substantive `reading_scope` describing what was read (statements/sections/full text/proof as actually applicable), and explicit `unchecked_items`. Unread work may be disclosed as a nonblocking object with `blocking:false` and an actual reason; unread support remains blocking. Source reading does not require claiming the entire external proof was checked. Its actual scope is preserved rather than inferred from the source title or file hash.

`source_inputs` binds source metadata (including access/permission facts), reading note, optional public permission note and applicable retained original bytes. Source batch validation and candidate acceptance reuse the same scope and path checks; changed metadata/notes/permissions/bytes are stale input failures. Source-review scope itself is frozen with the evidence and bound into downstream authoring materials. Plan contribution changes invalidate the existing exact promise projection. Never edit accepted history to refresh hashes.

Keep private originals outside the public project. Store no absolute/private location in public records: use `local_path:null`, a safe public identity, an actual previously computed hash if available, and honest retention limits. `original_text_private` records actual private reading without placing the private path or bytes into public inputs; private readability is an assertion, and unretained bytes remain UNVERIFIED. Online/private records also require `material_hash_unavailable_reason` and `raw_bytes_unavailable_reason`; a known hash is not a rehashable byte certificate. Do not use a note's hash as original material identity.

A public project-local original requires `material_visibility:public` plus dated `redistribution:granted` with actual basis. Freeze and candidate gates refuse private/denied/unknown original inputs before creating public snapshots. Private path components (`private`/`.private`) and byte-identical aliases of declared originals in reading notes or review inputs are checked too. `.gitignore` is an additional convenience, not the runtime gate. Software cannot discover undeclared originals or establish what a file contains: authors must honestly register sources and keep private material out of project inputs. Authoring materials and manuscript packages always omit registered originals and byte-identical aliases, including authorized ones; omission is never reported as permission.

| Synthetic engineering scenario | Access | Reading | Bytes | Original redistribution | Knowledge / Paper result |
|---|---|---|---|---|---|
| Scoped local fixture, public/authorized original | VERIFIED | VERIFIED | VERIFIED | VERIFIED | Knowledge READY when its other gates pass; no research originality inferred. |
| Actual declared online/private scope, no retained copy, unknown permission | VERIFIED | VERIFIED | UNVERIFIED | UNVERIFIED (`unknown`) | Knowledge may be READY; original bytes omitted. |
| Same reading, explicit dated refusal | VERIFIED | VERIFIED | UNVERIFIED | REJECTED (`denied`) | Knowledge may be READY; original bytes omitted. |
| Legacy metadata/hash with missing access/scope/permission evidence | UNVERIFIED | UNVERIFIED | Only retained-byte identity can be verified | UNVERIFIED | No automatic migration or reading acceptance. |
| Retained private or unauthorized original/alias | Independently reported | Independently reported | Independently reported | As recorded | Freeze/candidate public-input gate refuses. |

These are fixture outcomes, not executed mathematical readings or legal opinions. Independent source facts, knowledge READY, marked Paper Draft preview and formal research delivery must each be reported with actual performed scope.

## Attribution at first formal use (all four modes)

Actual origin and mathematical use determine attribution, not environment type. A borrowed/equivalent theorem, lemma, proposition or corollary needs adjacent visible prose naming the controlling source and precise theorem/section/page locator. A special case, normalization change or reformulation additionally identifies the changed variables, assumptions, regularity, range or constants and the checked conversion. A composite local consequence names each external input and explains their combination. Bibliography-only listings, comments, hidden branches, a citation with the wrong version/hypotheses, and a source name in an optional theorem title do not satisfy this duty.

Truly local lemmas/calculations/examples do not require fabricated citations. If a local proof uses an external deep input, cite that input at the actual invocation and check its assumptions/output. Borrowed definitions, examples, problems and conjectures need nearby origin; independently formed ones are not forced to have authors. Reusing a correctly attributed local statement later via its label does not require repetitive citation, unless a new input/version is introduced.

Keep canonical bytes unchanged: put the origin prose before/after the generated input's enclosing statement, not a rewritten statement. Author and non-author use existing source/mathematical/coverage/output_semantic/contribution records, statement_context and attribution findings to verify source identity, version, locator, quantifiers, constants and actual support. A nonempty cite is only a structural candidate, never semantic PASS; unresolved source facts remain REVIEW_REQUIRED. Do not add per-environment provenance records or reread unchanged sources mechanically.
