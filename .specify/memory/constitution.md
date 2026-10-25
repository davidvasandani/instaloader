# Instaloader fork constitution

Version: 1.0.0. Adopted: 2026-10-25.

1. Preserve upstream Git history and fork-specific supported behavior, including --list-only. Synchronize through merge commits, never force-reset the fork.
2. Keep synchronization scoped to upstream changes and necessary compatibility fixes; do not publish releases or change unrelated infrastructure.
3. Validate with repeatable offline checks and available CI. Distinguish Instagram-dependent tests from tests actually run.
4. Review the diff independently and resolve significant findings before merging.
5. Record source revisions, decisions, validation, and reusable knowledge. Merge via a reviewed PR only after CI passes.
