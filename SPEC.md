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

---

# 15lovecoffee archive task (527c)

# Archive 15lovecoffee

Use the checked-out Instaloader to download all accessible media from the Instagram profile `15lovecoffee`. Ignore the URL tracking query. Preserve photos, videos, captions, metadata and profile picture, plus reels, tagged posts, current stories and highlights where supported and accessible. Deleted or expired content is outside scope.

Store media outside version control in a persistent workspace archive. Never commit cookies or credentials. Reuse an authorized session if available; otherwise attempt public access and report authentication or platform restrictions accurately. Do not claim a complete archive unless all requested accessible categories finish successfully. Record reproducible commands, output location, counts and any exclusions. Follow the required SpecKit stages, independent review, knowledge capture and Vibe Kanban PR/CI/merge workflow for repository changes.
