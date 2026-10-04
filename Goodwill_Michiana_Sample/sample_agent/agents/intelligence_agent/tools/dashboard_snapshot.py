"""Tool for capturing dashboard screenshots."""

from __future__ import annotations

import json
import logging

from langchain_core.tools import tool

from sample_agent.connectors.dashboard_connector import get_dashboard_connector

logger = logging.getLogger(__name__)


@tool
async def dashboard_snapshot(
    include_in_response: bool = True,
    filter_name: str | None = None,
    filter_value: str | None = None,
) -> str:
    """Capture a dashboard screenshot via REST image endpoint or Playwright.

    Use when the user asks to see a dashboard, screenshot, chart, visual, or browser state.
    The image is stored out-of-band and returned by the API response, not inserted into LLM context.
    """
    try:
        filters = {filter_name: filter_value} if filter_name and filter_value else None
        connector = get_dashboard_connector()
        result = await connector.capture_snapshot(filters=filters)

        if result.get("success") and include_in_response and result.get("image"):
            connector.store_image(
                result["image"],
                title=result.get("dashboard", "Dashboard Snapshot"),
                content_type=result.get("content_type", "image/png"),
            )

        return json.dumps(
            {
                "success": bool(result.get("success")),
                "dashboard": result.get("dashboard"),
                "mode": result.get("mode"),
                "filters": filters,
                "message": result.get("message"),
                "error": result.get("error"),
            }
        )
    except Exception as exc:
        logger.exception("dashboard_snapshot failed")
        return json.dumps({"success": False, "error": str(exc)})


def create_dashboard_snapshot_tool():
    """Factory for the dashboard snapshot tool."""
    return dashboard_snapshot

