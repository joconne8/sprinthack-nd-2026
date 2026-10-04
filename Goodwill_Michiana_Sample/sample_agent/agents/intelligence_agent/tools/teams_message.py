"""Tool for drafting or sending Microsoft Teams updates."""

from __future__ import annotations

import json
import logging

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from sample_agent.connectors.microsoft_graph import get_graph_connector

logger = logging.getLogger(__name__)


class TeamsMessageInput(BaseModel):
    """Input schema for Teams message drafts."""

    title: str = Field(description="Short update title.")
    summary: str = Field(description="Message body for managers or stakeholders.")
    send: bool = Field(default=False, description="Only true when the user explicitly asks to send.")


def create_teams_message_tool() -> StructuredTool:
    """Create a Teams update tool."""

    async def draft_or_send_teams_message(title: str, summary: str, send: bool = False) -> str:
        """Draft or send a Teams channel update through Microsoft Graph."""
        try:
            connector = get_graph_connector()
            payload = connector.build_channel_message(title=title, summary=summary)
            if not send:
                return json.dumps({"success": True, "mode": "draft", "message_payload": payload})

            result = await connector.send_channel_message(payload)
            return json.dumps(result, default=str)
        except Exception as exc:
            logger.exception("Teams message tool failed")
            return json.dumps({"success": False, "error": str(exc)})

    return StructuredTool.from_function(
        func=draft_or_send_teams_message,
        coroutine=draft_or_send_teams_message,
        name="draft_or_send_teams_message",
        description=(
            "Draft a Microsoft Teams update for Goodwill managers or send it when explicitly requested. "
            "Default to draft mode unless the user clearly says to send/post."
        ),
        args_schema=TeamsMessageInput,
    )

