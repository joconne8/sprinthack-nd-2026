"""Agent configuration dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LlmConfig:
    """LangChain-compatible LLM configuration."""

    model: str
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.2


@dataclass(frozen=True)
class AgentConfig:
    """Agent behavior configuration."""

    max_reasoning_steps: int = 8
    recursion_limit: int = 25
    artifact_threshold: int = 5000
    always_visible_tools: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class AgentIdentity:
    """Agent metadata used by API and discovery layers."""

    name: str
    description: str
    slug: str

