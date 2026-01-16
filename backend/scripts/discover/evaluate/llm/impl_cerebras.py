# Cerebras LLM 实现 - 免费，超快推理
import os
from scripts.discover.evaluate.llm.base import LLMProvider, LLMResult


class CerebrasProvider(LLMProvider):
    """Cerebras Provider - 免费，极速推理"""

    NAME = "cerebras"
    MODEL = "llama-3.3-70b"
    IS_FREE = True

    def generate(self, prompt: str) -> LLMResult:
        import httpx

        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            raise ValueError("CEREBRAS_API_KEY not set")

        response = httpx.post(
            "https://api.cerebras.ai/v1/chat/completions",
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
            raise ValueError(f"Cerebras error: {response.text}")

        data = response.json()
        usage = data.get("usage", {})

        return LLMResult(
            answer=data["choices"][0]["message"]["content"],
            latency_ms=0,
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            cost_usd=0,
        )
