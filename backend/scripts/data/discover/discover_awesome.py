# Awesome Lists 资源发现脚本 - 从 GitHub Awesome 列表提取链接
import os
import re
from typing import Any, Dict, List, Optional
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.discover.urls import AWESOME_LISTS


class DiscoverAwesomeScript(ScriptBase):
    """从 GitHub Awesome 列表发现资源"""

    NAME = "discover_awesome"
    DESCRIPTION = "从 GitHub Awesome 列表提取资源链接"
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data_source", "awesome", "__init__.py")

    def __init__(self, verbose: bool = False) -> None:
        super().__init__(verbose)
        self.headers = {"Accept": "application/vnd.github.v3.raw"}

    def _escape_string(self, s: str) -> str:
        """转义字符串中的特殊字符"""
        if not s:
            return ""
        return s.replace("\\", "\\\\").replace('"', "'").replace("\n", " ").replace("\r", "")

    def init_file(self) -> None:
        """初始化输出文件"""
        os.makedirs(os.path.dirname(self.OUTPUT_FILE), exist_ok=True)
        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("# Awesome 数据源 - 由 discover_awesome.py 脚本自动生成\n")
            f.write("from typing import List, Dict, Any\n\n")
            f.write("AWESOME_SOURCES: List[Dict[str, Any]] = [\n")

    def append_to_file(self, item: Dict[str, Any]) -> None:
        """追加单条记录到文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("    {\n")
            f.write(f'        "url": "{item["url"]}",\n')
            f.write(f'        "name": "{self._escape_string(item["name"])}",\n')
            f.write(f'        "description": "{self._escape_string(item["description"])}",\n')
            f.write(f'        "source_type": "{item["source_type"]}",\n')
            f.write(f'        "source_list": "{item["source_list"]}",\n')
            f.write(f'        "tags": {item["tags"]},\n')
            f.write("    },\n")

    def close_file(self) -> None:
        """关闭文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("]\n\n")
            f.write('__all__ = ["AWESOME_SOURCES"]\n')

    def get_readme_content(self, repo_url: str) -> Optional[str]:
        """获取仓库 README 内容"""
        match = re.match(r"https://github\.com/([^/]+)/([^/]+)", repo_url)
        if not match:
            return None

        owner, repo = match.groups()
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"

        try:
            resp = requests.get(api_url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            self.error(f"获取 README 失败: {repo_url} - {e}")
            return None

    def extract_links(self, content: str) -> List[Dict[str, str]]:
        """从 Markdown 内容提取链接"""
        pattern = r"\[([^\]]+)\]\((https?://[^\)]+)\)"
        matches = re.findall(pattern, content)

        links = []
        for name, url in matches:
            if self.is_valid_resource_url(url):
                links.append({"name": name.strip(), "url": url})

        return links

    def is_valid_resource_url(self, url: str) -> bool:
        """验证是否为有效资源 URL"""
        skip_patterns = [
            "github.com/topics",
            "shields.io",
            "img.shields.io",
            "badge",
            "#",
            "twitter.com",
            "linkedin.com",
        ]
        return not any(skip in url for skip in skip_patterns)

    def discover_all(self) -> int:
        """发现所有资源"""
        seen_urls: set = set()
        count = 0

        self.init_file()

        for awesome_url in AWESOME_LISTS:
            self.info(f"解析 Awesome 列表: {awesome_url}")
            content = self.get_readme_content(awesome_url)
            if not content:
                continue

            links = self.extract_links(content)
            for link in links:
                url = link["url"]
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                item = {
                    "url": url,
                    "name": link["name"],
                    "description": "",
                    "source_type": "awesome",
                    "source_list": awesome_url,
                    "tags": [],
                }
                self.append_to_file(item)
                count += 1

        self.close_file()
        return count

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 Awesome Lists 资源发现...")

        try:
            count = self.discover_all()
            self.success(f"发现 {count} 个资源并保存到文件")
            return ScriptResult(
                success=True,
                message=f"Discovered {count} resources",
                created=count,
            )
        except Exception as e:
            self.error(f"发现失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])


if __name__ == "__main__":
    script = DiscoverAwesomeScript(verbose=True)
    result = script.run()
    print(result)
