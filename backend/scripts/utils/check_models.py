# 检查脚本 - 检查 OpenRouter 模型
import requests

from scripts.base import CheckScript


class CheckModelsScript(CheckScript):
    """检查 OpenRouter 模型"""

    NAME = "模型检查"
    DESCRIPTION = "检查 OpenRouter 最新模型"

    def check(self) -> bool:
        """执行检查"""
        response = requests.get("https://openrouter.ai/api/v1/models", timeout=30)
        data = response.json()
        models = data.get("data", [])

        self.info(f"Total models from OpenRouter: {len(models)}")

        self.info("\n--- Searching for GPT-5, Claude Opus 4 ---")
        for m in models:
            name = m.get("id", "").lower()
            if "gpt-5" in name or "opus-4" in name or "opus4" in name:
                self.info(m.get("id"))

        self.info("\n--- Latest OpenAI models ---")
        for m in models:
            if m.get("id", "").startswith("openai/"):
                self.info(f"  {m.get('id')}")

        self.info("\n--- Latest Anthropic models ---")
        for m in models:
            if m.get("id", "").startswith("anthropic/"):
                self.info(f"  {m.get('id')}")

        return len(models) > 0


if __name__ == "__main__":
    script = CheckModelsScript()
    result = script.run()
    exit(0 if result.success else 1)
