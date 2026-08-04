"""Post-generation hook for ai-circus-template.

Runs after cookiecutter renders the project files:
1. Generates data_model.py + .env.example from settings.yaml (via `uv run`).
2. Initializes a local git repository with an initial commit.

Both steps are best-effort: if `uv` or `git` are unavailable, this hook prints
guidance instead of failing the whole generation.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

PACKAGE_NAME = "{{cookiecutter.package_name}}"
PROJECT_DIR = Path.cwd()


def _run(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True, cwd=PROJECT_DIR)  # noqa: S603
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def generate_data_model() -> None:
    """Generate data_model.py/.env.example from settings.yaml using `uv run`.

    Loads config_generator.py directly by file path rather than importing
    `{package}.core.config_generator` — the package's __init__ imports
    data_model.py, which does not exist yet at this point.
    """
    if not shutil.which("uv"):
        print(  # noqa: T201
            "⚠️  uv not found — skipping automatic data_model.py generation.\n"
            "   Install uv, then run 'make setup' (or 'make generate-data-model')."
        )
        return

    script = PROJECT_DIR / "_generate_data_model_tmp.py"
    script.write_text(
        "import importlib.util\n"
        "spec = importlib.util.spec_from_file_location(\n"
        f"    'config_generator', 'src/{PACKAGE_NAME}/core/config_generator.py'\n"
        ")\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n"
        f"module.generate_data_model('settings.yaml', 'src/{PACKAGE_NAME}/data_model.py', '.env.example')\n"
    )
    try:
        ok = _run(["uv", "run", "--", "python", script.name])
    finally:
        script.unlink(missing_ok=True)

    if ok:
        print("✓ Generated data_model.py and .env.example from settings.yaml")  # noqa: T201
    else:
        print("⚠️  Could not generate data_model.py automatically — run 'make setup' manually.")  # noqa: T201


def init_git() -> None:
    """Initialize a local git repository with an initial commit, if git is available."""
    if not shutil.which("git") or (PROJECT_DIR / ".git").exists():
        return
    if _run(["git", "init", "-q"]) and _run(["git", "add", "-A"]):
        _run(["git", "commit", "-q", "-m", "chore: initial scaffold from ai-circus-template"])
        print("✓ Initialized local git repository with an initial commit")  # noqa: T201


if __name__ == "__main__":
    generate_data_model()
    init_git()
