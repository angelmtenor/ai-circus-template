# ai-circus-template

A [cookiecutter](https://cookiecutter.readthedocs.io/) template for scaffolding general-purpose
Python projects — packaging, backend services, CLIs, libraries, anything that isn't GenAI/LLM
specific. Distilled from [ai-circus](https://github.com/angelmtenor/ai-circus)'s core
infrastructure (logging, system info, validated environment configuration) with all GenAI/LLM
packages and tooling removed.

## What you get

- **`core/`** — Loguru-based logging (`core/logger.py`), system/environment info utilities
  (`core/info.py`), and a settings-model generator (`core/config_generator.py`) that turns a
  declarative `settings.yaml` into a validated `pydantic-settings` model (`data_model.py`), plus a
  matching `.env.example`.
- **`tools/`** — two example CLI tools (`hello_world`, `check_service`) showing the intended usage
  pattern for new tools.
- **`app.py`** — a minimal application entry point wired to the generated config and logger.
- Full dev tooling: `uv`, `ruff`, `pyrefly`/`ty`, `pytest` + coverage, `pre-commit` (incl.
  `gitleaks`), a `Makefile`, Dockerfile (multi-stage), a VS Code Dev Container, and a GitHub
  Actions CI workflow mirroring `make check`.
- Repo scaffolding: `LICENSE` (MIT/Apache-2.0/Proprietary), `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `SECURITY.md`, PR template.
- **Agent-agnostic AI instructions**: `AGENTS.md` (security rules, human-in-the-loop protocol,
  verification requirements) and `SKILLS.md` (architecture/coding standards) are the source of
  truth; `CLAUDE.md`, `GEMINI.md`, and `.github/copilot-instructions.md` are thin pointers back to
  them, plus `.copilotignore`/`.geminiignore` to keep secrets out of agent context.


## Prerequisites

This template (and the projects it generates) targets Linux — native, WSL, a remote VM, or a
VS Code Dev Container:

- If you don't already have it, install [VS Code](https://code.visualstudio.com/download) on your
  **host machine** first. For **WSL**, add the
  [Remote - WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
  ("WSL: Connect to WSL"); for a **remote VM**, add the
  [Remote - SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
  ("Remote-SSH: Connect to Host...").
- **Windows:** use **WSL** ([install guide](https://learn.microsoft.com/en-us/windows/wsl/install)).
- Install [Docker](https://docs.docker.com/engine/install/ubuntu/) — needed for the generated
  project's Dockerfile/Dev Container.

## Usage

```bash
uv tool install cookiecutter   # or: pipx install cookiecutter
cookiecutter /path/to/ai-circus-template
```

You'll be prompted for `project_name`, `author_name`, `author_email`, `license`, `python_version`,
etc. After generation, the post-generation hook will:

1. Run the settings generator (via `uv run`) to produce `data_model.py` and `.env.example` from
   `settings.yaml`.
2. Initialize a local git repository with an initial commit.

Then, inside the generated project:

```bash
make setup
make check
make run
```

## Customizing

- Add new env vars in `settings.yaml`, then run `make generate-data-model`.
- Add new CLI tools under `src/<package_name>/tools/`, and register them as `[project.scripts]`
  in `pyproject.toml`.
- Replace the `check_service` example with your own external API integration.

## Template variables

See [cookiecutter.json](cookiecutter.json) for the full list of prompts (project name/slug/package
name, description, author, license, Python version, etc.).
