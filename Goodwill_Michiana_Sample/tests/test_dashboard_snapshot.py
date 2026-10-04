"""Tests for screenshot side-channel behavior."""

from __future__ import annotations

import json
import asyncio

from sample_agent.agents.intelligence_agent.tools.dashboard_snapshot import create_dashboard_snapshot_tool
from sample_agent.connectors.dashboard_connector import DashboardConnector


def test_dashboard_snapshot_stores_placeholder_image(monkeypatch):
    connector = DashboardConnector(image_url="", web_url="", dashboard_name="Demo Dashboard")
    monkeypatch.setattr(
        "sample_agent.agents.intelligence_agent.tools.dashboard_snapshot.get_dashboard_connector",
        lambda: connector,
    )

    tool = create_dashboard_snapshot_tool()
    result = json.loads(asyncio.run(tool.ainvoke({})))

    assert result["success"] is True
    assert result["mode"] == "placeholder"
    assert result["dashboard"] == "Demo Dashboard"
    assert len(connector.pop_images()) == 1


def test_dashboard_snapshot_can_skip_response_image(monkeypatch):
    connector = DashboardConnector(image_url="", web_url="", dashboard_name="Demo Dashboard")
    monkeypatch.setattr(
        "sample_agent.agents.intelligence_agent.tools.dashboard_snapshot.get_dashboard_connector",
        lambda: connector,
    )

    tool = create_dashboard_snapshot_tool()
    result = json.loads(asyncio.run(tool.ainvoke({"include_in_response": False})))

    assert result["success"] is True
    assert connector.pop_images() == []
