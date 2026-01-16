# 搜索技术领域发现脚本
from typing import Any

from scripts.data.domain.tags import TAGS, AI_EXTRA_TAGS
from scripts.discover.base import DomainDiscoverScript
from scripts.discover.sources.github import GitHubSource
from scripts.discover.sources.hackernews import HackerNewsSource


class DiscoverSearchTechniquesScript(DomainDiscoverScript):
    """搜索技术领域资源发现"""

    NAME = "discover_search_techniques"
    DESCRIPTION = "发现搜索和检索技术"
    DOMAIN_CODE = "search_techniques"
    MIN_QUALITY_SCORE = 60.0

    def _get_domain_tags(self) -> list[dict[str, Any]]:
        """获取当前领域的标签"""
        all_tags = TAGS + AI_EXTRA_TAGS
        return [t for t in all_tags if t.get("domain_code") == self.DOMAIN_CODE]

    @property
    def KEYWORDS(self) -> list[str]:
        """从 tags.py 自动生成搜索关键词"""
        keywords = []
        all_tags = TAGS + AI_EXTRA_TAGS
        
        for tag in all_tags:
            if tag.get("domain_code") == self.DOMAIN_CODE:
                keywords.append(tag["name_en"])
                code_as_keyword = tag["code"].replace("_", " ")
                if code_as_keyword != tag["name_en"].lower():
                    keywords.append(code_as_keyword)
        
        keywords.extend(["vector search", "similarity search", "information retrieval"])
        return keywords

    @property
    def CATEGORY_KEYWORDS(self) -> dict[str, list[str]]:
        """资源分类关键词"""
        return {
            "semantic": ["semantic search", "vector search", "similarity search", "dense retrieval"],
            "hybrid": ["hybrid search", "bm25", "sparse retrieval", "lexical search"],
            "reranking": ["reranking", "rerank", "cross encoder", "colbert"],
            "evaluation": ["retrieval evaluation", "recall", "precision", "ndcg"],
        }

    def _init_sources(self) -> None:
        self.SOURCES = [
            GitHubSource(verbose=self.verbose, min_stars=200),
            HackerNewsSource(verbose=self.verbose, min_points=30),
        ]


if __name__ == "__main__":
    script = DiscoverSearchTechniquesScript(verbose=True)
    result = script.run()
    print(result)
