from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Literal

import httpx
from google import genai
from google.genai import types

from src.common.errors import AppError, AppErrorCode
from src.common.config import get_settings

settings = get_settings()

Language = Literal["zh", "en"]


class LLMStreamChunk:
    def __init__(self, text: str, done: bool = False) -> None:
        self.text = text
        self.done = done


class LLMMessage:
    def __init__(self, role: Literal["user", "assistant"], content: str) -> None:
        self.role = role
        self.content = content


class LLMProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    async def stream_chat(
        self, messages: list[LLMMessage], system_prompt: str
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        pass


class GeminiProvider(LLMProvider):
    def __init__(self) -> None:
        self.client: genai.Client | None = None
        self.model = "gemini-2.0-flash"

    @property
    def name(self) -> str:
        return "Gemini"

    def is_available(self) -> bool:
        return bool(settings.gemini_api_key)

    async def stream_chat(
        self, messages: list[LLMMessage], system_prompt: str
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        if not self.client:
            self.client = genai.Client(api_key=settings.gemini_api_key)

        chat_history = [
            {
                "role": "model" if m.role == "assistant" else "user",
                "parts": [{"text": m.content}],
            }
            for m in messages[:-1]
        ]
        last_message = messages[-1]

        response = await self.client.aio.models.generate_content_stream(
            model=self.model,
            contents=[*chat_history, {"role": "user", "parts": [{"text": last_message.content}]}],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.1,
                top_p=0.95,
            ),
        )

        async for chunk in response:
            yield LLMStreamChunk(text=chunk.text or "", done=False)
        yield LLMStreamChunk(text="", done=True)


class GroqProvider(LLMProvider):
    def __init__(self) -> None:
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    @property
    def name(self) -> str:
        return "Groq"

    def is_available(self) -> bool:
        return bool(settings.groq_api_key)

    async def stream_chat(
        self, messages: list[LLMMessage], system_prompt: str
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        api_messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": m.role, "content": m.content} for m in messages],
        ]

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                self.base_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.groq_api_key}",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": api_messages,
                    "stream": True,
                    "temperature": 0.1,
                },
                timeout=60.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            yield LLMStreamChunk(text="", done=True)
                            return
                        try:
                            import json

                            parsed = json.loads(data)
                            content = parsed.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield LLMStreamChunk(text=content, done=False)
                        except json.JSONDecodeError:
                            pass
        yield LLMStreamChunk(text="", done=True)


class CohereProvider(LLMProvider):
    def __init__(self) -> None:
        self.base_url = "https://api.cohere.com/v2/chat"

    @property
    def name(self) -> str:
        return "Cohere"

    def is_available(self) -> bool:
        return bool(settings.cohere_api_key)

    async def stream_chat(
        self, messages: list[LLMMessage], system_prompt: str
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        chat_history = [
            {"role": "assistant" if m.role == "assistant" else "user", "content": m.content}
            for m in messages[:-1]
        ]
        last_message = messages[-1]

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                self.base_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.cohere_api_key}",
                    "X-Client-Name": "rehui-advisor",
                },
                json={
                    "model": "command-r-plus",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *chat_history,
                        {"role": "user", "content": last_message.content},
                    ],
                    "stream": True,
                },
                timeout=60.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        import json

                        parsed = json.loads(line)
                        if parsed.get("type") == "content-delta":
                            text = parsed.get("delta", {}).get("message", {}).get("content", {}).get("text", "")
                            if text:
                                yield LLMStreamChunk(text=text, done=False)
                    except json.JSONDecodeError:
                        pass
        yield LLMStreamChunk(text="", done=True)


class OpenRouterProvider(LLMProvider):
    def __init__(self) -> None:
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    @property
    def name(self) -> str:
        return "OpenRouter"

    def is_available(self) -> bool:
        return bool(settings.openrouter_api_key)

    async def stream_chat(
        self, messages: list[LLMMessage], system_prompt: str
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        api_messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": m.role, "content": m.content} for m in messages],
        ]

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                self.base_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "HTTP-Referer": "https://rehui-advisor.local",
                    "X-Title": "Rehui Advisor",
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": api_messages,
                    "stream": True,
                },
                timeout=60.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            yield LLMStreamChunk(text="", done=True)
                            return
                        try:
                            import json

                            parsed = json.loads(data)
                            content = parsed.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield LLMStreamChunk(text=content, done=False)
                        except json.JSONDecodeError:
                            pass
        yield LLMStreamChunk(text="", done=True)


class LLMManager:
    def __init__(self) -> None:
        self.providers: list[LLMProvider] = [
            GeminiProvider(),
            GroqProvider(),
            CohereProvider(),
            OpenRouterProvider(),
        ]

    def get_available_providers(self) -> list[str]:
        return [p.name for p in self.providers if p.is_available()]

    async def stream_chat(
        self, messages: list[LLMMessage], system_prompt: str
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        available = [p for p in self.providers if p.is_available()]

        if not available:
            raise AppError(
                AppErrorCode.INTERNAL_ERROR,
                "No LLM provider available. Please configure at least one API key.",
            )

        last_error: Exception | None = None

        for provider in available:
            try:
                async for chunk in provider.stream_chat(messages, system_prompt):
                    yield chunk
                return
            except Exception as e:
                last_error = e
                continue

        raise last_error or AppError(AppErrorCode.INTERNAL_ERROR, "All LLM providers failed")
