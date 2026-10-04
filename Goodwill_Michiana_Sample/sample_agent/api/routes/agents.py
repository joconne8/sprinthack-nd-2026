"""Agent invocation routes."""

from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from sample_agent.agents.intelligence_agent.agent import IntelligenceAgentBuilder

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentPayload(BaseModel):
    """Request payload for agent invocation."""

    message: str
    thread_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    model: str | None = Field(default=None, description="Optional model override for demos or A/B tests.")
    context: dict | None = Field(default=None, description="Optional channel/user/application context.")


@router.post("/intelligence-agent/invoke")
async def invoke_intelligence_agent(payload: AgentPayload, request: Request):
    """Invoke the sample intelligence agent."""
    start = time.time()
    settings = request.app.state.settings

    if payload.model:
        builder = IntelligenceAgentBuilder.default_builder(
            llm_base_url=settings.litellm_proxy_api_base,
            llm_api_key=settings.litellm_proxy_api_key,
            model=payload.model,
            temperature=settings.agent_temperature,
            checkpointer=request.app.state.checkpointer,
            http_client=request.app.state.http_client,
        )
        agent = await builder.build()
    else:
        agent = request.app.state.intelligence_agent

    result = await agent.run(payload.message, thread_id=str(payload.thread_id))
    return {
        "response": result.response,
        "thread_id": result.thread_id,
        "images": result.images or [],
        "latency_ms": int((time.time() - start) * 1000),
    }

