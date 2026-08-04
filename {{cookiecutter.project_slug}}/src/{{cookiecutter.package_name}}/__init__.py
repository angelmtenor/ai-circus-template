"""{{cookiecutter.project_name}}: {{cookiecutter.project_description}}

Main components:
- core: Core infrastructure (logger, system info, settings generator)
- data_model: Validated environment configuration (Pydantic Settings)
- tools: Command-line tools and utilities
"""

from __future__ import annotations

from {{cookiecutter.package_name}}.core.logger import get_logger
from {{cookiecutter.package_name}}.data_model import get_env_config

__version__ = "{{cookiecutter.version}}"
__author__ = "{{cookiecutter.author_name}}"
__all__: list[str] = [
    "get_env_config",
    "get_logger",
]
