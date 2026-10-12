# Maintaining and distributing 2.1.0

Change the unique authoritative layer, regenerate derivatives, rerun behavioral tests and inspect actual new PDFs. Do not silently rewrite frozen samples or snapshots. Update the explicit package_release.py whitelist for every runtime script, nested module and resource. Unsupported/unreviewed files fail packaging; fonts are forbidden.

Run `python scripts/validate_assets.py --json`; it parses supported Python grammar, checks local documentation links and executes native knowledge/freeze preparation smoke behavior for all four profiles and five views (20 combinations). Run repository unittest tests. Public examples are stored in the repository's examples directory; Release attachments contain only the installation archive and checksums. Run `python scripts/build_checks.py --output NEW_DIRECTORY` for current and frozen style tasks, separately from new-profile validation.

Package using `python scripts/package_release.py --output ../pure-math-survey-2.1.0.zip`. Reopen/check all members and run tools/verify_release.py against that archive in the repository (historical suites are examples/vnext/projects and examples/rc2/projects; current articles are selected by examples/r3/verification-manifest.json; use --no-build only for an explicitly reported build omission) in a freshly extracted directory and isolated no-pip environment. Test the runtime, not just source-tree imports. State tested runtime/platform separately from the Python 3.10 grammar check.

The repository's `artifact-checksums.txt` inventories the current whitelisted skill
resources, excluding itself. Refresh it after resource changes and verify every
entry against the current files. The packager deliberately ignores that source
file and generates a fresh checksum list from the actual selected bytes inside
each archive. Verify source and archive lists separately; neither updates an old
archive, historical snapshot or accepted review. The historical Minimal template
`assets/templates/profile-minimal-rc2.tex` remains required alongside the r3 template.
Runtime text is checked out with LF line endings so these source-resource hashes
remain portable; binary reference assets and immutable example files retain their
explicit byte-preservation attributes.

Keep development notes and test reports outside the installation archive. No GitHub release, PR or local user installation is performed by these scripts.
