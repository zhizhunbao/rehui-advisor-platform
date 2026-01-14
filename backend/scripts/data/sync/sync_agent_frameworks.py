# 同步脚本 - 从 GitHub 同步 Agent 框架元数据到本地文件
from pathlib import Path
from typing import Any, Dict, List

import requests

from scripts.base import SyncScript
from scripts.data.data_sources.github.ai import AGENTS_SOURCES as AGENT_FRAMEWORKS


GITHUB_API = "https://api.github.com"


class SyncAgentFrameworksScript(SyncScript):
    """从 GitHub 同步 Agent 框架元数据到本地文件"""

    NAME = "Agent 框架同步"
    DESCRIPTION = "从 GitHub 同步 Agent 框架的 stars/forks 等元数据"

    def sync(self) -> int:
        """执行同步"""
        updated_frameworks: List[Dict[str, Any]] = []

        for framework in AGENT_FRAMEWORKS:
            self.info(f"获取 {framework['name']}...")
            github_data = self._fetch_github_metadata(framework["url"])

            updated = {
                **framework,
                "stars": github_data.get("stars", 0),
                "forks": github_data.get("forks", 0),
                "language": github_data.get("language", ""),
                "github_description": github_data.get("description", ""),
            }
            updated_frameworks.append(updated)
            self.info(f"  ✓ {framework['name']} (⭐{github_data.get('stars', 0)})")

        self._save_to_file(updated_frameworks)
        return len(updated_frameworks)

    def _fetch_github_metadata(self, url: str) -> Dict[str, Any]:
        """获取 GitHub 仓库元数据"""
        try:
            parts = url.replace("https://github.com/", "").split("/")
            if len(parts) < 2:
                return {}

            owner, repo = parts[0], parts[1]
            api_url = f"{GITHUB_API}/repos/{owner}/{repo}"

            response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=10)

            if response.status_code != 200:
                self.warning(f"  无法获取 {owner}/{repo}: {response.status_code}")
                return {}

            data = response.json()
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "language": data.get("language", ""),
                "description": data.get("description", ""),
            }
        except Exception as e:
            self.warning(f"  获取元数据失败: {e}")
            return {}

    def _save_to_file(self, frameworks: List[Dict[str, Any]]) -> None:
        """保存到本地 Python 文件"""
        output_path = Path(__file__).parent / "data" / "agent_frameworks.py"

        lines = [
            "# Agent 框架数据 (自动生成，请勿手动修改)",
            "from typing import Any, Dict, List",
            "",
            "AGENT_FRAMEWORKS: List[Dict[str, Any]] = [",
        ]

        for fw in frameworks:
            lines.append("    {")
            lines.append(f'        "url": {repr(fw.get("url", ""))},')
            lines.append(f'        "name": {repr(fw.get("name", ""))},')
            lines.append(f'        "description": {repr(fw.get("description", ""))},')
            lines.append(f'        "tags": {repr(fw.get("tags", []))},')
            if fw.get("stars"):
                lines.append(f'        "stars": {fw.get("stars", 0)},')
            if fw.get("forks"):
                lines.append(f'        "forks": {fw.get("forks", 0)},')
            if fw.get("language"):
                lines.append(f'        "language": {repr(fw.get("language", ""))},')
            lines.append("    },")

        lines.append("]")
        lines.append("")

        output_path.write_text("\n".join(lines), encoding="utf-8")
        self.success(f"已保存到 {output_path}")


if __name__ == "__main__":
    script = SyncAgentFrameworksScript()
    result = script.run()
    exit(0 if result.success else 1)
