"""Tool: Check connectivity to an example external service.

Demonstrates a small, reusable HTTP client pattern for verifying that a
configured external API is reachable and responding. Replace the example
service with your own integration(s).

Author: {{cookiecutter.author_name}}
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import httpx

from {{cookiecutter.package_name}} import get_env_config
from {{cookiecutter.package_name}}.core.info import info_system
from {{cookiecutter.package_name}}.core.logger import configure_logger, get_logger

logger = get_logger(__name__)


@dataclass
class APIConfig:
    """Configuration for an API endpoint and request parameters."""

    name: str
    url: str | Callable[[str], str]
    method: str = "GET"
    headers: dict[str, str] | Callable[[str], dict[str, str]] | None = None
    json: dict[str, str] | Callable[[str], dict[str, str]] | None = None
    params: dict[str, str] | Callable[[str], dict[str, str]] | None = None


def resolve_api_config(config: APIConfig, api_key: str) -> APIConfig:
    """Resolve dynamic APIConfig callables without mutating the source config."""
    return APIConfig(
        name=config.name,
        url=config.url(api_key) if callable(config.url) else config.url,
        method=config.method,
        headers=config.headers(api_key) if callable(config.headers) else config.headers,
        json=config.json(api_key) if callable(config.json) else config.json,
        params=config.params(api_key) if callable(config.params) else config.params,
    )


class APIClient:
    """Generic API client for making HTTP requests."""

    @staticmethod
    def fetch_data(config: APIConfig) -> dict | None:
        """Fetch data from an API with the given configuration."""
        try:
            with httpx.Client() as client:
                request_kwargs: dict = {"url": config.url, "timeout": 10.0}
                if config.headers:
                    request_kwargs["headers"] = config.headers
                if config.params:
                    request_kwargs["params"] = config.params
                # Only include json for POST requests
                if config.method.upper() == "POST":
                    request_kwargs["json"] = config.json

                if config.method.upper() == "GET":
                    response = client.get(**request_kwargs)
                else:
                    response = client.post(**request_kwargs)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    resp = e.response
                    body = resp.text if resp is not None else "<no response body>"
                    status = resp.status_code if resp is not None else "<no status>"
                    logger.error(f"Failed to fetch {config.name} data: status={status} body={body}")
                    return None
                try:
                    return response.json()
                except ValueError:
                    logger.error(f"Non-JSON response from {config.name}: {response.text}")
                    return None
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch {config.name} data: {e}")
            return None


def main() -> None:
    """Main function to execute the example service connectivity check."""
    configure_logger(level="INFO")
    logger.info("Starting the script...")
    info_system()
    config = get_env_config()

    api_key = config.EXAMPLE_SERVICE_API_KEY.get_secret_value() if config.EXAMPLE_SERVICE_API_KEY else ""
    if not api_key:
        logger.warning("EXAMPLE_SERVICE_API_KEY is not set — checking anonymous connectivity only.")

    example_config = APIConfig(
        name="ExampleService",
        url=f"{config.EXAMPLE_SERVICE_BASE_URL}/get",
        headers=(lambda key: {"Authorization": f"Bearer {key}"}) if api_key else None,
    )

    client = APIClient()
    data = client.fetch_data(resolve_api_config(example_config, api_key))
    if data:
        logger.info(f"ExampleService reachable: {config.EXAMPLE_SERVICE_BASE_URL}")
    else:
        logger.error(f"ExampleService unreachable: {config.EXAMPLE_SERVICE_BASE_URL}")


if __name__ == "__main__":
    main()
