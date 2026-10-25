# Tracked build output can replace updated package source

Tags: `vk/7a98-sync-instaloader`, `7a98e576-c076-49f2-9b0a-ae948fd1520a`, `packaging`, `setuptools`.

The original fork committed build/lib/instaloader and instaloader.egg-info. Building a wheel from git archive gave generated and source files the same extraction timestamps. Setuptools retained stale build/lib modules: the wheel contained six old modules even though imports and tests against the working source passed.

Remove generated build and egg-info files from version control and ignore build/, dist/, and *.egg-info/. A passing source test is insufficient evidence of package correctness.

To check a sync, extract `git archive HEAD` into a fresh directory, run `pip wheel --no-deps --wheel-dir <output> <extracted-directory>`, then compare every instaloader/*.py wheel entry byte-for-byte against the committed source. This reproduced the failure before cleanup and passed afterward. No release publication is needed for this check.
