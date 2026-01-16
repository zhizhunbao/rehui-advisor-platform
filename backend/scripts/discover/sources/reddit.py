# Reddit 数据源
from typing import Any

import requests

from scripts.discover.base import DataSource, DiscoveredItem


class RedditSource(DataSource):
    """Reddit 帖子搜索"""

    NAME = "reddit"
    API_URL = "https://www.reddit.com/search.json"

    def __init__(self, verbose: bool = False, subreddits: list[str] | None = None) -> None:
        super().__init__(verbose)
        self.subreddits = subreddits or []
        self.headers = {"User-Agent": "DiscoverBot/1.0"}

    def search(self, keywords: list[str], limit: int = 10) -> list[DiscoveredItem]:
        results: dict[str, DiscoveredItem] = {}

        for keyword in keywords:
            items = self._search_posts(keyword, limit)
            for item in items:
                if item.url not in results:
                    results[item.url] = item

        return list(results.values())

    def _search_posts(self, keyword: str, limit: int) -> list[DiscoveredItem]:
        query = keyword
        if self.subreddits:
            query = f"{keyword} subreddit:{'+'.join(self.subreddits)}"

        params = {"q": query, "sort": "relevance", "limit": limit, "type": "link"}

        try:
            resp = requests.get(self.API_URL, headers=self.headers, params=params, timeout=30)
            resp.raise_for_status()
            posts = resp.json().get("data", {}).get("children", [])
        except requests.RequestException as e:
            self.log(f"请求失败: {e}")
            return []

        return [self._to_item(p["data"]) for p in posts if p.get("data")]

    def _to_item(self, post: dict[str, Any]) -> DiscoveredItem:
        return DiscoveredItem(
            url=f"https://reddit.com{post.get('permalink', '')}",
            title=post.get("title", ""),
            description=post.get("selftext", "")[:500],
            source_type="reddit",
            domain_code="",
            tags=[post.get("subreddit", "").lower()],
            metadata={"score": post.get("score", 0), "created_utc": post.get("created_utc")},
        )
