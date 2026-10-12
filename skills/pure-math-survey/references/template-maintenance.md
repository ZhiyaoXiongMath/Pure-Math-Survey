# Maintaining and distributing 2.1.0

Change the unique authoritative layer, regenerate derivatives, rerun behavioral tests and inspect actual new PDFs. Do not silently rewrite frozen samples or snapshots. Update the explicit package_release.py whitelist for every runtime script, nested module and resource. Unsupported/unreviewed files fail packaging; fonts are forbidden.

Run `python scripts/validate_assets.py --json`; it parses supported Python grammar, checks local documentation links and executes native knowledge/freeze preparation smoke behavior for all four profiles and five views (20 combinations). Run repository unittest tests. Public examples are stored in the repository's examples directory; Release attachments contain only the installation archive and checksums. Run `python scripts/build_checks.py --output NEW_DIRECTORY` for current and frozen style tasks, separately from new-profile validation.

Package using `python scripts/package_release.py --output ../pure-math-survey-2.1.0.zip`. Reopen/check all members and run tools/verify_release.py against that archive in the repository (the source suites are examples/vnext/projects and examples/rc2/projects; use --no-build only for an explicitly reported build omission) in a freshly extracted directory and isolated no-pip environment. Test the runtime, not just source-tree imports. State tested runtime/platform separately from the Python 3.10 grammar check.

Keep development notes and test reports outside the installation archive. No GitHub release, PR or local user installation is performed by these scripts.
