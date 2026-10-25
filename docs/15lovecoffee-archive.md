# 15lovecoffee archive attempt

Status: **blocked, no media downloaded** (2026-10-25). Instagram returned
HTTP 403 Forbidden on the initial GraphQL query. Instaloader exited 4.
This is not evidence that the profile is empty, private or nonexistent.

Source checkout: `c69eff0dbbcdb3691964af1893c4576eeb9efe5f`.
The CLI imported successfully with the available Python dependencies.
No session files were found in the current user's standard configuration
location or the checked temporary Instaloader directories.

From the workspace root, the attempted command was:

```sh
python3 instaloader/instaloader.py \
  --dirname-pattern "$PWD/archives/{target}" \
  --reels --tagged --igtv \
  --max-connection-attempts 1 --request-timeout 20 \
  --abort-on 401,403,429 15lovecoffee
```

The process was additionally bounded to 50 seconds using Python
`subprocess.run(timeout=50)`. It returned before that timeout.
No fast-update, date or count filter was used. Default photos, carousel
media, videos, captions, compressed metadata and profile picture remained enabled.

## Coverage

| Category | Outcome |
| --- | --- |
| Posts, carousel media, videos, captions, metadata, profile picture | Blocked before profile resolution |
| Reels, tagged posts, IGTV | Requested; blocked before enumeration |
| Current stories, highlights | Not attempted: require login |
| Comments, geotags | Not requested: require login |

The intended destination is `archives/15lovecoffee/` at the workspace root,
outside both Git repositories. Zero files exist there. Diagnostic files
`archives/15lovecoffee-attempt.log` and `archives/15lovecoffee-attempt.json`
record output, the exact command, elapsed time and exit code outside Git.

## Resume prerequisites

An authorized Instaloader session and its login username are needed for an
authenticated retry. A session may still encounter platform restrictions;
a 403 alone does not prove that authentication will fix access. Do not export
credentials from another service's managed browser. Use Instaloader's
`--login USERNAME --sessionfile /private/path` mechanism and include
`--stories --highlights --comments --geotags` for authenticated coverage.
Keep session material outside Git. Stop on login challenges or throttling.

Retain the same output location on retry. Verify successful enumeration of
each category and count downloaded media before reporting completion.
Deleted and expired content cannot be recovered by this operation.
