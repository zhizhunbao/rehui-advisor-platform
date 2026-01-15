# 数据源模块 - 按 source_type 组织
from typing import Any, Dict, List

from scripts.data.discover.data_source.github import GITHUB_SOURCES
from scripts.data.discover.data_source.rss import RSS_SOURCES
from scripts.data.discover.data_source.hackernews import HACKERNEWS_SOURCES
from scripts.data.discover.data_source.reddit import REDDIT_SOURCES
from scripts.data.discover.data_source.huggingface import HUGGINGFACE_SOURCES
from scripts.data.discover.data_source.stackoverflow import STACKOVERFLOW_SOURCES
from scripts.data.discover.data_source.devto import DEVTO_SOURCES
from scripts.data.discover.data_source.producthunt import PRODUCTHUNT_SOURCES
from scripts.data.discover.data_source.awesome import AWESOME_SOURCES
from scripts.data.discover.data_source.medium import MEDIUM_SOURCES

DATA_SOURCES: List[Dict[str, Any]] = []
DATA_SOURCES.extend(GITHUB_SOURCES)
DATA_SOURCES.extend(RSS_SOURCES)
DATA_SOURCES.extend(HACKERNEWS_SOURCES)
DATA_SOURCES.extend(REDDIT_SOURCES)
DATA_SOURCES.extend(HUGGINGFACE_SOURCES)
DATA_SOURCES.extend(STACKOVERFLOW_SOURCES)
DATA_SOURCES.extend(DEVTO_SOURCES)
DATA_SOURCES.extend(PRODUCTHUNT_SOURCES)
DATA_SOURCES.extend(AWESOME_SOURCES)
DATA_SOURCES.extend(MEDIUM_SOURCES)

__all__ = [
    "DATA_SOURCES",
    "GITHUB_SOURCES",
    "RSS_SOURCES",
    "HACKERNEWS_SOURCES",
    "REDDIT_SOURCES",
    "HUGGINGFACE_SOURCES",
    "STACKOVERFLOW_SOURCES",
    "DEVTO_SOURCES",
    "PRODUCTHUNT_SOURCES",
    "AWESOME_SOURCES",
    "MEDIUM_SOURCES",
]
