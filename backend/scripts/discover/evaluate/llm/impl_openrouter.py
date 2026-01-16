# OpenRouter LLM 实现 - 聚合多个免费模型
import os
from scripts.discover.evaluate.llm.base import LLMProvider, LLMResult


class OpenRouterProvider(LLMProvider):
    """OpenRouter Provider - 使用免费模型"""

    NAME = "openrouter"
    MODEL = "deepseek/deepseek-r1-0528:free"
    IS_FREE = True

    def generate(self, prompt: str) -> LLMResult:
        import httpx

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not set")

        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.MODEL,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )

        if response.status_code != 200:
            raise ValueError(f"OpenRouter error: {response.text}")

        data = response.json()
        if "error" in data:
            raise ValueError(f"OpenRouter error: {data['error']}")

        return LLMResult(
            answer=data["choices"][0]["message"]["content"],
            latency_ms=0,
            input_tokens=data.get("usage", {}).get("prompt_tokens", 0),
            output_tokens=data.get("usage", {}).get("completion_tokens", 0),
            cost_usd=0,
        )
