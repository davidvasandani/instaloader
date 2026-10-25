# Tasks

Plan: ./plan.md. Dependencies are serial except the explicitly independent verification layer.

- [x] T001 Register/attach repository and create workspace branch; preserve root pipeline artifacts and .specify/memory/constitution.md.
- [x] T002 Merge upstream 09dea80d into branch; inspect instaloader/ and all changed upstream paths, preserving --list-only (depends T001).
- [x] T003 Add offline compatibility tests in test/test_list_only.py and wire into .github/workflows/lint.yml; gate deployment in .github/workflows/documentation.yml; resolve compatibility failures (depends T002).
- [x] T004 [P] Run offline tests, lint/type checks, and package smoke checks; record in specs/vk/7a98-sync-instaloader/verification.md (depends T003).
- [x] T005 [P] Build Sphinx documentation; record result in specs/vk/7a98-sync-instaloader/docs-validation.md (depends T003).
- [ ] T006 Independent Codex review of full diff; fix significant findings and re-verify; record review evidence (depends T004,T005).
- [ ] T007 Add knowledge-base/instaloader-upstream-sync.md and refresh knowledge-base/index.md, tagged vk/7a98-sync-instaloader; commit records (depends T006).
- [ ] T008 Open Vibe Kanban PR, verify passing CI on current head, merge preserving history, and verify master ancestry (depends T007).
