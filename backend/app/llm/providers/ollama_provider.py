from typing import Any

import httpx

from app.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        model: str = "llama3.1",
        base_url: str = "http://localhost:11434",
        timeout: float = 60.0,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        payload = {
            "model": kwargs.pop("model", self.model),
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": kwargs.pop("temperature", 0.1), **kwargs},
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json()["response"].strip()
