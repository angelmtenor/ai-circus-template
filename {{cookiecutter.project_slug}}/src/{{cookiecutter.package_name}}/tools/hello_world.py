"""Tool "Hello World" for {{cookiecutter.project_name}}.
Author: {{cookiecutter.author_name}}
"""

from __future__ import annotations

from {{cookiecutter.package_name}} import get_env_config
from {{cookiecutter.package_name}}.core.info import info_system
from {{cookiecutter.package_name}}.core.logger import configure_logger, get_logger

logger = get_logger(__name__)


class SimpleClass:
    """A simple class for demonstration purposes."""

    def __init__(self, name: str) -> None:
        """Initialize the class with a name."""
        self.name = name

    def greet(self) -> None:
        """Print a greeting message."""
        logger.info(f"Hello, {self.name}!")


def main() -> None:
    """Main function to demonstrate the functionality of the module."""
    configure_logger()
    info_system()
    config = get_env_config()
    simple = SimpleClass(config.LOG_LEVEL)
    simple.greet()


if __name__ == "__main__":
    main()
