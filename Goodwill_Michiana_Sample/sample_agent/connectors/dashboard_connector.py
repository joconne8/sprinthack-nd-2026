"""Generic BI/dashboard connector with screenshot side-channel storage."""

from __future__ import annotations

import base64
import logging
import os
from typing import Any

import httpx

from sample_agent.connectors.screenshot import capture_page_screenshot, normalize_filter_params, placeholder_png_bytes

logger = logging.getLogger(__name__)


class DashboardConnector:
    """Capture dashboard snapshots via REST images, browser screenshots, or a placeholder."""

    def __init__(
        self,
        image_url: str | None = None,
        web_url: str | None = None,
        auth_token: str | None = None,
        dashboard_name: str | None = None,
    ) -> None:
        self.image_url = image_url if image_url is not None else os.getenv("DASHBOARD_IMAGE_URL", "")
        self.web_url = web_url if web_url is not None else os.getenv("DASHBOARD_WEB_URL", "")
        self.auth_token = auth_token if auth_token is not None else os.getenv("DASHBOARD_AUTH_TOKEN", "")
        self.dashboard_name = dashboard_name if dashboard_name is not None else os.getenv(
            "DASHBOARD_NAME", "Sample Operating Dashboard"
        )
        self._captured_images: list[dict[str, Any]] = []

    def store_image(self, image_bytes: bytes, title: str, content_type: str = "image/png") -> None:
        """Store an image for later API response attachment."""
        self._captured_images.append(
            {
                "data": base64.b64encode(image_bytes).decode("utf-8"),
                "content_type": content_type,
                "filename": "dashboard_snapshot.png",
                "title": title,
            }
        )

    def pop_images(self) -> list[dict[str, Any]]:
        """Return and clear pending captured images."""
        images = self._captured_images
        self._captured_images = []
        return images

    async def capture_snapshot(self, filters: dict[str, str] | None = None) -> dict[str, Any]:
        """Capture a dashboard image using the best configured mode."""
        if self.image_url:
            return await self._capture_rest_image(filters=filters)
        if self.web_url:
            return await self._capture_browser_image(filters=filters)

        return {
            "success": True,
            "image": placeholder_png_bytes(),
            "dashboard": self.dashboard_name,
            "content_type": "image/png",
            "mode": "placeholder",
            "message": "No dashboard provider configured, returned a placeholder image.",
        }

    async def _capture_rest_image(self, filters: dict[str, str] | None = None) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        params = normalize_filter_params(filters)
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(self.image_url, headers=headers, params=params)
            response.raise_for_status()

        return {
            "success": True,
            "image": response.content,
            "dashboard": self.dashboard_name,
            "content_type": response.headers.get("content-type", "image/png"),
            "mode": "rest_image",
            "message": "Dashboard image captured from REST endpoint.",
        }

    async def _capture_browser_image(self, filters: dict[str, str] | None = None) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        image = await capture_page_screenshot(self.web_url, headers=headers)
        return {
            "success": True,
            "image": image,
            "dashboard": self.dashboard_name,
            "content_type": "image/png",
            "mode": "playwright",
            "filters": filters,
            "message": "Dashboard image captured from browser page.",
        }


_connector: DashboardConnector | None = None


def get_dashboard_connector() -> DashboardConnector:
    """Get the process-local dashboard connector."""
    global _connector
    if _connector is None:
        _connector = DashboardConnector()
    return _connector

