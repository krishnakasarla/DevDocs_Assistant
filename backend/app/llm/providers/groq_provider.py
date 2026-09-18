from typing import Any

import httpx

from app.llm.base import LLMProvider


class GroqProvider(LLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "https://api.groq.com/openai/v1",
        timeout: float = 60.0,
    ) -> None:
        if not api_key:
            raise ValueError("GROQ_API_KEY is required when LLM_PROVIDER=groq")
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        payload = {
            "model": kwargs.pop("model", self.model),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.pop("temperature", 0.1),
            **kwargs,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
