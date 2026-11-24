# /speckit.specify: GraphQL rate-limit handling
P1: A user whose GraphQL query receives HTTP 200 with rate-limit code 1675004 gets rate-controller backoff and a bounded retry, rather than an unrelated metadata error.
P1: A retried POST retains its method and payload.
P2: Exhaustion reports the throttle explicitly; ordinary success and unrelated/malformed error entries retain current behavior.
Acceptance: synthetic throttle-then-success, exhaustion, HTTP 429, GET/POST and unrelated response regression tests pass. No request bypass or guaranteed archive completion. No public API signature change.

/speckit.clarify: Match numeric error code 1675004 only for GraphQL requests, not message substrings or arbitrary API bodies. Apply existing max-connection-attempts and interrupt semantics. --abort-on remains an HTTP status filter: HTTP 200 errors do not become literal HTTP 429. No open questions.
