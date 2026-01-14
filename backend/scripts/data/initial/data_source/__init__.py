# 数据源模块 - 从 discover 目录导入
from scripts.data.discover.data_sources import DATA_SOURCES
from scripts.data.discover.data_sources.github.ai import AI_GITHUB_SOURCES

__all__ = [
    "DATA_SOURCES",
    "AI_GITHUB_SOURCES",
]
