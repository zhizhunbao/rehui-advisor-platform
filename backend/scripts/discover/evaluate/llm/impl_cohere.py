# Cohere LLM 实现 - 有免费额度
import os
from scripts.discover.evaluate.llm.base import LLMProvider, LLMResult


class CohereProvider(LLMProvider):
    """Cohere Provider - command-r-plus 免费试用"""

    NAME = "cohere"
    MODEL = "command-r-plus"
    IS_FREE = True

    def generate(self, prompt: str) -> LLMResult:
        import httpx

        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set")

        response = httpx.post(
            "https://api.cohere.com/v2/chat",
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
            raise ValueError(f"Cohere error: {response.text}")

        data = response.json()
        content = data.get("message", {}).get("content", [{}])[0].get("text", "")
        usage = data.get("usage", {})

        return LLMResult(
            answer=content,
            latency_ms=0,
            input_tokens=usage.get("billed_units", {}).get("input_tokens", 0),
            output_tokens=usage.get("billed_units", {}).get("output_tokens", 0),
            cost_usd=0,
        )
