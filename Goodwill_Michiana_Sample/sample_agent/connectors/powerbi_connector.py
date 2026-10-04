"""Power BI screenshot connector."""

from __future__ import annotations

import base64
import os
from typing import Any

import httpx

from sample_agent.connectors.screenshot import capture_page_screenshot, placeholder_png_bytes


class PowerBIConnector:
    """Capture Power BI report images via export endpoint, browser screenshot, or placeholder."""

    def __init__(self) -> None:
        self.image_export_url = os.getenv("POWERBI_IMAGE_EXPORT_URL", "")
        self.report_web_url = os.getenv("POWERBI_REPORT_WEB_URL", "")
        self.bearer_token = os.getenv("POWERBI_BEARER_TOKEN", "")
        self.report_name = os.getenv("POWERBI_REPORT_NAME", "Goodwill Michiana Operations Dashboard")
        self._captured_images: list[dict[str, Any]] = []

    def store_image(self, image_bytes: bytes, title: str, content_type: str = "image/png") -> None:
        """Store an image for later API response attachment."""
        self._captured_images.append(
            {
                "data": base64.b64encode(image_bytes).decode("utf-8"),
                "content_type": content_type,
                "filename": "powerbi_snapshot.png",
                "title": title,
            }
        )

    def pop_images(self) -> list[dict[str, Any]]:
        """Return and clear pending captured images."""
        images = self._captured_images
        self._captured_images = []
        return images

    async def capture_report_snapshot(
        self,
        page_name: str | None = None,
        filters: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Capture a report snapshot using the best configured mode."""
        if self.image_export_url:
            return await self._capture_rest_image(page_name=page_name, filters=filters)
        if self.report_web_url:
            return await self._capture_browser_image(page_name=page_name, filters=filters)

        return {
            "success": True,
            "image": placeholder_png_bytes(),
            "report": self.report_name,
            "content_type": "image/png",
            "mode": "placeholder",
            "message": "No Power BI provider configured, returned a placeholder image.",
        }

    async def _capture_rest_image(
        self,
        page_name: str | None = None,
        filters: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        params = {"pageName": page_name} if page_name else {}
        if filters:
            params.update({f"filter_{key}": value for key, value in filters.items()})

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(self.image_export_url, headers=headers, params=params)
            response.raise_for_status()

        return {
            "success": True,
            "image": response.content,
            "report": self.report_name,
            "content_type": response.headers.get("content-type", "image/png"),
            "mode": "rest_image",
            "message": "Power BI image captured from configured export endpoint.",
        }

    async def _capture_browser_image(
        self,
        page_name: str | None = None,
        filters: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        image = await capture_page_screenshot(self.report_web_url, headers=headers)
        return {
            "success": True,
            "image": image,
            "report": self.report_name,
            "content_type": "image/png",
            "mode": "playwright",
            "page_name": page_name,
            "filters": filters,
            "message": "Power BI image captured from browser page.",
        }


_connector: PowerBIConnector | None = None


def get_powerbi_connector() -> PowerBIConnector:
    """Get the process-local Power BI connector."""
    global _connector
    if _connector is None:
        _connector = PowerBIConnector()
    return _connector

