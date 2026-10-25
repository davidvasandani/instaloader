# Prior knowledge: Instaloader sync

Task: vk/7a98-sync-instaloader. Searched the workspace's homelab knowledge-base/, docs/knowledge/, and docs/knowledge-base/ for Instaloader, fork synchronization, and CI behavior. Instaloader has no existing project knowledge base.

Relevant guidance:
- docs/knowledge-base/fork-release-tarballs.md: keep fork branches mergeable with upstream; avoid incidental version/publication changes during a sync. This task requests no release.
- docs/knowledge-base/required-check-starvation-and-cancellation.md: queued checks do not establish failure; inspect the actual head and results before merging, and do not cancel unrelated runs.
- knowledge-base/github-newest-branch-by-commit-date.md: default branch selection is distinct from choosing the most recently committed branch. Here both repositories explicitly use master.

Repository evidence: the fork has three unique commits, including feat: add --list-only, and upstream has 27 unique commits. Preserve the fork behavior when merging. No Instaloader-specific prior sync guidance was found.
