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

Independent Codex CLI review (against c69eff0) reproduced two P2 findings: valid play_count overwritten by a fallback, and raw requests exceptions escaping CSRF initialization. Fixed by retaining existing play counts (including zero) and translating initialization request failures to ConnectionException with the original cause. Added three offline test methods for preserved counts, missing-count fallback, and timeout/connection-error translation. All 10 tests pass; PyLint remains 10.00/10 and MyPy passes.

After removing generated packaging files, an archive wheel build passed and every packaged Python module matched its source byte-for-byte.

Second Codex review reproduced a P2 geotag failure: the new web-info response uses location.pk while Post.location expects location.id. Normalize a copied nested location dictionary, retaining an existing id and avoiding mutation of input. Regression coverage exercises pk-only, id-only, and both identifiers through Post.from_shortcode and Post.location.

Third review reproduced a P2 liker-ID mismatch: the new endpoint returns pk, causing Profile.userid and set operations to fetch each profile again. Copy pk to a missing id while preserving the source dictionary. A regression test confirms both pk and id inputs support set collection and ID reads without extra GraphQL requests.

Fourth review reproduced a P2 --abort-on regression in the new page-fetch path. Check fatal_status_codes before recoverable HTTP handling. The same guard now covers CSRF initialization (without following redirects), whose non-success responses become ConnectionException. Offline tests exercise fatal 302/404/429 in both paths and a recoverable nonfatal response.

Fifth review reproduced a P2 video-download failure when normalization supplies video_url=None and the iPhone endpoint supplies a valid alternative. Exclude empty candidates before URL comparison. A regression test covers absent/empty web versions, valid iPhone fallback, and no available video without iPhone support.

Sixth review reproduced two remaining P2 issues: absent carousel video URLs bypassed available iPhone alternatives, and HTML profile resolution lost retries/429 backoff. Added authenticated carousel fallback and a shared HTML request helper for profile pages and CSRF initialization. It preserves configured attempt limits (including unlimited zero), rate-controller backoff, fatal-status aborts, and Instaloader exception types. Regression coverage exercises carousel null/empty variants, timeout and 503 recovery, 429 backoff, retry exhaustion, and unlimited-mode recovery. All 18 offline tests pass; lint and type checks remain clean.

Seventh review reproduced two P2 error cases: a recoverable rejection of optional play-count lookup blocked usable video metadata, and Ctrl-C during a subsequent HTML retry escaped instead of skipping the target. Optional lookup now catches InstaloaderException while preserving explicit AbortDownloadException. HTML retries translate subsequent interrupts to ConnectionException; a first-attempt interrupt still propagates. Both behaviors have regression tests. All 20 offline tests pass with clean lint/type checks.

Eighth review found a P2 caption normalization failure: empty/null-text caption objects survived in the fallback field and caused TypeError. Set both the legacy edge representation and fallback caption field to normalized text. Tests cover missing, empty, populated object captions and legacy text; hashtags and mentions remain usable. All 21 tests pass. The review sandbox itself was read-only, so its seven file-writing list-only tests could not run; all run successfully in this workspace and CI.
