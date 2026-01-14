# GitHub 数据源 - 按 category 组织
from typing import Any, Dict, List

from scripts.data.discover.data_source.github.ai import AI_GITHUB_SOURCES
from scripts.data.discover.data_source.github.career import CAREER_GITHUB_SOURCES
from scripts.data.discover.data_source.github.education import EDUCATION_GITHUB_SOURCES
from scripts.data.discover.data_source.github.finance import FINANCE_GITHUB_SOURCES
from scripts.data.discover.data_source.github.healthcare import HEALTHCARE_GITHUB_SOURCES
from scripts.data.discover.data_source.github.housing import HOUSING_GITHUB_SOURCES
from scripts.data.discover.data_source.github.immigration import IMMIGRATION_GITHUB_SOURCES
from scripts.data.discover.data_source.github.travel import TRAVEL_GITHUB_SOURCES

GITHUB_SOURCES: List[Dict[str, Any]] = []
GITHUB_SOURCES.extend(AI_GITHUB_SOURCES)
GITHUB_SOURCES.extend(CAREER_GITHUB_SOURCES)
GITHUB_SOURCES.extend(EDUCATION_GITHUB_SOURCES)
GITHUB_SOURCES.extend(FINANCE_GITHUB_SOURCES)
GITHUB_SOURCES.extend(HEALTHCARE_GITHUB_SOURCES)
GITHUB_SOURCES.extend(HOUSING_GITHUB_SOURCES)
GITHUB_SOURCES.extend(IMMIGRATION_GITHUB_SOURCES)
GITHUB_SOURCES.extend(TRAVEL_GITHUB_SOURCES)

__all__ = ["GITHUB_SOURCES"]
