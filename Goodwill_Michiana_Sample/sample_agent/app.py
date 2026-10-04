"""FastAPI application factory."""

from __future__ import annotations

import httpx
from fastapi import FastAPI
from langgraph.checkpoint.memory import MemorySaver

from sample_agent.agents.intelligence_agent.agent import IntelligenceAgentBuilder
from sample_agent.api.routes.agents import router as agents_router
from sample_agent.api.routes.base import router as base_router
from sample_agent.settings import Settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""
    app = FastAPI(title="Sample Intelligence Agent", version="0.1.0")
    settings = Settings()

    app.state.settings = settings
    app.state.http_client = httpx.AsyncClient(timeout=60.0)
    app.state.checkpointer = MemorySaver()

    app.include_router(base_router)
    app.include_router(agents_router)

    @app.on_event("startup")
    async def startup() -> None:
        builder = IntelligenceAgentBuilder.default_builder(
            llm_base_url=settings.litellm_proxy_api_base,
            llm_api_key=settings.litellm_proxy_api_key,
            model=settings.agent_model,
            temperature=settings.agent_temperature,
            checkpointer=app.state.checkpointer,
            http_client=app.state.http_client,
        )
        app.state.intelligence_agent = await builder.build()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await app.state.http_client.aclose()

    return app

