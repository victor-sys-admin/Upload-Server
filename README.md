# Upload Server

A lightweight Python web server for transferring files from a mobile device to a macOS host over a local network.
Built with Flask, designed for simplicity, testability, and local-only usage.

---

## Requirements

* Python **3.12**
* [Poetry](https://python-poetry.org/)
* macOS (tested)
* Phone and host on the **same local network**

---

## Installation

Clone the repository and set up the development environment using Poetry:

```sh
git clone <repo-url>
cd upload_server
```

```sh
poetry env use python3.12
poetry env activate
poetry install --no-root
```

---

## Running the Server

Start the upload server locally:

```sh
poetry run python3 -m upload_server
```

By default, the server listens on port **8000**.

Open the server URL from your phone browser using the host’s local IP address:

```
http://<host-ip>:8000
```

### Firewall note

Make sure to **temporarily allow incoming connections** for Python in your system firewall settings, or disable the firewall for local testing.

---

## Development

### Linting

Run static analysis with `pylint`:

```sh
poetry run pylint --ignore="tests" --recursive=y .
```

---

### Security Analysis

Run a security scan using `bandit`:

```sh
poetry run bandit . -r --exclude "./tests"
```

Optional: export results to a file with severity filtering:

```sh
poetry run bandit . -r --exclude "./tests" -o bandit.txt -f txt --severity-level medium
```

---

### Testing and Coverage

Run the test suite with coverage:

```sh
poetry run coverage run -m pytest
```

Generate a coverage report:

```sh
poetry run coverage report
```

Optional HTML report:

```sh
poetry run coverage html
```

---

## Notes

* This server is intended for **local network use only**
* No authentication or encryption is enabled by default
* Do not expose this service to public networks without additional security measures

---

## Security Disclaimers

* This server does not include authentication or encryption by default.
* Intended for local network use only.
* Do not expose to public networks without additional security measures.
* Use at your own risk. Review the code before production use.

## PyPI / GitHub Best Practices

* Includes pyproject.toml for dependency management and packaging.
* All source code is under a version-controlled repository.
* Templates and static assets are in separate folders for clean structure.
* Tests are included and run with pytest for continuous integration.
* Linting and security scanning are integrated for safe publishing.

## License

MIT
