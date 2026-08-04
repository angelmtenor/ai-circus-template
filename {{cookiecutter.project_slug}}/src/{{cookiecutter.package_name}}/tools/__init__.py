"""Tools module for {{cookiecutter.project_name}}.

This module provides command-line tools and utilities:
- hello_world: Basic demonstration tool
- check_service: Verify connectivity to an example external service
"""

from __future__ import annotations

from .check_service import main as check_service
from .hello_world import main as hello_world

__all__ = [
    "check_service",
    "hello_world",
]
