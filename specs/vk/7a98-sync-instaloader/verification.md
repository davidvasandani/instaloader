# Verification

- Fork baseline: c69eff0dbbcdb3691964af1893c4576eeb9efe5f.
- Upstream: 09dea80d2be81bed94e8d65717cf8684fcc2998b (27 upstream-only commits).
- Merge completed without conflicts; fork list-only methods and CLI routes preserved.
- Python 3.13: seven offline unittest cases passed, covering URL formatting, filtering/count limit, empty export, saved-post login guard, authenticated saved export, profile normal/list routing, saved CLI routing, feed and hashtag listing. Unexpected requests/downloads fail these tests.
- compileall and CLI --help passed; --list-only remains exposed.
- MyPy passed with locked dependencies. PyLint initially found fork whitespace/local import issues and the removed suggestion-mode configuration option. Fixed formatting, moved Hashtag import to module scope, and removed the obsolete option without disabling checks.
- Sphinx warnings-as-errors build passed; see docs-validation.md.
- Live Instagram integration tests were not run; upstream now maintains those in instaloader/instaloader-tests.
- Upstream requires Python >=3.10 and tests 3.10–3.15.
- Documentation deployment is gated to the upstream repository, preserving fork documentation builds without attempting upstream publication.

Independent review and GitHub CI results are recorded after execution.

After fixes: PyLint 10.00/10; MyPy clean; all seven offline tests pass; git diff --check clean.

Package archive check found that tracked build/lib files produced a wheel with six stale modules (including __init__, CLI, Instaloader, context, iterator, and structures). Remove generated build/ and egg-info from version control and ignore future output; rebuild and compare every wheel module against source. This is a necessary sync compatibility fix.
