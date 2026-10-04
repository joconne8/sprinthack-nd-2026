"""Tool for querying Goodwill Michiana demo business metrics."""

from __future__ import annotations

import json
import logging
from typing import Literal

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from sample_agent.connectors.warehouse import get_warehouse_connector, serialize_rows

logger = logging.getLogger(__name__)


class QueryMetricsInput(BaseModel):
    """Input schema for the metrics query tool."""

    metric: Literal["summary", "retail", "donations", "workforce", "incidents"] = Field(
        default="summary",
        description="Goodwill metric family to retrieve.",
    )
    limit: int = Field(default=10, ge=1, le=100, description="Maximum rows to return.")


def create_query_metrics_tool() -> StructuredTool:
    """Create a LangChain tool that reads from SQL or Goodwill demo rows."""

    async def query_metrics(metric: str = "summary", limit: int = 10) -> str:
        """Fetch trusted operating metrics from the configured warehouse or demo data."""
        try:
            connector = get_warehouse_connector()
            rows = connector.query_metric(metric=metric, limit=limit)
            return serialize_rows({"source": connector.source_name, "metric": metric, "rows": rows})
        except Exception as exc:
            logger.exception("query_metrics failed")
            return json.dumps({"success": False, "error": str(exc), "metric": metric})

    return StructuredTool.from_function(
        func=query_metrics,
        coroutine=query_metrics,
        name="query_metrics",
        description=(
            "Query Goodwill Michiana operating metrics. Use for retail store performance, donations, "
            "workforce program outcomes, mission services, and operational incidents. Returns demo data "
            "if WAREHOUSE_DSN is not configured."
        ),
        args_schema=QueryMetricsInput,
    )
