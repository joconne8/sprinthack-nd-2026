"""Copilot Studio handoff connector."""

from __future__ import annotations

import os
from typing import Any

import httpx


class CopilotStudioConnector:
    """Post concise handoff payloads to a configured Copilot Studio endpoint."""

    def __init__(self) -> None:
        self.webhook_url = os.getenv("COPILOT_STUDIO_WEBHOOK_URL", "")
        self.api_key = os.getenv("COPILOT_STUDIO_API_KEY", "")

    async def handoff(self, user_request: str, summary: str, priority: str = "normal") -> dict[str, Any]:
        """Send a handoff payload, or return dry-run content if not configured."""
        payload = {
            "source": "goodwill-michiana-langgraph-agent",
            "user_request": user_request,
            "summary": summary,
            "priority": priority,
        }

        if not self.webhook_url:
            return {"success": True, "mode": "dry_run", "handoff_payload": payload}

        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.webhook_url, headers=headers, json=payload)
            response.raise_for_status()
            return {"success": True, "mode": "sent", "status_code": response.status_code}


_connector: CopilotStudioConnector | None = None


def get_copilot_connector() -> CopilotStudioConnector:
    """Get the process-local Copilot Studio connector."""
    global _connector
    if _connector is None:
        _connector = CopilotStudioConnector()
    return _connector

