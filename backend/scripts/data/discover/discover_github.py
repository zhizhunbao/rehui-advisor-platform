# GitHub 资源发现脚本 - 通过标签搜索 GitHub 仓库
import os
import time
from typing import Any, Dict, List, Optional
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.domain.tags import TAGS
from scripts.data.initial.domain.domains import DOMAINS
from scripts.data.initial.domain.categories import CATEGORIES


class DiscoverGitHubScript(ScriptBase):
    """通过标签搜索 GitHub 发现新资源"""

    NAME = "discover_github"
    DESCRIPTION = "通过标签搜索 GitHub 仓库"

    GITHUB_API = "https://api.github.com"
    SEARCH_REPOS_URL = f"{GITHUB_API}/search/repositories"
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data_source", "github", "__init__.py")

    def __init__(self, verbose: bool = False) -> None:
        super().__init__(verbose)
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def _escape_string(self, s: str) -> str:
        """转义字符串中的特殊字符"""
        if not s:
            return ""
        return s.replace("\\", "\\\\").replace('"', "'").replace("\n", " ").replace("\r", "")

    def init_file(self) -> None:
        """初始化输出文件"""
        os.makedirs(os.path.dirname(self.OUTPUT_FILE), exist_ok=True)
        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("# GitHub 数据源 - 由 discover_github.py 脚本自动生成\n")
            f.write("from typing import List, Dict, Any\n\n")
            f.write("GITHUB_SOURCES: List[Dict[str, Any]] = [\n")

    def append_to_file(self, item: Dict[str, Any]) -> None:
        """追加单条记录到文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("    {\n")
            f.write(f'        "url": "{item["url"]}",\n')
            f.write(f'        "name": "{self._escape_string(item["name"])}",\n')
            f.write(f'        "description": "{self._escape_string(item["description"])}",\n')
            f.write(f'        "source_type": "{item["source_type"]}",\n')
            f.write(f'        "stars": {item["stars"]},\n')
            f.write(f'        "updated_at": "{item["updated_at"]}",\n')
            f.write(f'        "tags": {item["tags"]},\n')
            f.write("    },\n")

    def close_file(self) -> None:
        """关闭文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("]\n\n")
            f.write('__all__ = ["GITHUB_SOURCES"]\n')

    def get_tag_info(self, tag_code: str) -> Dict[str, str]:
        """获取标签的完整信息（类别、领域、标签）"""
        for tag in TAGS:
            if tag["code"] == tag_code:
                domain_code = tag["domain_code"]
                domain_info = next((d for d in DOMAINS if d["code"] == domain_code), None)
                if domain_info:
                    category_code = domain_info["category_code"]
                    category_info = next((c for c in CATEGORIES if c["code"] == category_code), None)
                    return {
                        "category": category_info["name_en"] if category_info else "Unknown",
                        "domain": domain_info["name_en"],
                        "tag": tag["name_en"],
                    }
        return {"category": "Unknown", "domain": "Unknown", "tag": "Unknown"}

    def get_tags_by_domain(self, domain_code: str) -> List[str]:
        """获取指定领域的所有标签"""
        return [
            tag["name_en"]
            for tag in TAGS
            if tag["domain_code"] == domain_code
        ]

    def get_all_domain_codes(self) -> List[str]:
        """获取所有领域代码"""
        return list(set(tag["domain_code"] for tag in TAGS))

    def search_repos(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 10,
    ) -> List[Dict[str, Any]]:
        """搜索 GitHub 仓库"""
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
        }
        try:
            resp = requests.get(
                self.SEARCH_REPOS_URL,
                headers=self.headers,
                params=params,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json().get("items", [])
        except requests.RequestException as e:
            self.error(f"搜索失败: {query} - {e}")
            return []

    def discover_by_tag(
        self,
        tag: str,
        domain_code: str,
        min_stars: int = 100,
    ) -> List[Dict[str, Any]]:
        """通过单个标签发现资源"""
        query = f"{tag} in:name,description,readme stars:>={min_stars}"
        repos = self.search_repos(query)

        results = []
        for repo in repos:
            results.append({
                "url": repo["html_url"],
                "name": repo["name"],
                "description": repo.get("description", ""),
                "source_type": "github",
                "domain_code": domain_code,
                "stars": repo["stargazers_count"],
                "updated_at": repo["updated_at"],
                "tags": [tag.lower()],
            })
        return results

    def discover_by_domain(
        self,
        domain_code: str,
        min_stars: int = 100,
    ) -> List[Dict[str, Any]]:
        """通过领域发现资源"""
        tags = [(tag["code"], tag["name_en"]) for tag in TAGS if tag["domain_code"] == domain_code]
        if not tags:
            return []

        all_results: Dict[str, Dict[str, Any]] = {}
        for tag_code, tag_name in tags:
            tag_info = self.get_tag_info(tag_code)
            self.info(f"搜索 [{tag_info['category']}] > [{tag_info['domain']}] > {tag_name}")
            results = self.discover_by_tag(tag_name, domain_code, min_stars)
            for item in results:
                url = item["url"]
                if url in all_results:
                    all_results[url]["tags"].extend(item["tags"])
                else:
                    all_results[url] = item
            time.sleep(1)

        return list(all_results.values())

    def discover_all(
        self,
        domain_codes: Optional[List[str]] = None,
        min_stars: int = 100,
    ) -> int:
        """发现所有领域的资源"""
        if domain_codes is None:
            domain_codes = self.get_all_domain_codes()

        self.init_file()
        seen_urls: set = set()
        count = 0

        for i, domain_code in enumerate(domain_codes):
            self.info(f"发现领域: {domain_code}")
            results = self.discover_by_domain(domain_code, min_stars)
            for item in results:
                if item["url"] not in seen_urls:
                    seen_urls.add(item["url"])
                    self.append_to_file(item)
                    count += 1
            self.progress(i + 1, len(domain_codes), f"发现 {len(results)} 个资源")

        self.close_file()
        return count

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 GitHub 资源发现...")

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
    script = DiscoverGitHubScript(verbose=True)
    result = script.run()
    print(result)
