# Feature specification: synchronize Instaloader

Status: specified. Feature directory: specs/vk/7a98-sync-instaloader/.

## Summary
Bring the fork up to upstream master while retaining its list-only extension, so users receive upstream fixes without losing their existing workflow.

## User stories
- As the fork maintainer, I want upstream updates incorporated with traceable history.
- As a list-only user, I want enumeration without downloading posts to continue working.

## Functional requirements
- FR-1: Incorporate upstream 09dea80d2be81bed94e8d65717cf8684fcc2998b.
- FR-2: Retain fork --list-only behavior and existing fork history.
- FR-3: Provide reproducible checks and independent review evidence.
- FR-4: Deliver through a Vibe Kanban PR merged after passing CI.

## Out of scope
Package publication, releases, Instagram account operations, and homelab deployment.

## Acceptance criteria
- The upstream revision and fork baseline are both ancestors of the merged master.
- Offline regression tests prove list-only enumeration avoids downloads and regular mode still downloads.
- Relevant CI checks pass and independent review has no unresolved significant findings.
- Spec, plan, tasks, verification, and knowledge records are committed.

## Open questions
None. Both default branches are master; use that branch, retain the fork extension, and preserve history with a merge commit.

## Clarification record
/speckit.clarify: reviewed scope and acceptance criteria. Use upstream master at the recorded revision (not the upcoming/v4.16 branch); preserve --list-only. Live Instagram access is not an acceptance prerequisite. A merge commit is required to retain upstream ancestry. No open questions remain.
