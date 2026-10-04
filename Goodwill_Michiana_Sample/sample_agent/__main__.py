"""CLI entry point for the sample service."""

from __future__ import annotations

import sys

import uvicorn

from sample_agent.settings import Settings


def main() -> None:
    settings = Settings()
    uvicorn.run(
        "sample_agent.app:create_app",
        factory=True,
        host=settings.http_host,
        port=settings.http_port,
        log_level="info",
        reload="--reload" in sys.argv,
    )


if __name__ == "__main__":
    main()

