# Synchronizing this fork with upstream

Tags: `vk/7a98-sync-instaloader`, `7a98e576-c076-49f2-9b0a-ae948fd1520a`, `upstream-sync`, `instaloader`.

Both davidvasandani/instaloader and instaloader/instaloader use master. This sync incorporates upstream 09dea80d2be81bed94e8d65717cf8684fcc2998b into fork baseline c69eff0dbbcdb3691964af1893c4576eeb9efe5f. Preserve both ancestors using merge commits: squash/rebase loses the upstream ancestry that makes future syncs straightforward.

The fork adds --list-only and list_posts_to_file/list_saved_posts. Offline tests cover profile, hashtag, feed, and saved-post routing, filtering, limits, and login requirements. This is not a promise that every other CLI target supports list-only mode.

## Endpoint changes require conversion tests

The updated web-info response differs from the legacy Post/Profile representations:

- Convert nested location.pk and liker.pk to id without mutating input or replacing an existing id.
- Preserve existing play counts, including zero. Optional fallback rejection must not prevent use of valid media; explicit AbortDownloadException must still propagate.
- Normalize both caption edges and the fallback caption value. Keeping a raw caption dictionary breaks caption properties and filters when text is absent.
- Exclude empty video candidates and recover carousel video URLs from the authenticated iPhone response where available.

The new HTML profile/CSRF request path must retain configured retry limits, unlimited-attempt behavior, rate-controller 429 backoff, fatal-status aborts, and interrupt semantics. A first interrupt aborts; interrupting a retry skips that target through ConnectionException.

## Validation and delivery

Run `python -m unittest discover -s test -p 'test_*.py'`, `pylint instaloader`, `mypy -m instaloader`, and Sphinx with `-W -n`, using locked dependencies. The sync raises the upstream Python minimum to 3.10; CI tests 3.10–3.15, builds docs, and builds the Windows executable. Live Instagram integration tests live upstream in instaloader/instaloader-tests and require separate account/network validation.

Gate the documentation deployment step to github.repository == 'instaloader/instaloader'; otherwise a fork master push attempts deployment to upstream Pages. Keep fork documentation builds active. Open and merge via Vibe Kanban, using merge strategy after successful checks on the actual PR head.
