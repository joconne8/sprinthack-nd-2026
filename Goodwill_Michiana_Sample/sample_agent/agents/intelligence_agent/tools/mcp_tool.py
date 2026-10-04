"""Tool for generic MCP stdio calls."""

from __future__ import annotations

import json
import logging

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from sample_agent.connectors.mcp_stdio import get_mcp_connector

logger = logging.getLogger(__name__)


class MCPToolInput(BaseModel):
    """Input schema for a generic MCP tool call."""

    tool_name: str = Field(description="The MCP tool name to call.")
    arguments_json: str = Field(default="{}", description="JSON object string containing tool arguments.")


def create_mcp_tool() -> StructuredTool:
    """Create a generic MCP call tool."""

    async def call_mcp_tool(tool_name: str, arguments_json: str = "{}") -> str:
        """Call a configured MCP stdio server tool."""
        try:
            arguments = json.loads(arguments_json or "{}")
            if not isinstance(arguments, dict):
                return json.dumps({"success": False, "error": "arguments_json must decode to an object"})

            result = await get_mcp_connector().call_tool(tool_name=tool_name, arguments=arguments)
            return json.dumps(result, default=str)
        except json.JSONDecodeError as exc:
            return json.dumps({"success": False, "error": f"Invalid JSON arguments: {exc}"})
        except Exception as exc:
            logger.exception("MCP tool call failed")
            return json.dumps({"success": False, "error": str(exc)})

    return StructuredTool.from_function(
        func=call_mcp_tool,
        coroutine=call_mcp_tool,
        name="call_mcp_tool",
        description=(
            "Call a tool exposed by the configured MCP stdio server. Use only when the user asks for a "
            "capability owned by that MCP server or a previous tool result says the server is configured."
        ),
        args_schema=MCPToolInput,
    )

