"""Tool for capturing Power BI report screenshots."""

from __future__ import annotations

import json
import logging

from langchain_core.tools import tool

from sample_agent.connectors.powerbi_connector import get_powerbi_connector

logger = logging.getLogger(__name__)


@tool
async def powerbi_snapshot(
    include_in_response: bool = True,
    page_name: str | None = None,
    filter_name: str | None = None,
    filter_value: str | None = None,
) -> str:
    """Capture a Power BI report screenshot."""
    try:
        filters = {filter_name: filter_value} if filter_name and filter_value else None
        connector = get_powerbi_connector()
        result = await connector.capture_report_snapshot(page_name=page_name, filters=filters)

        if result.get("success") and include_in_response and result.get("image"):
            connector.store_image(
                result["image"],
                title=result.get("report", "Power BI Report Snapshot"),
                content_type=result.get("content_type", "image/png"),
            )

        return json.dumps(
            {
                "success": bool(result.get("success")),
                "report": result.get("report"),
                "mode": result.get("mode"),
                "page_name": page_name,
                "filters": filters,
                "message": result.get("message"),
                "error": result.get("error"),
            }
        )
    except Exception as exc:
        logger.exception("powerbi_snapshot failed")
        return json.dumps({"success": False, "error": str(exc)})


def create_powerbi_snapshot_tool():
    """Factory for the Power BI snapshot tool."""
    return powerbi_snapshot

