# 数据源模块 - 按 source_type 组织
from typing import Any, Dict, List

from scripts.data.discover.data_sources.github import GITHUB_SOURCES
from scripts.data.discover.data_sources.rss import RSS_SOURCES
from scripts.data.discover.data_sources.website import WEBSITE_SOURCES

DATA_SOURCES: List[Dict[str, Any]] = []
DATA_SOURCES.extend(GITHUB_SOURCES)
DATA_SOURCES.extend(RSS_SOURCES)
DATA_SOURCES.extend(WEBSITE_SOURCES)

__all__ = [
    "DATA_SOURCES",
    "GITHUB_SOURCES",
    "RSS_SOURCES",
    "WEBSITE_SOURCES",
]
