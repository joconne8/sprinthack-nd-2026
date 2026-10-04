"""Small MCP stdio client for demo connectors."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any


class MCPStdioConnector:
    """Call a configured MCP stdio server with initialize and tools/call messages."""

    def __init__(
        self,
        command: str | None = None,
        args: list[str] | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> None:
        self.command = command if command is not None else os.getenv("MCP_SERVER_COMMAND", "")
        self.args = args if args is not None else self._json_env_list("MCP_SERVER_ARGS")
        self.extra_env = extra_env if extra_env is not None else self._json_env_dict("MCP_SERVER_ENV")

    async def call_tool(self, tool_name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        """Call one MCP tool by name."""
        if not self.command:
            return {
                "success": False,
                "error": "MCP_SERVER_COMMAND is not configured.",
                "hint": "Set MCP_SERVER_COMMAND and MCP_SERVER_ARGS in .env.",
            }

        process = await asyncio.create_subprocess_exec(
            self.command,
            *self.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, **self.extra_env},
        )

        messages = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "sample-intelligence-agent", "version": "0.1.0"},
                },
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": arguments or {}},
            },
        ]

        stdin_payload = "\n".join(json.dumps(message) for message in messages) + "\n"
        stdout_bytes, stderr_bytes = await asyncio.wait_for(process.communicate(stdin_payload.encode()), timeout=60)
        stdout_text = stdout_bytes.decode(errors="replace")
        stderr_text = stderr_bytes.decode(errors="replace")

        for line in stdout_text.splitlines():
            try:
                response = json.loads(line)
            except json.JSONDecodeError:
                continue
            if response.get("id") == 2:
                if "error" in response:
                    return {"success": False, "error": response["error"], "stderr": stderr_text[:1000]}
                return {"success": True, "result": response.get("result"), "stderr": stderr_text[:1000]}

        return {"success": False, "error": "No MCP tools/call response found.", "stderr": stderr_text[:1000]}

    @staticmethod
    def _json_env_list(name: str) -> list[str]:
        try:
            value = json.loads(os.getenv(name, "[]"))
            return value if isinstance(value, list) else []
        except json.JSONDecodeError:
            return []

    @staticmethod
    def _json_env_dict(name: str) -> dict[str, str]:
        try:
            value = json.loads(os.getenv(name, "{}"))
            return value if isinstance(value, dict) else {}
        except json.JSONDecodeError:
            return {}


_connector: MCPStdioConnector | None = None


def get_mcp_connector() -> MCPStdioConnector:
    """Get the process-local MCP connector."""
    global _connector
    if _connector is None:
        _connector = MCPStdioConnector()
    return _connector

