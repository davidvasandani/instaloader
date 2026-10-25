# Tasks

Plan: ./plan.md. Dependencies are serial except the explicitly independent verification layer.

- [x] T001 Register/attach repository and create workspace branch; preserve root pipeline artifacts and .specify/memory/constitution.md.
- [x] T002 Merge upstream 09dea80d into branch; inspect instaloader/ and all changed upstream paths, preserving --list-only (depends T001).
- [x] T003 Add offline compatibility tests in test/test_list_only.py and wire into .github/workflows/lint.yml; gate deployment in .github/workflows/documentation.yml; resolve compatibility failures (depends T002).
- [x] T004 [P] Run offline tests, lint/type checks, and package smoke checks; record in specs/vk/7a98-sync-instaloader/verification.md (depends T003).
- [x] T005 [P] Build Sphinx documentation; record result in specs/vk/7a98-sync-instaloader/docs-validation.md (depends T003).
- [x] T006 Independent Codex review of full diff; fix significant findings and re-verify; record review evidence (depends T004,T005).
- [x] T007 Add knowledge-base/instaloader-upstream-sync.md and refresh knowledge-base/index.md, tagged vk/7a98-sync-instaloader; commit records (depends T006).
- [x] T008 Prepare delivery records and validate that both upstream and fork baseline are ancestors of the topic branch (depends T007).

## External delivery gate

After this committed implementation checklist: open the Vibe Kanban PR, require passing checks on its current head, merge with merge strategy, and verify both ancestors on origin/master. The GitHub PR state and checks are the authoritative completion record for this gate; this pre-merge document does not claim the PR has already merged.
