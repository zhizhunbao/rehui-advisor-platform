# 同步脚本 - 从 GitHub 同步 Prompt 模板到本地文件
import csv
import io
from pathlib import Path
from typing import Any, Dict, List

import requests

from scripts.base import SyncScript


RAW_GITHUB = "https://raw.githubusercontent.com"

CATEGORY_MAP = {
    "act as": "roleplay", "pretend": "roleplay", "simulate": "roleplay", "character": "roleplay",
    "write": "writing", "essay": "writing", "story": "writing", "poem": "writing", "article": "writing",
    "code": "coding", "programming": "coding", "developer": "coding", "software": "coding",
    "business": "business", "marketing": "business", "sales": "business", "startup": "business",
    "teach": "education", "learn": "education", "tutor": "education", "explain": "education",
    "creative": "creative", "brainstorm": "creative", "idea": "creative", "design": "creative",
    "analyze": "analysis", "research": "analysis", "data": "analysis", "review": "analysis",
    "translate": "translation", "language": "translation", "interpreter": "translation",
    "assistant": "assistant", "helper": "assistant", "advisor": "assistant",
}


class SyncPromptsScript(SyncScript):
    """从 GitHub 同步 Prompt 模板到本地文件"""

    NAME = "Prompt 同步"
    DESCRIPTION = "从 GitHub 开源仓库同步 Prompt 模板到本地数据文件"

    def sync(self) -> int:
        """执行同步"""
        all_prompts: List[Dict[str, Any]] = []

        prompts1 = self._fetch_awesome_chatgpt_prompts()
        all_prompts.extend(prompts1)

        seen = set()
        unique_prompts = []
        for p in all_prompts:
            key = p["name"].lower()
            if key not in seen:
                seen.add(key)
                unique_prompts.append(p)

        self._save_to_file(unique_prompts)
        return len(unique_prompts)

    def _categorize_prompt(self, title: str, content: str) -> str:
        """根据标题和内容自动分类"""
        text = (title + " " + content).lower()
        for keyword, category in CATEGORY_MAP.items():
            if keyword in text:
                return category
        return "general"

    def _fetch_awesome_chatgpt_prompts(self) -> List[Dict[str, Any]]:
        """获取 f/awesome-chatgpt-prompts"""
        self.info("获取 f/awesome-chatgpt-prompts...")
        url = f"{RAW_GITHUB}/f/awesome-chatgpt-prompts/main/prompts.csv"
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            self.warning(f"无法访问: {response.status_code}")
            return []

        prompts = []
        reader = csv.DictReader(io.StringIO(response.text))

        for row in reader:
            title = row.get("act", "").strip()
            content = row.get("prompt", "").strip()
            if not title or not content:
                continue

            prompts.append({
                "name": title,
                "description": f"Act as {title}",
                "content": content,
                "category": self._categorize_prompt(title, content),
                "source": "awesome-chatgpt-prompts",
                "repo": "f/awesome-chatgpt-prompts",
            })

        self.info(f"  共 {len(prompts)} 个 prompts")
        return prompts

    def _save_to_file(self, prompts: List[Dict[str, Any]]) -> None:
        """保存到本地 Python 文件"""
        output_path = Path(__file__).parent / "data" / "community_prompts.py"

        lines = [
            "# 社区 Prompt 模板数据 (自动生成，请勿手动修改)",
            "from typing import Any, Dict, List",
            "",
            "COMMUNITY_PROMPTS: List[Dict[str, Any]] = [",
        ]

        for prompt in prompts:
            lines.append("    {")
            lines.append(f'        "name": {repr(prompt.get("name", ""))},')
            lines.append(f'        "description": {repr(prompt.get("description", ""))},')
            lines.append(f'        "category": {repr(prompt.get("category", "general"))},')
            lines.append(f'        "source": {repr(prompt.get("source", ""))},')
            lines.append(f'        "repo": {repr(prompt.get("repo", ""))},')
            content = prompt.get("content", "")
            lines.append(f'        "content": {repr(content)},')
            lines.append("    },")

        lines.append("]")
        lines.append("")

        output_path.write_text("\n".join(lines), encoding="utf-8")
        self.success(f"已保存到 {output_path}")


if __name__ == "__main__":
    script = SyncPromptsScript()
    result = script.run()
    exit(0 if result.success else 1)
