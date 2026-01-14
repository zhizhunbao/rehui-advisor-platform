# 同步脚本 - 从 OpenRouter 同步 LLM 模型数据到本地文件
from pathlib import Path
from typing import Any, Dict, List

import requests

from scripts.base import SyncScript


OPENROUTER_API = "https://openrouter.ai/api/v1/models"


class SyncModelsScript(SyncScript):
    """从 OpenRouter 同步 LLM 模型到本地文件"""

    NAME = "模型同步"
    DESCRIPTION = "从 OpenRouter API 同步 LLM 模型数据到本地数据文件"

    def sync(self) -> int:
        """执行同步"""
        models = self._fetch_openrouter_models()
        if not models:
            self.warning("未获取到模型数据")
            return 0

        self._save_to_file(models)
        return len(models)

    def _fetch_openrouter_models(self) -> List[Dict[str, Any]]:
        """从 OpenRouter 获取模型列表"""
        self.info("获取 OpenRouter 模型列表...")

        try:
            response = requests.get(OPENROUTER_API, timeout=30)
            if response.status_code != 200:
                self.warning(f"无法访问 OpenRouter: {response.status_code}")
                return []

            data = response.json()
            raw_models = data.get("data", [])
            self.info(f"  获取到 {len(raw_models)} 个模型")

            models = []
            for m in raw_models:
                model_id = m.get("id", "")
                provider = model_id.split("/")[0] if "/" in model_id else "unknown"

                models.append({
                    "name": model_id,
                    "display_name": m.get("name", model_id),
                    "provider": provider,
                    "context_length": m.get("context_length", 0),
                    "pricing": {
                        "prompt": m.get("pricing", {}).get("prompt", "0"),
                        "completion": m.get("pricing", {}).get("completion", "0"),
                    },
                    "description": m.get("description", ""),
                })

            return models
        except Exception as e:
            self.error(f"获取模型失败: {e}")
            return []

    def _save_to_file(self, models: List[Dict[str, Any]]) -> None:
        """保存到本地 Python 文件"""
        output_path = Path(__file__).parent / "data" / "openrouter_models.py"

        lines = [
            "# OpenRouter 模型数据 (自动生成，请勿手动修改)",
            "from typing import Any, Dict, List",
            "",
            "OPENROUTER_MODELS: List[Dict[str, Any]] = [",
        ]

        for model in models:
            lines.append("    {")
            lines.append(f'        "name": {repr(model.get("name", ""))},')
            lines.append(f'        "display_name": {repr(model.get("display_name", ""))},')
            lines.append(f'        "provider": {repr(model.get("provider", ""))},')
            lines.append(f'        "context_length": {model.get("context_length", 0)},')
            lines.append(f'        "pricing": {repr(model.get("pricing", {}))},')
            lines.append(f'        "description": {repr(model.get("description", ""))},')
            lines.append("    },")

        lines.append("]")
        lines.append("")

        output_path.write_text("\n".join(lines), encoding="utf-8")
        self.success(f"已保存到 {output_path}")


if __name__ == "__main__":
    script = SyncModelsScript()
    result = script.run()
    exit(0 if result.success else 1)
