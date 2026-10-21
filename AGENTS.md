# Pure-Math-Survey 2.4.1 development

Apply this section to work targeting 2.4.1. Preserve unrelated existing repository instructions. Current explicit user instructions take precedence.

1. Read `docs/development/v2.4.1/DEVELOPMENT_STATE.yaml`, `docs/development/v2.4.1/DEVELOPMENT_RULES.zh-CN.md`, and the current stage in `docs/development/v2.4.1/PR_WORKFLOW.zh-CN.md`. On first handoff, read `docs/development/v2.4.1/DEVELOPMENT_GUIDE.zh-CN.md` too. For PR review, use the PR's actual head_sha for these files, especially before PR-01 has merged.
2. Reconcile actual GitHub main, the current PR, current HEAD, checks, reviews and merge state before working. Continue existing same-stage work. State-file snapshots may lag GitHub.
3. 2.4.1 exposes only minimal writing. Remove runtime audit roles/gates/loops and mandatory child chats. Do not recreate them under verifier/critic/quality terminology or bypass them using fake approvals or draft flags.
4. Reuse one canonical KB for knowledge units and manuscript statements. Follow the preserved rules.v22 content contract with the explicitly documented 2.4.1 runtime overrides. Do not require paired full fast/slow proofs.
5. Implement one stage, keep it runnable and installable, perform relevant checks, and produce its concrete PR. Code review belongs to development, never to each paper-generation run. Honor actual user authorization for merge/release.
6. `DEVELOPMENT_STATE.yaml` is the only persisted current development status. Do not write a commit's own final SHA inside itself or claim a PR merged before it merges. Record a prior merge in the next normal stage commit.
7. Old four-mode/r4/r5 development instructions are historical for this target. Do not load development history into runtime prompts or ship it in the skill installer.
8. Do not claim tests, source reading, tokens saved, page inspection, merge or release without actual evidence. Keep old user projects unchanged when unsupported.
