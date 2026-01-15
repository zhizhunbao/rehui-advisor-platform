# Hacker News 资源发现脚本 - 通过标签搜索 HN
from typing import Any, Dict, List
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.domain.tags import TAGS


class DiscoverHackerNewsScript(ScriptBase):
    """通过标签搜索 Hacker News 发现新资源"""

    NAME = "discover_hackernews"
    DESCRIPTION = "通过标签搜索 Hacker News"

    ALGOLIA_API = "https://hn.algolia.com/api/v1/search"

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return [tag["name_en"] for tag in TAGS]

    def search_stories(
        self,
        query: str,
        hits_per_page: int = 20,
    ) -> List[Dict[str, Any]]:
        """搜索 HN 故事"""
        params = {
            "query": query,
            "tags": "story",
            "hitsPerPage": hits_per_page,
        }
        try:
            resp = requests.get(self.ALGOLIA_API, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json().get("hits", [])
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
            hits = self.search_stories(tag)

            for hit in hits:
                url = hit.get("url")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                results.append({
                    "url": url,
                    "name": hit.get("title", ""),
                    "description": "",
                    "source_type": "hackernews",
                    "points": hit.get("points", 0),
                    "comments": hit.get("num_comments", 0),
                    "hn_id": hit.get("objectID", ""),
                    "tags": [tag.lower()],
                })

        return results

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 Hacker News 资源发现...")

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
    script = DiscoverHackerNewsScript(verbose=True)
    result = script.run()
    print(result)
