# StackOverflow 资源发现脚本 - 通过标签搜索热门问题
import time
from typing import Any, Dict, List
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.domain.tags import TAGS


class DiscoverStackOverflowScript(ScriptBase):
    """通过标签搜索 StackOverflow 热门问题"""

    NAME = "discover_stackoverflow"
    DESCRIPTION = "通过标签搜索 StackOverflow 热门问题"

    API_URL = "https://api.stackexchange.com/2.3"

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return [tag["name_en"].lower().replace(" ", "-") for tag in TAGS]

    def search_questions(
        self,
        tag: str,
        page_size: int = 10,
    ) -> List[Dict[str, Any]]:
        """搜索问题"""
        url = f"{self.API_URL}/questions"
        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": tag,
            "site": "stackoverflow",
            "pagesize": page_size,
            "filter": "withbody",
        }
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json().get("items", [])
        except requests.RequestException as e:
            self.error(f"搜索失败: {tag} - {e}")
            return []

    def discover_all(self) -> List[Dict[str, Any]]:
        """发现所有资源"""
        tags = self.get_all_tags()
        results: List[Dict[str, Any]] = []
        seen_urls: set = set()

        for tag in tags:
            self.info(f"搜索标签: {tag}")
            questions = self.search_questions(tag)

            for q in questions:
                url = q.get("link", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                results.append({
                    "url": url,
                    "name": q.get("title", ""),
                    "description": "",
                    "source_type": "stackoverflow",
                    "score": q.get("score", 0),
                    "answer_count": q.get("answer_count", 0),
                    "tags": q.get("tags", []),
                })

            time.sleep(1)

        return results

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 StackOverflow 资源发现...")

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
    script = DiscoverStackOverflowScript(verbose=True)
    result = script.run()
    print(result)
