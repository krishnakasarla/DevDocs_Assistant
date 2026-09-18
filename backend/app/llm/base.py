from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate text from a fully constructed prompt."""
