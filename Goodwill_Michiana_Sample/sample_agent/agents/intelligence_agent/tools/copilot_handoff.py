"""Tool for handing summaries to Copilot Studio."""

from __future__ import annotations

import json
import logging

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from sample_agent.connectors.copilot_studio import get_copilot_connector

logger = logging.getLogger(__name__)


class CopilotHandoffInput(BaseModel):
    """Input schema for Copilot Studio handoffs."""

    user_request: str = Field(description="Original user request or follow-up objective.")
    summary: str = Field(description="Concise context to pass into Copilot Studio.")
    priority: str = Field(default="normal", description="Priority label such as low, normal, high, or urgent.")


def create_copilot_handoff_tool() -> StructuredTool:
    """Create a Copilot Studio handoff tool."""

    async def copilot_handoff(user_request: str, summary: str, priority: str = "normal") -> str:
        """Send or prepare a Copilot Studio handoff."""
        try:
            connector = get_copilot_connector()
            result = await connector.handoff(user_request=user_request, summary=summary, priority=priority)
            return json.dumps(result, default=str)
        except Exception as exc:
            logger.exception("Copilot handoff failed")
            return json.dumps({"success": False, "error": str(exc)})

    return StructuredTool.from_function(
        func=copilot_handoff,
        coroutine=copilot_handoff,
        name="copilot_handoff",
        description=(
            "Pass a summarized Goodwill operations issue or next step into Copilot Studio. "
            "If no webhook is configured, returns a dry-run payload suitable for demos."
        ),
        args_schema=CopilotHandoffInput,
    )

