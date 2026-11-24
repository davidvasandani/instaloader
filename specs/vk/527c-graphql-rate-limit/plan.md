# /speckit.plan
Python requests library, no new dependencies or storage. In instaloader/instaloadercontext.py:get_json inspect GraphQL errors after JSON decoding and before status checks. Safely ignore non-list errors and non-dict entries. Raise TooManyRequestsException for code 1675004, reuse existing controller and limits. Forward use_post in the recursive retry.
Regression tests in test/test_graphql_rate_limits.py use mocked requests and controller, avoiding real waits/network. Run unittest, pylint, mypy; test the same patch against upstream/master in an isolated worktree. Independent Codex review then PR and required CI.
Constitution check: bounded existing policy, no bypass, no secret fixtures, no list-only change. No data model or external contract change.
