# SambaNova LLM 实现 - 免费，快速推理
import os
from scripts.discover.evaluate.llm.base import LLMProvider, LLMResult


class SambaNovaProvider(LLMProvider):
    """SambaNova Provider - 免费 API"""

    NAME = "sambanova"
    MODEL = "Meta-Llama-3.3-70B-Instruct"
    IS_FREE = True

    def generate(self, prompt: str) -> LLMResult:
        import httpx

        api_key = os.getenv("SAMBANOVA_API_KEY")
        if not api_key:
            raise ValueError("SAMBANOVA_API_KEY not set")

        response = httpx.post(
            "https://api.sambanova.ai/v1/chat/completions",
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
            raise ValueError(f"SambaNova error: {response.text}")

        data = response.json()
        usage = data.get("usage", {})

        return LLMResult(
            answer=data["choices"][0]["message"]["content"],
            latency_ms=0,
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            cost_usd=0,
        )
