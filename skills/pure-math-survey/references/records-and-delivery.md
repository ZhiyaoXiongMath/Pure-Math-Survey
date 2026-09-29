# Native 2.0.0 data and delivery contract

See [contracts](contracts.md) for fields and [validation](validation.md) for evidence. Authority: project/scope/knowledge/source records → immutable snapshot → output plan → authored TeX plus generated fragments. Indexes and generated files are replaceable; frozen bytes and historical reviews are not overwritten.

A minimal project contains project.json, scope.md, knowledge/overview.md, conventions.tex, discovery.md and coverage.json. Nodes/sources/evidence are added as needed. Zero outputs and unused nodes are legal. Knowledge nodes use JSON frontmatter, not YAML. Unknown schema versions fail explicitly. Relative POSIX paths only; reject traversal and symbolic links.

Snapshots fix project, scope, knowledge and associated evidence and referenced local source material. They exclude outputs, cache and earlier snapshots. Canonical JSON of schema_version/project_id/sorted file records produces the full KB-SHA256 ID. Snapshot manifest does not hash itself. Atomic staging prevents a half-written final snapshot; existing same-ID bytes are verified before reuse.

Outputs live in outputs/ID, with plan.json, outline.md, manuscript/, generated/, materials/, evidence/, build/. `materials/` is a bounded generated authoring pack; it is not a second editable KB. `output package` includes TeX, style, exact fragments, selected readable knowledge/evidence, plan, actual build/check evidence, manifests and rebuild.py. Raw original sources are omitted unless separately and lawfully supplied. The full repository demonstrations retain complete selected snapshots; standalone output packages carry consumed identities/materials, not an entire KB.

Rebuild an extracted output with `python -I rebuild.py --output ../rebuilt`. The destination must be new and outside that package. New compilation is reproducibility evidence; its PDF needs a new visual review before replacing the originally inspected delivery.
