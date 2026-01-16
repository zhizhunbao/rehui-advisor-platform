# Hacker News 数据源
from typing import Any

import requests

from scripts.discover.base import DataSource, DiscoveredItem


class HackerNewsSource(DataSource):
    """Hacker News 搜索（通过 Algolia API）"""

    NAME = "hackernews"
    API_URL = "https://hn.algolia.com/api/v1/search"

    def __init__(self, verbose: bool = False, min_points: int = 50) -> None:
        super().__init__(verbose)
        self.min_points = min_points

    def search(self, keywords: list[str], limit: int = 10) -> list[DiscoveredItem]:
        results: dict[str, DiscoveredItem] = {}

        for keyword in keywords:
            items = self._search_stories(keyword, limit)
            for item in items:
                if item.url not in results:
                    results[item.url] = item

        return list(results.values())

    def _search_stories(self, keyword: str, limit: int) -> list[DiscoveredItem]:
        params = {
            "query": keyword,
            "tags": "story",
            "numericFilters": f"points>={self.min_points}",
            "hitsPerPage": limit,
        }

        try:
            resp = requests.get(self.API_URL, params=params, timeout=30)
            resp.raise_for_status()
            hits = resp.json().get("hits", [])
        except requests.RequestException as e:
            self.log(f"请求失败: {e}")
            return []

        return [self._to_item(hit) for hit in hits if hit.get("url")]

    def _to_item(self, hit: dict[str, Any]) -> DiscoveredItem:
        tags = self._extract_tags(hit.get("title", ""), hit.get("story_text", ""))
        return DiscoveredItem(
            url=hit.get("url", ""),
            title=hit.get("title", ""),
            description=hit.get("story_text") or "",
            source_type="hackernews",
            domain_code="",
            tags=tags,
            metadata={"points": hit.get("points", 0), "created_at": hit.get("created_at")},
        )

    def _extract_tags(self, title: str, description: str) -> list[str]:
        """从标题和描述中提取标签"""
        text = f"{title} {description}".lower()
        tags = []
        
        tag_keywords = {
            "claude": ["claude"],
            "skills": ["skill", "skills"],
            "mcp": ["mcp", "model context protocol"],
            "agent": ["agent", "agents"],
            "prompt": ["prompt", "prompts"],
            "llm": ["llm", "language model"],
            "ai": ["ai", "artificial intelligence"],
            "openai": ["openai", "gpt"],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)
        
        return tags if tags else []
