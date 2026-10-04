"""Goodwill-oriented warehouse connector with deterministic demo fallback."""

from __future__ import annotations

import json
import os
from datetime import date
from decimal import Decimal
from typing import Any


class WarehouseConnector:
    """Read metrics from SQL when configured, otherwise return Goodwill demo rows."""

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn if dsn is not None else os.getenv("WAREHOUSE_DSN", "")
        self.engine = self._create_engine(self.dsn) if self.dsn else None

    @property
    def source_name(self) -> str:
        return "warehouse" if self.engine else "goodwill_demo_data"

    def query_metric(self, metric: str, limit: int = 10) -> list[dict[str, Any]]:
        """Query a generic metrics view or return demo data."""
        if not self.engine:
            return self._demo_rows(metric=metric, limit=limit)

        from sqlalchemy import text

        query = text(
            """
            SELECT metric_date, metric_family, metric_name, location, value, status, notes
            FROM public.goodwill_operations_metrics_v
            WHERE metric_family = :metric OR :metric = 'summary'
            ORDER BY metric_date DESC, metric_family, metric_name
            LIMIT :limit
            """
        )
        with self.engine.connect() as conn:
            result = conn.execute(query, {"metric": metric, "limit": limit})
            columns = list(result.keys())
            return [dict(zip(columns, row)) for row in result]

    @staticmethod
    def _demo_rows(metric: str, limit: int) -> list[dict[str, Any]]:
        today = date.today().isoformat()
        rows = [
            {
                "metric_date": today,
                "metric_family": "retail",
                "metric_name": "daily_sales_vs_plan_pct",
                "location": "South Bend flagship",
                "value": 4.8,
                "status": "ahead",
                "notes": "Demo data: sales are ahead of plan, driven by apparel and home goods.",
            },
            {
                "metric_date": today,
                "metric_family": "donations",
                "metric_name": "donation_intake_trailers_at_capacity",
                "location": "Michiana network",
                "value": 3,
                "status": "watch",
                "notes": "Demo data: three locations may need pickup routing support.",
            },
            {
                "metric_date": today,
                "metric_family": "workforce",
                "metric_name": "job_placement_followups_due",
                "location": "Mission services",
                "value": 18,
                "status": "action_needed",
                "notes": "Demo data: follow-ups due for participant placement support.",
            },
            {
                "metric_date": today,
                "metric_family": "incidents",
                "metric_name": "open_facilities_tickets",
                "location": "Elkhart store",
                "value": 2,
                "status": "watch",
                "notes": "Demo data: HVAC and donation door tickets are open.",
            },
        ]
        if metric != "summary":
            rows = [row for row in rows if row["metric_family"] == metric]
        return rows[:limit]

    @staticmethod
    def _create_engine(dsn: str):
        from sqlalchemy import create_engine

        return create_engine(dsn, pool_pre_ping=True)


def serialize_rows(payload: Any) -> str:
    """Serialize rows that may include dates, Decimals, or driver-specific values."""

    def default_serializer(value: Any) -> str | float:
        if isinstance(value, Decimal):
            return float(value)
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)

    return json.dumps(payload, indent=2, default=default_serializer)


_connector: WarehouseConnector | None = None


def get_warehouse_connector() -> WarehouseConnector:
    """Get the process-local warehouse connector."""
    global _connector
    if _connector is None:
        _connector = WarehouseConnector()
    return _connector
