"""LangGraph builder for the sample intelligence agent."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Self

import httpx
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_litellm import ChatLiteLLM
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from sample_agent.agents.common.config import AgentConfig, AgentIdentity, LlmConfig
from sample_agent.agents.common.langgraph_runner import LangGraphAgent
from sample_agent.agents.intelligence_agent.prompt import build_system_prompt
from sample_agent.agents.intelligence_agent.state import IntelligenceAgentState
from sample_agent.agents.intelligence_agent.tools.copilot_handoff import create_copilot_handoff_tool
from sample_agent.agents.intelligence_agent.tools.mcp_tool import create_mcp_tool
from sample_agent.agents.intelligence_agent.tools.powerbi_snapshot import create_powerbi_snapshot_tool
from sample_agent.agents.intelligence_agent.tools.query_metrics import create_query_metrics_tool
from sample_agent.agents.intelligence_agent.tools.teams_message import create_teams_message_tool


class IntelligenceAgentBuilder:
    """Build the sample LangGraph agent."""

    def __init__(
        self,
        agent_config: AgentConfig,
        llm_config: LlmConfig,
        checkpointer: BaseCheckpointSaver,
        http_client: httpx.AsyncClient,
        identity: AgentIdentity | None = None,
    ) -> None:
        self.agent_config = agent_config
        self.llm_config = llm_config
        self.checkpointer = checkpointer
        self.http_client = http_client
        self.identity = identity or AgentIdentity(
            name="Goodwill Michiana Copilot Intelligence Agent",
            description="Goodwill Michiana agent with Teams, Copilot Studio, Power BI, and MCP tools",
            slug="intelligence-agent",
        )

    @classmethod
    def default_builder(
        cls,
        llm_base_url: str,
        llm_api_key: str,
        checkpointer: BaseCheckpointSaver,
        http_client: httpx.AsyncClient,
        model: str,
        temperature: float = 0.2,
    ) -> Self:
        """Create a builder with practical demo defaults."""
        return cls(
            agent_config=AgentConfig(
                max_reasoning_steps=8,
                recursion_limit=25,
                always_visible_tools={"query_metrics", "powerbi_snapshot", "draft_or_send_teams_message"},
            ),
            llm_config=LlmConfig(
                model=model,
                base_url=llm_base_url,
                api_key=llm_api_key,
                temperature=temperature,
            ),
            checkpointer=checkpointer,
            http_client=http_client,
        )

    async def build(self) -> LangGraphAgent:
        """Build and compile the LangGraph workflow."""
        llm = ChatLiteLLM(
            model=self.llm_config.model,
            api_key=self.llm_config.api_key,
            base_url=self.llm_config.base_url,
            temperature=self.llm_config.temperature,
        )

        tools = [
            create_query_metrics_tool(),
            create_powerbi_snapshot_tool(),
            create_teams_message_tool(),
            create_copilot_handoff_tool(),
            create_mcp_tool(),
        ]
        llm_with_tools = llm.bind_tools(tools)

        async def reasoner(state: IntelligenceAgentState) -> dict:
            messages = state["messages"]
            steps = state.get("reasoning_steps", 0)

            if steps >= self.agent_config.max_reasoning_steps:
                force_message = HumanMessage(
                    content="You have reached the maximum reasoning steps. Provide the final answer now."
                )
                result = await llm_with_tools.ainvoke(messages + [force_message])
                return {"messages": [force_message, result], "reasoning_steps": steps + 1}

            result = await llm_with_tools.ainvoke(messages)
            return {"messages": [result], "reasoning_steps": steps + 1}

        workflow = StateGraph(IntelligenceAgentState)
        workflow.add_node("reasoner", reasoner)
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_edge(START, "reasoner")
        workflow.add_conditional_edges("reasoner", tools_condition)
        workflow.add_edge("tools", "reasoner")

        compiled = workflow.compile(checkpointer=self.checkpointer)

        return LangGraphAgent(
            graph=compiled.with_config({"recursion_limit": self.agent_config.recursion_limit}),
            name=self.identity.name,
            description=self.identity.description,
            slug=self.identity.slug,
            initial_state_builder=self.build_initial_state,
        )

    @staticmethod
    def build_initial_state(message: str, thread_id: str | None = None) -> IntelligenceAgentState:
        """Build initial graph state."""
        thread_id = thread_id or str(uuid.uuid4())
        utc_now = datetime.now(UTC)

        return IntelligenceAgentState(
            messages=[
                SystemMessage(content=build_system_prompt()),
                HumanMessage(content=f"UTC now: {utc_now.isoformat()}\n\nUser request: {message}"),
            ],
            reasoning_steps=0,
            thread_id=thread_id,
        )
