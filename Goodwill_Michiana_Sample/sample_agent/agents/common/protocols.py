"""Small protocol surface shared by agent implementations."""

from __future__ import annotations

import abc
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    """Result returned by an agent invocation."""

    response: str
    thread_id: str | None = None
    images: list[dict] | None = None


class Agent(abc.ABC):
    """Minimal async agent interface."""

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @property
    @abc.abstractmethod
    def description(self) -> str: ...

    @property
    @abc.abstractmethod
    def slug(self) -> str: ...

    @abc.abstractmethod
    async def run(self, message: str, thread_id: str | None = None) -> ExecutionResult:
        """Run the agent."""
        ...

