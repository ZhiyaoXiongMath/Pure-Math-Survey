# Maintaining and distributing 2.0.3

Change the unique authoritative layer, regenerate derivatives, rerun behavioral tests and inspect actual new PDFs. Do not silently rewrite frozen samples or snapshots. Update the explicit package_release.py whitelist for every runtime script, nested module and resource. Unsupported/unreviewed files fail packaging; fonts are forbidden.

Run `python scripts/validate_assets.py --json`; it parses supported Python grammar, checks local documentation links and executes native knowledge/freeze/three-profile preparation smoke behavior. Run repository unittest tests. Public examples are stored in the repository's examples directory; Release attachments contain only the installation archive and checksums. Run `python scripts/build_checks.py --output NEW_DIRECTORY` for current and frozen style tasks, separately from new-profile validation.

Package using `python scripts/package_release.py --output /path/pure-math-survey-2.0.3.zip`. Reopen/check all members and run tools/verify_release.py --no-build against that archive (or supply --example-root for the reviewed three-profile matrix-tree project to include external builds) in a freshly extracted directory and isolated no-pip environment. Test the runtime, not just source-tree imports. State tested runtime/platform separately from the Python 3.10 grammar check.

Keep development notes and test reports outside the installation archive. No GitHub release, PR or local user installation is performed by these scripts.
