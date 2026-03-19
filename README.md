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

By default, the server listens on `0.0.0.0:8000` and saves files to an `uploads` folder.

You can customize the server behavior using the following CLI arguments:
* `--port [PORT]`: Port to listen on (default: 8000)
* `--host [HOST]`: Address to listen on (default: 0.0.0.0)
* `--upload-dir [DIR]`: Directory to save uploaded files (default: uploads)
* `--message [MSG]`: Custom message to display on the web page

Example:
```sh
poetry run python3 -m upload_server --port 9000 --upload-dir custom_folder --message "My Upload Server"
```

Open the server URL from your phone browser using the host’s local IP address:

```
http://<host-ip>:<host-port>
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
* Filenames are automatically sanitized to prevent path traversal attacks.

---

## Security Disclaimers

* This server does not include authentication or encryption by default.
* Intended for local network use only.
* Do not expose to public networks without additional security measures.
* Use at your own risk. Review the code before production use.

## Security Note: Binding to `0.0.0.0`

The application explicitly defaults to binding to all network interfaces for convenience:

```python
parser.add_argument("--host", type=str, default="0.0.0.0",  # nosec B104
```

This triggers a Bandit warning (`B104: hardcoded_bind_all_interfaces`) because binding to `0.0.0.0` can expose a service to unintended networks.

### Why this is intentional

This server is designed to receive files from a **mobile device on the same local network**.
Defaulting to `0.0.0.0` is required so the service is reachable from other devices (e.g. a phone) out-of-the-box and not limited to `localhost`.

Binding only to `127.0.0.1` would prevent access from external devices and break the primary use case.

### Risk assessment

* ✔ Intended for **local network use only**
* ❌ No authentication or encryption by default
* ❌ Not hardened for public exposure

### Mitigations and user responsibility

* Users should **run this server only on trusted local networks**
* Firewall rules should restrict access as needed
* The server **must not be exposed to the public internet**
* Advanced users can override the bind address using the `--host` CLI argument (e.g., `--host 127.0.0.1`) if they want strict isolation.

The Bandit warning is therefore explicitly suppressed using `# nosec B104`, as this behavior is **by design and documented**.

---

**Summary:**
This is a conscious trade-off between usability and security, acceptable for a local-only utility but inappropriate for public-facing deployments.


## PyPI / GitHub Best Practices

* Includes pyproject.toml for dependency management and packaging.
* All source code is under a version-controlled repository.
* Templates and static assets are in separate folders for clean structure.
* Tests are included and run with pytest for continuous integration.
* Linting and security scanning are integrated for safe publishing.

## License

MIT
