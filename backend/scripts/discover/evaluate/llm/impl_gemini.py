# Google Gemini LLM 实现 - 有免费额度
import os
from scripts.discover.evaluate.llm.base import LLMProvider, LLMResult


class GeminiProvider(LLMProvider):
    """Google Gemini Provider - 使用新版 SDK"""

    NAME = "gemini"
    MODEL = "gemini-2.0-flash"
    IS_FREE = True

    def generate(self, prompt: str) -> LLMResult:
        from google import genai

        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model=self.MODEL,
            contents=prompt,
        )

        return LLMResult(
            answer=response.text,
            latency_ms=0,
            input_tokens=response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
            output_tokens=response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
            cost_usd=0,
        )
