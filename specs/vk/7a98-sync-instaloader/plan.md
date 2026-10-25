# Technical plan

Spec: ./spec.md. Status: ready.

## Technical context and approach
Python package with CLI in instaloader/__main__.py and download implementation in instaloader/instaloader.py. Existing workflows run PyLint/MyPy on Python 3.10–3.15 after the upstream merge, Sphinx documentation, and Windows packaging. test/ includes live Instagram tests; add focused offline coverage for fork behavior.

Merge upstream/master into the workspace branch from origin/master. Examine the merge and compare against upstream to ensure the --list-only CLI flag and enumeration methods survive. Preserve existing generated build/lib and egg-info files unless tests reveal a concrete compatibility problem. Do not publish a package.

Run compile/import/help checks, offline regression tests, and CI-equivalent lint/type/doc checks where tooling permits. Add the offline tests to CI. Scope the documentation deployment step to the upstream repository so a fork master merge cannot attempt publishing to upstream's Pages repository. Record every compatibility change and its evidence in verification.md.

Register and attach the repository via Vibe Kanban's repository/workspace API (no corresponding MCP registration tool is exposed). Use the MCP Create PR and merge tools for delivery. Preserve both histories with merge strategy, not squash/rebase.

## Data model and contracts
No new persistent entities or interfaces. Preserve --list-only CLI and Python enumeration method contracts.

## Constitution check
All five principles satisfied: history and fork behavior retained; scope limited; offline validation with CI; independent review; recorded evidence and PR gate.

## Risks
Fork changes may expose existing lint failures. Instagram integration tests require credentials and network and must not be represented as offline passes. CI may be disabled on a fork; inspect configuration and enable repository Actions if necessary for authorized validation. Concurrent master updates require re-fetch and validation before merge.
