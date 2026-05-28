from typing import AsyncIterator
from openai import AsyncOpenAI
from backend.core.config import settings


class Engine:

    def __init__(self):
        if settings.engine == "ollama":
            self.client = AsyncOpenAI(
                base_url=settings.ollama_base_url,
                api_key="ollama",
            )
            self.model = settings.ollama_model
        elif settings.engine == "anthropic":
            raise NotImplementedError("Anthropic engine coming in phase 2")
        else:
            raise ValueError(f"Unknown engine: {settings.engine}")

    def _build_messages(self, messages: list[dict], system: str | None) -> list[dict]:
        if system:
            return [{"role": "system", "content": system}] + messages
        return messages

    async def complete(self, messages: list[dict], system: str | None = None) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(messages, system),
        )
        return response.choices[0].message.content

    async def stream_complete(
        self, messages: list[dict], system: str | None = None
    ) -> AsyncIterator[str]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(messages, system),
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
