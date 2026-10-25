# Prior knowledge: Instaloader sync

Task: vk/7a98-sync-instaloader. Searched the workspace's homelab knowledge-base/, docs/knowledge/, and docs/knowledge-base/ for Instaloader, fork synchronization, and CI behavior. Instaloader has no existing project knowledge base.

Relevant guidance:
- docs/knowledge-base/fork-release-tarballs.md: keep fork branches mergeable with upstream; avoid incidental version/publication changes during a sync. This task requests no release.
- docs/knowledge-base/required-check-starvation-and-cancellation.md: queued checks do not establish failure; inspect the actual head and results before merging, and do not cancel unrelated runs.
- knowledge-base/github-newest-branch-by-commit-date.md: default branch selection is distinct from choosing the most recently committed branch. Here both repositories explicitly use master.

Repository evidence: the fork has three unique commits, including feat: add --list-only, and upstream has 27 unique commits. Preserve the fork behavior when merging. No Instaloader-specific prior sync guidance was found.

---

# 15lovecoffee archive task (527c)

# Prior knowledge: 527c-download-15lovec

Searched homelab/knowledge-base, homelab/docs/knowledge-base and homelab/docs/knowledge for Instaloader, Instagram and 15lovecoffee. No account-specific or Instaloader-specific page was found.

- `homelab/knowledge-base/ohana-instagram-saved-posts.md`: a partial scan is not proof of completeness; persist discovered media and report unconfirmed endings accurately.
- `homelab/docs/knowledge-base/family-os-instagram-dm-archive.md`: authenticated browser state belongs to its managed browser boundary; do not export that service's cookies to this downloader. Record actual failures rather than treating an empty result as success.
- `homelab/knowledge-base/ohana-external-feed-mirrors.md`: retain historical media; missing upstream items should not erase an archive.

This is a separate one-off Instaloader operation, not an Ohana integration. Use public access or a session explicitly available to Instaloader. Keep media and secrets outside Git; preserve resumability and evidence of incomplete coverage.
