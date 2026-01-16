# GitHub 数据源
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from scripts.discover.base import DataSource, DiscoveredItem


class GitHubSource(DataSource):
    """GitHub 仓库搜索"""

    NAME = "github"
    API_URL = "https://api.github.com/search/repositories"

    def __init__(self, verbose: bool = False, min_stars: int = 100) -> None:
        super().__init__(verbose)
        load_dotenv(Path(__file__).parents[3] / ".env", override=True)
        self.min_stars = min_stars
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
            self.log(f"GitHub token 已加载: {self.token[:20]}...")

    def search(self, keywords: list[str], limit: int = 10) -> list[DiscoveredItem]:
        results: dict[str, DiscoveredItem] = {}

        for keyword in keywords:
            query = f"{keyword} in:name,description,readme stars:>={self.min_stars}"
            items = self._search_repos(query, limit)
            for item in items:
                if item.url not in results:
                    results[item.url] = item

        return list(results.values())

    def _search_repos(self, query: str, limit: int) -> list[DiscoveredItem]:
        params = {"q": query, "sort": "stars", "order": "desc", "per_page": limit}

        try:
            resp = requests.get(self.API_URL, headers=self.headers, params=params, timeout=30)
            resp.raise_for_status()
            repos = resp.json().get("items", [])
        except requests.RequestException as e:
            self.log(f"请求失败: {e}")
            return []

        return [self._to_item(repo) for repo in repos]

    def search_code(self, query: str, limit: int = 10) -> list[DiscoveredItem]:
        """搜索包含特定内容的仓库"""
        url = "https://api.github.com/search/code"
        params = {"q": query, "per_page": limit}

        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=30)
            resp.raise_for_status()
            items = resp.json().get("items", [])
        except requests.RequestException as e:
            self.log(f"代码搜索失败: {e}")
            return []

        seen = set()
        results = []
        for item in items:
            repo = item.get("repository", {})
            url = repo.get("html_url", "")
            if url and url not in seen:
                seen.add(url)
                tags = [t.lower() for t in repo.get("topics", [])]
                results.append(DiscoveredItem(
                    url=url,
                    title=repo.get("name", ""),
                    description=repo.get("description") or "",
                    source_type="github",
                    domain_code="",
                    tags=tags,
                    metadata={"full_name": repo.get("full_name", ""), "stars": repo.get("stargazers_count", 0)},
                ))
        return results

    def _to_item(self, repo: dict[str, Any]) -> DiscoveredItem:
        return DiscoveredItem(
            url=repo["html_url"],
            title=repo["name"],
            description=repo.get("description") or "",
            source_type="github",
            domain_code="",
            tags=[t.lower() for t in repo.get("topics", [])],
            metadata={"stars": repo["stargazers_count"], "updated_at": repo["updated_at"]},
        )
