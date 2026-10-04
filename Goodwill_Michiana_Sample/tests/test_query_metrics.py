"""Tests for the sample metrics connector/tool."""

from __future__ import annotations

import json
import asyncio

from sample_agent.agents.intelligence_agent.tools.query_metrics import create_query_metrics_tool


def test_query_metrics_returns_demo_data():
    tool = create_query_metrics_tool()
    result = json.loads(asyncio.run(tool.ainvoke({"metric": "summary", "limit": 2})))

    assert result["source"] == "goodwill_demo_data"
    assert result["metric"] == "summary"
    assert len(result["rows"]) == 2
