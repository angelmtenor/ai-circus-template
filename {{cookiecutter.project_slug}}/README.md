# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

---

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
![Package Version](https://img.shields.io/badge/Package%20Version-{{cookiecutter.version}}-green?style=for-the-badge)
![Supported Python Versions](https://img.shields.io/badge/Supported%20Python%20Versions-{{cookiecutter.python_version}}%2B-blue?style=for-the-badge)

---

## 🖥️ Prerequisites: Development Environment

This project targets Linux (native, WSL, remote VM, or a VS Code Dev Container):

- **macOS / native Linux:** already Unix-based — skip ahead to Quick Start.
- **Windows:** use **WSL** ([install guide](https://learn.microsoft.com/en-us/windows/wsl/install)).
- **Remote VM** (AWS/Azure/GCP/on-prem): provision a Linux base and connect over SSH.
- **VS Code Dev Container:** open this folder in VS Code and let it build `.devcontainer/Dockerfile`.

You'll need [uv](https://docs.astral.sh/uv/getting-started/installation/) installed to manage the virtual
environment and dependencies (the Dev Container installs it automatically).

---

## 🚀 Quick Start

Once your environment is ready, get the project up and running in seconds after cloning the
repository:

```bash
make setup    # Initialize venv, .env, generate settings, and verify environment
make check    # Run QA checks (linting) and tests
make run      # Run the main application
```

To verify everything end-to-end before a commit:
```bash
make all      # clean -> setup -> check -> run
```

---

## Project Layout

```
src/{{cookiecutter.package_name}}/
├── app.py              # Application entry point
├── core/               # Core infrastructure
│   ├── logger.py        # Loguru-based logging setup
│   ├── info.py           # System/environment info utilities
│   └── config_generator.py  # Generates data_model.py from settings.yaml
├── data_model.py       # Generated Pydantic Settings model (DO NOT EDIT DIRECTLY)
└── tools/              # Example command-line tools
    ├── hello_world.py
    └── check_service.py
```

---

## Configuration

The project uses a single source of truth for settings defined in `settings.yaml`.

1. Run `make setup` to initialize your `.env` file from `.env.example`.
2. Edit `.env` to fill in any secret values (e.g. `EXAMPLE_SERVICE_API_KEY`).
3. The application validates these at runtime using Pydantic Settings (`src/{{cookiecutter.package_name}}/data_model.py`).
4. After editing `settings.yaml`, run `make generate-data-model` to regenerate `data_model.py` and `.env.example`.

---

## Common Workflows

| Command | Description |
|---|---|
| `make clean` | Remove `.venv`, caches, and artifacts (with `.env` backup) |
| `make setup` | Full environment initialization and verification |
| `make check` | Run `qa` (linting) and `test` (unit tests) |
| `make run` | Execute the main application |
| `make qa` | Run pre-commit hooks (ruff, pyrefly, config drift check, etc.) |
| `make test` | Run the pytest suite |
| `make all` | Full end-to-end verification pipeline |
| `make update` | Upgrade lockfile, sync deps, update pre-commit hooks |
| `make generate-data-model` | Regenerate `data_model.py`/`.env.example` from `settings.yaml` |
| `make hello-world` | Run the hello-world demonstration tool |
| `make check-service` | Check connectivity to the example external service |
| `make build` | Build the distributable package |
| `make build-container` | Build the Docker image |
| `make run-container` | Build and run the Docker container |

Each tool target is a thin wrapper around a `uv run` console script — they're declared under
`[project.scripts]` in [pyproject.toml](pyproject.toml) and can be run directly without `make`,
e.g. `uv run {{cookiecutter.project_slug}}-hello-world`.

---

## Contributing

- Review the [Contributing Guidelines](CONTRIBUTING.md) for the workflow and submission process.
- Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- See [SECURITY.md](SECURITY.md) before deploying to production.
