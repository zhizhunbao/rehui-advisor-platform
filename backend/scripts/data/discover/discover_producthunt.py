# Product Hunt 资源发现脚本 - 通过标签搜索产品
import os
from typing import Any, Dict, List
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.domain.tags import TAGS


class DiscoverProductHuntScript(ScriptBase):
    """通过标签搜索 Product Hunt 产品"""

    NAME = "discover_producthunt"
    DESCRIPTION = "通过标签搜索 Product Hunt 产品"

    API_URL = "https://api.producthunt.com/v2/api/graphql"

    def __init__(self, verbose: bool = False) -> None:
        super().__init__(verbose)
        self.token = os.getenv("PRODUCTHUNT_TOKEN", "")

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return [tag["name_en"] for tag in TAGS]

    def search_posts(self, query: str, first: int = 10) -> List[Dict[str, Any]]:
        """搜索产品"""
        if not self.token:
            self.warning("未配置 PRODUCTHUNT_TOKEN，跳过搜索")
            return []

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        graphql_query = """
        query($query: String!, $first: Int!) {
            posts(first: $first, order: VOTES, topic: $query) {
                edges {
                    node {
                        id
                        name
                        tagline
                        url
                        votesCount
                        website
                    }
                }
            }
        }
        """
        try:
            resp = requests.post(
                self.API_URL,
                headers=headers,
                json={"query": graphql_query, "variables": {"query": query, "first": first}},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            edges = data.get("data", {}).get("posts", {}).get("edges", [])
            return [edge["node"] for edge in edges]
        except requests.RequestException as e:
            self.error(f"搜索失败: {query} - {e}")
            return []

    def discover_all(self) -> List[Dict[str, Any]]:
        """发现所有资源"""
        tags = self.get_all_tags()
        results: List[Dict[str, Any]] = []
        seen_urls: set = set()

        for tag in tags:
            self.info(f"搜索标签: {tag}")
            posts = self.search_posts(tag)

            for post in posts:
                url = post.get("website") or post.get("url", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                results.append({
                    "url": url,
                    "name": post.get("name", ""),
                    "description": post.get("tagline", ""),
                    "source_type": "producthunt",
                    "votes": post.get("votesCount", 0),
                    "tags": [tag.lower()],
                })

        return results

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 Product Hunt 资源发现...")

        try:
            results = self.discover_all()
            self.success(f"发现 {len(results)} 个资源")
            return ScriptResult(
                success=True,
                message=f"Discovered {len(results)} resources",
                created=len(results),
            )
        except Exception as e:
            self.error(f"发现失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])


if __name__ == "__main__":
    script = DiscoverProductHuntScript(verbose=True)
    result = script.run()
    print(result)
