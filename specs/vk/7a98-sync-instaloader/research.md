# Research

Both repositories use master. Baseline divergence is 3 fork-only commits and 27 upstream-only commits. The fork extension was introduced in 9775f33; the other two fork commits are upstream merge commits. Git merge preserves this lineage and supports future syncs. Reset, squash, and rebase were rejected because the acceptance criteria require both histories.

The existing documentation workflow deploys on every master push to instaloader/instaloader.github.io, including fork pushes. Gate only deployment by repository identity; keep documentation builds active in the fork.
