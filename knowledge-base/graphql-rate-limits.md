# GraphQL throttling inside HTTP 200

Task: `527cbd5a-e0b3-41ba-9061-f80d8a6dad4c` / `vk/527c-download-15lovec`.

On 2026-11-24, public post metadata returned HTTP 200 with an errors list containing numeric code 1675004 and message Rate limit exceeded. Missing metadata was a downstream symptom, not proof of a schema change or a private account. Recognize the code at the GraphQL request boundary and use existing TooManyRequestsException cooldown/attempt handling. Do not classify unknown GraphQL errors by loose message matching.

The older fork's recursive get_json retry dropped use_post. Forward it so POST retries retain body semantics. Upstream 7acd1b6 uses an iterative retry loop and already preserves the method; its anonymous endpoint is api/graphql, which also needs payload classification.

Validation: fork 25 offline tests; upstream five focused tests; pylint 10/10 and mypy clean on both; separate Codex reviews found no actionable defects. A single patched live query returned the explicit rate-limit diagnostic. No successful post download is implied. Preview images remain a partial archive outside Git.

Upstream report: https://github.com/instaloader/instaloader/issues/2806.
