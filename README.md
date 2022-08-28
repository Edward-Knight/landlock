# [🔒🐍 Landlock for Python](https://github.com/Edward-Knight/landlock)

[![PyPI - Status](https://img.shields.io/pypi/status/landlock)](https://pypi.org/project/landlock/)
[![PyPI - License](https://img.shields.io/pypi/l/landlock)](https://pypi.org/project/landlock/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/landlock)](https://pypi.org/project/landlock/)
[![PyPI - Latest Project Version](https://img.shields.io/pypi/v/landlock)](https://pypi.org/project/landlock/)
[![GitHub Workflow Status (main)](https://img.shields.io/github/workflow/status/Edward-Knight/landlock/test/main)](https://github.com/Edward-Knight/landlock/actions/workflows/test.yml?query=branch%3Amain)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Edward-Knight/landlock/main.svg)](https://results.pre-commit.ci/latest/github/Edward-Knight/landlock/main)

Harden your Python code by with rule-based file system access restrictions.

## Example

Let's write a simple HTTP server that serves files in the local directory.

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(("", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
```

But if there's a symlink in the local directory, the program can "escape".

```shell
$ ln -s /etc oops
$ python3 test.py &
[1] ...
$ curl localhost:8000
...
$ curl localhost:8000/oops/passwd
uh oh
$ kill $!
[1]+  Terminated              python3 test.py
```

Now let's harden our server with Landlock!

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

from landlock import Ruleset

server = HTTPServer(("", 8000), SimpleHTTPRequestHandler)

# the ruleset by default disallows all filesystem access
rs = Ruleset()
# explicitly allow access to the local directory hierarchy
rs.allow(".")
# turn on protections
rs.apply()

server.serve_forever()
```

And now we get a permission denied error if we try and access files outside the current directory,
even via a symlink:

```shell
$ python3 test.py &
[1] ...
$ curl localhost:8000
...
$ curl localhost:8000/oops/
127.0.0.1 - - [DD/MMM/YYYY HH:MM:SS] code 404, message No permission to list directory
...
$ kill $!
[1]+  Terminated              python3 test.py
```

Success! Instead of dumping the password file, we instead get a permission error!

Landlock is great for hardening applications against both accidental programming mistakes,
and attacks.
It won't prevent an exploited application from all malicious behavior,
but it can stop it reading with the filesystem and interacting with device files.

## Developer Information

## Testing

Tests are run using [pytest](https://docs.pytest.org/en/latest/).
Each test is run in a separate subprocess using [pytest-forked](https://github.com/pytest-dev/pytest-forked)
so Landlock rules don't conflict.
