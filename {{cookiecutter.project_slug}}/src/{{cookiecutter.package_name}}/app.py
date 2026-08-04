"""
app.py
------

Entry point for {{cookiecutter.project_name}}.
Initializes configuration and logs environment state.

Author: {{cookiecutter.author_name}}
"""

from __future__ import annotations

import sys

from pydantic import ValidationError

from {{cookiecutter.package_name}} import get_env_config
from {{cookiecutter.package_name}}.core.logger import configure_logger, get_logger

logger = get_logger(__name__)


def main() -> None:
    """Main application entry point."""
    configure_logger()

    try:
        config = get_env_config()
    except ValidationError as e:
        logger.error("Configuration error: Mandatory environment variable(s) missing or invalid:")
        for error in e.errors():
            logger.error("  {}: {}", " -> ".join(str(loc) for loc in error["loc"]), error["msg"])
        sys.exit(1)

    lines = ["--- Initializing Application Settings ---"]
    # Accessed via type(config) rather than config directly: Pydantic v2 deprecates
    # (and v3 removes) reading model_fields off an instance.
    for field_name in type(config).model_fields:
        val = getattr(config, field_name)
        if hasattr(val, "get_secret_value"):
            secret_val = val.get_secret_value()
            val = "****" + secret_val[-4:] if secret_val else "None"
        lines.append(f"  {field_name}: {val}")

    logger.info("\n" + "\n".join(lines))
    logger.success("{} started successfully.", "{{cookiecutter.project_name}}")


if __name__ == "__main__":
    main()
