# Instaloader upstream synchronization

Synchronize davidvasandani/instaloader master with instaloader/instaloader master at a recorded upstream commit. Preserve upstream history and any fork-specific changes; do not force-push or overwrite divergent work. Use a topic branch and merge a reviewed pull request only after CI passes.

Acceptance criteria:
- Record fork base, upstream revision, divergence, and any conflict resolutions.
- The selected upstream revision is an ancestor of the resulting fork master.
- Run the repository's relevant checks and independently review the complete change.
- Complete the ordered WikiLLM and SpecKit artifacts and record reusable project knowledge.
- Open the PR through Vibe Kanban Create PR and merge after successful checks.

Scope is the Instaloader repository. Homelab infrastructure and deployment are outside this synchronization. No new release or package publication is requested.

Recorded baseline: fork c69eff0dbbcdb3691964af1893c4576eeb9efe5f; upstream 09dea80d2be81bed94e8d65717cf8684fcc2998b. The fork's --list-only behavior is a required compatibility invariant. See PRIOR_KNOWLEDGE.md for read-only knowledge recall.
