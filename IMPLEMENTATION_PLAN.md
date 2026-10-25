# Implementation plan

1. Complete SpecKit constitution, specification, clarification, technical plan, tasks, and analysis in order.
2. Register and attach Instaloader to this Vibe Kanban workspace, using master as the PR base.
3. Create the workspace topic branch from fork c69eff0dbbcdb3691964af1893c4576eeb9efe5f and merge upstream 09dea80d2be81bed94e8d65717cf8684fcc2998b, preserving the fork's --list-only feature.
4. Inspect conflicts and the full upstream diff. Run CI-equivalent checks and offline regression checks for --list-only; do not require Instagram credentials.
5. Run independent Codex CLI review, fix confirmed findings, and repeat validation as necessary.
6. Record reusable sync knowledge and verification evidence; commit all task artifacts.
7. Use Vibe Kanban Create PR against master, wait for passing CI, merge with history preserved, and verify upstream ancestry on the resulting master.

---

# 15lovecoffee archive task (527c)

# Implementation plan

1. Complete the workspace-provided SpecKit commands in their required order; their feature artifacts live in homelab/specs/vk/527c-download-15lovec.
2. Inspect the checked-out Instaloader CLI, dependencies and local session availability without exposing secrets.
3. Run a bounded public download for 15lovecoffee into ../archives/15lovecoffee. Include reels, tagged and IGTV where available; preserve normal post captions and metadata. If an authorized Instaloader session is available, include stories and highlights.
4. Stop on platform access restrictions and preserve partial files. If a long-running download is possible, use a bounded Vibe Kanban poller rather than a detached process.
5. Verify actual media counts, category coverage and command exit state. Document the exact command and outcome; do not mark an incomplete archive complete.
6. Independently review repository changes using Codex CLI and resolve significant findings.
7. Record reusable operational knowledge in homelab, commit each changed repo, and use Vibe Kanban Create PR and merge only after required CI passes. Download completion remains a separate acceptance gate.

## CI repair discovered during PR validation

Existing CI failed on the documentation-only commit: Python 3.9 has no Ubuntu
26.04 build, Pylint rejects the removed `suggestion-mode` option, and existing
list-only code has whitespace, line-length and import-placement findings.
Pin the lint job to Ubuntu 24.04 (confirmed in actions/python-versions manifest),
remove the obsolete option and fix those formatting/import findings without
changing downloader behavior. Independently review and run the existing CI.

Validation: independent `codex review --uncommitted` found no actionable
regressions in the CI repair. Local Pylint 4.0.2 scored 10.00/10 and MyPy
reported no issues. Remote matrix and build checks remain the merge gate.
