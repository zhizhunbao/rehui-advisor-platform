# Reddit 资源发现脚本 - 通过标签搜索热门帖子
import os
import time
from typing import Any, Dict, List
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.domain.tags import TAGS
from scripts.data.initial.domain.domains import DOMAINS
from scripts.data.initial.domain.categories import CATEGORIES


class DiscoverRedditScript(ScriptBase):
    """通过标签搜索 Reddit 热门资源"""

    NAME = "discover_reddit"
    DESCRIPTION = "通过标签搜索 Reddit 热门帖子"

    REDDIT_API = "https://www.reddit.com"
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data_source", "reddit", "__init__.py")

    def __init__(self, verbose: bool = False) -> None:
        super().__init__(verbose)
        self.headers = {
            "User-Agent": "ResourceBot/1.0 (by /u/resourcebot)",
        }

    def _escape_string(self, s: str) -> str:
        """转义字符串中的特殊字符"""
        if not s:
            return ""
        return s.replace("\\", "\\\\").replace('"', "'").replace("\n", " ").replace("\r", "")

    def init_file(self) -> None:
        """初始化输出文件"""
        os.makedirs(os.path.dirname(self.OUTPUT_FILE), exist_ok=True)
        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("# Reddit 数据源 - 由 discover_reddit.py 脚本自动生成\n")
            f.write("from typing import List, Dict, Any\n\n")
            f.write("REDDIT_SOURCES: List[Dict[str, Any]] = [\n")

    def append_to_file(self, item: Dict[str, Any]) -> None:
        """追加单条记录到文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("    {\n")
            f.write(f'        "url": "{item["url"]}",\n')
            f.write(f'        "name": "{self._escape_string(item["name"])}",\n')
            f.write(f'        "description": "{self._escape_string(item["description"])}",\n')
            f.write(f'        "source_type": "{item["source_type"]}",\n')
            f.write(f'        "score": {item["score"]},\n')
            f.write(f'        "comments": {item["comments"]},\n')
            f.write(f'        "subreddit": "{item["subreddit"]}",\n')
            f.write(f'        "tags": {item["tags"]},\n')
            f.write("    },\n")

    def close_file(self) -> None:
        """关闭文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("]\n\n")
            f.write('__all__ = ["REDDIT_SOURCES"]\n')

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

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return [tag["name_en"] for tag in TAGS]

    def search_posts(
        self,
        query: str,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """搜索帖子"""
        url = f"{self.REDDIT_API}/search.json"
        params = {"q": query, "limit": limit, "sort": "relevance", "t": "month"}
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return [child["data"] for child in data["data"]["children"]]
        except requests.RequestException as e:
            self.error(f"搜索失败: {query} - {e}")
            return []

    def discover_all(self) -> int:
        """发现所有资源"""
        all_tags = [(tag["code"], tag["name_en"]) for tag in TAGS]
        seen_urls: set = set()
        count = 0

        self.init_file()

        for tag_code, tag_name in all_tags:
            tag_info = self.get_tag_info(tag_code)
            self.info(f"搜索 [{tag_info['category']}] > [{tag_info['domain']}] > {tag_name}")
            posts = self.search_posts(tag_name)

            for post in posts:
                url = post.get("url", "")
                if not url or "reddit.com" in url or url in seen_urls:
                    continue
                seen_urls.add(url)
                item = {
                    "url": url,
                    "name": post.get("title", ""),
                    "description": post.get("selftext", "")[:200],
                    "source_type": "reddit",
                    "score": post.get("score", 0),
                    "comments": post.get("num_comments", 0),
                    "subreddit": post.get("subreddit", ""),
                    "tags": [tag_name.lower()],
                }
                self.append_to_file(item)
                count += 1

            time.sleep(1)

        self.close_file()
        return count

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 Reddit 资源发现...")

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
    script = DiscoverRedditScript(verbose=True)
    result = script.run()
    print(result)
