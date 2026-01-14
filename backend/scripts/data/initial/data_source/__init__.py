# 数据源模块 - 从 discover 目录导入
from scripts.data.discover.data_source import DATA_SOURCES
from scripts.data.discover.data_source.github.ai import AI_GITHUB_SOURCES

__all__ = [
    "DATA_SOURCES",
    "AI_GITHUB_SOURCES",
]
