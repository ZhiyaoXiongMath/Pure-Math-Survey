# Length and selection

## Defaults are selections, not ten automatic volumes

A single-topic request selects V concise. An explicit five-part series or five-part suite selects I–V concise. End-to-end testing of a specified part preserves that selection. The ten templates are a catalog; standard and paired editions require a request. The manifest must explicitly record the selected documents, even though the legacy validator retains its ten-document compatibility fallback.

| Part | Concise reading-review threshold | Standard reading-review threshold |
|---|---:|---:|
| I | 5 | 8 |
| II | 6 | 10 |
| III | 6 | 10 |
| IV | 5 | 8 |
| V | 10 | 16 |

Count all pages, including references. These thresholds are editorial reread triggers, not content quotas, failure limits or targets to fill. Never lower the 12-point font, narrow the baseline margins, remove a necessary assumption or use unexplained abbreviations to fit. Review genuine side branches, duplicated exposition and compressible proof detail first. When the selected mathematics needs more space, retain it and record a specific reading decision in the existing `architecture.md`; do not ask for approval merely to exceed default guidance.

The optional manifest field `page_review_threshold` changes only the diagnostic trigger. Its historical spelling, `page_review_limit`, is also accepted with the same non-blocking meaning; conflicting values are an input error. Neither spelling sets a hard page limit. Do not introduce a larger threshold merely to hide a reported overrun.

Only an explicit user requirement sets `documents[].max_pages`, a positive integer including references. Do not populate it from the defaults. `create_project.py --max-pages N` records that explicit limit for every selected document; distinct per-document limits can be entered in the manifest. If the necessary scope cannot satisfy such a limit, report the conflict rather than silently changing scope, deleting hypotheses or granting yourself an exception.

`check_reading_budget.py PROJECT` keeps its established command name. It reports:

| Status | Meaning | Exit code |
|---|---|---:|
| `WITHIN_GUIDANCE` | Measured length does not trigger the default reread; no quality certification | 0 |
| `REVIEW_NEEDED` | Measured length exceeds guidance; record an editorial reread, not a release failure | 0 |
| `PAGE_LIMIT_EXCEEDED` | An explicitly requested `max_pages` is exceeded | 1 |
| `ERROR` | Manifest, selection, dependency or PDF cannot be measured reliably | 2 |

The report binds each measurement to its PDF SHA-256. Current-project validation uses the same measurement: advisory overruns are notes, explicit-limit breaches and unavailable measurement are errors. A zero exit code does not claim that the editorial reread, PDF inspection or mathematical review has occurred.

## Select before expanding

Write one sentence describing the reader's mathematical task for each requested part. Select the principal answers and the minimum definitions needed to understand them. Keep a completed mechanism or model where the part promises one. Identify genuine side branches before drafting; do not demote a missing principal answer after writing the body.

I: retain the objects, question and a completed model. II: retain exact result statements and substantive relations. III: retain the decisive derivations and the actual closure of selected routes. IV: retain the organizing problem, strongest relevant settled boundary and exact remaining target. V: retain an independent thematic argument rather than concatenate the other parts.

For short parts, omit a contents page, separate title page, generic motivation, paper-by-paper tours, duplicated prose paraphrases of formulas, and inventories at the end. State a useful consequence once, outside the main theorem. A reader should not have to read an internal audit card to learn mathematics.

## Two reading passes

**First-page pass.** The reader can identify the objects, central question, selected actual answers and controlling status. I–IV introductions normally occupy at most one page; V normally at most two. If a precise main statement requires more space, cut side branches, not its hypotheses.

**Body pass.** Each section supplies a definition, result, completed inference, explanatory model, boundary or precise sourced question. Remove sections that only announce later sections. Every promised proof has an identified endpoint; every imported theorem has the hypotheses needed at its point of use.

Run `scripts/check_reading_budget.py PROJECT` after compiling. Review rendered pages as well: an empty final page or four dense pages of uninterrupted theorem statements can fail the reading task despite remaining below a diagnostic threshold.

## Scope is not a length-control variable

Remove ancillary branches, duplicated statements and dispensable comparisons before reducing the agreed question. Do not replace a general problem with its simplest special case without the user changing the scope. A standard edition adds depth where a decisive inference occurs, not a mandatory final depth section. A manuscript shorter than the guidance does not need padding.

## Selection and discovery

A default-guidance overrun triggers selection review, not smaller fonts, narrower margins or suppression of a core frontier. Record a retained overrun and its mathematical reason. Remove secondary branches before essential statements. Counts of results, Problems, searches or tests do not measure quality.
