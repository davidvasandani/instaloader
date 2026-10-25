# Instaloader Tests

Integration tests for Instaloader features that require Instagram access are maintained here:
https://github.com/instaloader/instaloader-tests

Offline fork regression tests (no account or network access):

```sh
python -m unittest discover -s test -p "test_*.py"
```
