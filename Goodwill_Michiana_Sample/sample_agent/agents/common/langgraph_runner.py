"""Wrapper that adapts a compiled LangGraph graph to the Agent protocol."""

from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING, Any, Callable

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage
from langgraph.graph.state import CompiledStateGraph

from sample_agent.agents.common.protocols import Agent, ExecutionResult
from sample_agent.connectors.powerbi_connector import get_powerbi_connector

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class LangGraphAgent(Agent):
    """Wrap a compiled LangGraph StateGraph as an application agent."""

    def __init__(
        self,
        graph: CompiledStateGraph,
        name: str,
        description: str,
        slug: str,
        initial_state_builder: Callable[..., dict[str, Any]],
    ) -> None:
        self._graph = graph
        self._name = name
        self._description = description
        self._slug = slug
        self._initial_state_builder = initial_state_builder

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def slug(self) -> str:
        return self._slug

    async def run(
        self,
        message: str,
        thread_id: str | None = None,
        callbacks: Sequence[BaseCallbackHandler] | None = None,
    ) -> ExecutionResult:
        """Execute the graph and collect side-channel screenshot artifacts."""
        thread_id = thread_id or str(uuid.uuid4())
        initial_state = self._initial_state_builder(message=message, thread_id=thread_id)

        config: dict[str, Any] = {"configurable": {"thread_id": thread_id}}
        if callbacks:
            config["callbacks"] = list(callbacks)

        try:
            result = await self._graph.ainvoke(initial_state, config=config)
            response = self._extract_response(result)
            images = get_powerbi_connector().pop_images() or None
            return ExecutionResult(response=response, thread_id=thread_id, images=images)
        except Exception:
            logger.exception("Agent execution failed for thread %s", thread_id)
            return ExecutionResult(
                response="I encountered an error while processing the request.",
                thread_id=thread_id,
                images=None,
            )

    @staticmethod
    def _extract_response(result: dict[str, Any]) -> str:
        """Extract the last AI text response from graph state."""
        for message in reversed(result.get("messages", [])):
            if isinstance(message, AIMessage) and message.content:
                if isinstance(message.content, str):
                    return message.content
                if isinstance(message.content, list):
                    parts = [part["text"] for part in message.content if isinstance(part, dict) and "text" in part]
                    if parts:
                        return "\n".join(parts)
        return "I was unable to generate a response. Please rephrase the request."
