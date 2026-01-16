# Groq LLM 实现 - 免费，速度快
import os
from scripts.discover.evaluate.llm.base import LLMProvider, LLMResult


class GroqProvider(LLMProvider):
    """Groq LLM Provider"""

    NAME = "groq"
    MODEL = "llama-3.1-8b-instant"
    IS_FREE = True

    def generate(self, prompt: str) -> LLMResult:
        from groq import Groq

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=self.MODEL,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        return LLMResult(
            answer=response.choices[0].message.content,
            latency_ms=0,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            cost_usd=0,
        )
