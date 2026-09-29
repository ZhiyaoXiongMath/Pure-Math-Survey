# Validation and honest evidence

| Layer | Executable check | What still requires actual reading |
|---|---|---|
| Structure | schema, IDs, references, paths, required cycles | meaning and sufficiency |
| Snapshot | every actual byte and content ID | mathematical correctness |
| Readiness | accepted scoped bindings, source support, coverage/gaps, proof steps | whether original text supports the assertion |
| Output structure | exact generated and snapshot material bytes/members, literal inputs, TeX inventory | surrounding prose and promised reader task |
| Build | actual commands, logs, PDF hash/page count, stable auxiliaries | readability or proof correctness |
| Render | all actual pages rasterized and hashed | every page must be opened and inspected |
| Release | reread real files and all evidence; reject draft/stale/missing | independent peer review is not supplied by a script |

States are not interchangeable. `kb validate` can be VALID with unassessed nodes. Freeze can succeed before readiness. `--draft` permits preparation but never formal release. Review templates use not_performed/revise, never auto-accept. Successful tests use synthetic review fixtures only where explicitly labeled; those fixtures are not mathematical acceptance.

Reviews contain review_id, kind, reviewer_mode, reviewed_at, inputs (path/SHA256), scope, findings, unchecked_items, disposition. Accepted requires a real nonfuture date and substantive findings. Use author_reread for the author/agent's own rereading. Nonblocking limitations are objects with `blocking:false` and an explicit reason; ordinary unchecked strings block. Independent review is optional, but its absence is reported.

Source reviews bind source records and reading notes/materials. Mathematical reviews bind nodes, necessary definitions/proof inputs, controlling sources and scope/conventions; local derivations state evidence_basis. Coverage binds scope, question, candidate nodes, overview, discovery and coverage. Open claims require actual dated reverse searches. Output-semantic reviews bind plan, outline, all authored/generated/material files; scope identifies consumed nodes, profile, principal_locations and proof_steps. Visual reviews bind actual PDF, build-report, render-manifest and every page image; scope includes ordered pages and substantive page_findings for all pages.

CLI envelopes are `{operation,status,errors,warnings,artifacts}` under `--json`. Exit codes: 0 completed operation; 2 invalid contract/input; 3 unmet readiness/release; 4 tool/I/O failure. Diagnostics carry consistent code/path/node_id/message. Use `kb readiness` and `output validate --stage release` for individual blocking findings; preparation/package cannot turn failures into PASS.

Literal TeX scanning cannot evaluate arbitrary macro conditionals or prove a theorem. Source texts/TeX must be trusted: disabled shell escape is not an operating-system sandbox. Build and review reports are transparent local assertions, not signed independent attestations.
