"""Tests for Power BI screenshot side-channel behavior."""

from __future__ import annotations

import asyncio
import json

from sample_agent.agents.intelligence_agent.tools.powerbi_snapshot import create_powerbi_snapshot_tool
from sample_agent.connectors.powerbi_connector import PowerBIConnector


def test_powerbi_snapshot_stores_placeholder_image(monkeypatch):
    connector = PowerBIConnector()
    connector.image_export_url = ""
    connector.report_web_url = ""
    connector.report_name = "Goodwill Demo Report"
    monkeypatch.setattr(
        "sample_agent.agents.intelligence_agent.tools.powerbi_snapshot.get_powerbi_connector",
        lambda: connector,
    )

    tool = create_powerbi_snapshot_tool()
    result = json.loads(asyncio.run(tool.ainvoke({})))

    assert result["success"] is True
    assert result["mode"] == "placeholder"
    assert result["report"] == "Goodwill Demo Report"
    assert len(connector.pop_images()) == 1

