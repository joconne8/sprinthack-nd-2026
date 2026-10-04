"""Microsoft Graph connector for Teams-oriented demos."""

from __future__ import annotations

import os
from typing import Any

import httpx


class MicrosoftGraphConnector:
    """Small client-credentials Microsoft Graph helper."""

    GRAPH_BASE = "https://graph.microsoft.com/v1.0"

    def __init__(self) -> None:
        self.tenant_id = os.getenv("MICROSOFT_TENANT_ID", "")
        self.client_id = os.getenv("MICROSOFT_CLIENT_ID", "")
        self.client_secret = os.getenv("MICROSOFT_CLIENT_SECRET", "")
        self.team_id = os.getenv("TEAMS_TEAM_ID", "")
        self.channel_id = os.getenv("TEAMS_CHANNEL_ID", "")
        self._token: str | None = None

    def build_channel_message(self, title: str, summary: str) -> dict[str, Any]:
        """Build a Graph chatMessage payload."""
        body = f"<h2>{title}</h2><p>{summary}</p>"
        return {"body": {"contentType": "html", "content": body}}

    async def send_channel_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a Teams channel message through Graph."""
        missing = self._missing_config("tenant_id", "client_id", "client_secret", "team_id", "channel_id")
        if missing:
            return {"success": False, "mode": "dry_run", "missing_config": missing, "message_payload": payload}

        token = await self._get_token()
        url = f"{self.GRAPH_BASE}/teams/{self.team_id}/channels/{self.channel_id}/messages"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers={"Authorization": f"Bearer {token}"}, json=payload)
            response.raise_for_status()
            return {"success": True, "graph_response": response.json()}

    async def _get_token(self) -> str:
        if self._token:
            return self._token

        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            self._token = response.json()["access_token"]
            return self._token

    def _missing_config(self, *names: str) -> list[str]:
        return [name.upper() for name in names if not getattr(self, name)]


_connector: MicrosoftGraphConnector | None = None


def get_graph_connector() -> MicrosoftGraphConnector:
    """Get the process-local Microsoft Graph connector."""
    global _connector
    if _connector is None:
        _connector = MicrosoftGraphConnector()
    return _connector

