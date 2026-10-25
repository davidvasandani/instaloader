# Implementation plan

1. Complete the workspace-provided SpecKit commands in their required order; their feature artifacts live in homelab/specs/vk/527c-download-15lovec.
2. Inspect the checked-out Instaloader CLI, dependencies and local session availability without exposing secrets.
3. Run a bounded public download for 15lovecoffee into ../archives/15lovecoffee. Include reels, tagged and IGTV where available; preserve normal post captions and metadata. If an authorized Instaloader session is available, include stories and highlights.
4. Stop on platform access restrictions and preserve partial files. If a long-running download is possible, use a bounded Vibe Kanban poller rather than a detached process.
5. Verify actual media counts, category coverage and command exit state. Document the exact command and outcome; do not mark an incomplete archive complete.
6. Independently review repository changes using Codex CLI and resolve significant findings.
7. Record reusable operational knowledge in homelab, commit each changed repo, and use Vibe Kanban Create PR and merge only after required CI passes. Download completion remains a separate acceptance gate.
