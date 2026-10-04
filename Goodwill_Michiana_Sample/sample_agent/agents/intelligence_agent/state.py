"""LangGraph state for the sample intelligence agent."""

from __future__ import annotations

from langgraph.graph import MessagesState


class IntelligenceAgentState(MessagesState):
    """Graph state plus lightweight loop tracking."""

    reasoning_steps: int
    thread_id: str

