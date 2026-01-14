# 数据源模块 - 按领域分类组织
from typing import Any, Dict, List

from scripts.data.data_sources.ai_tools import AI_TOOLS_SOURCES
from scripts.data.data_sources.career import CAREER_SOURCES
from scripts.data.data_sources.education import EDUCATION_SOURCES
from scripts.data.data_sources.finance import FINANCE_SOURCES
from scripts.data.data_sources.housing import HOUSING_SOURCES
from scripts.data.data_sources.immigration import IMMIGRATION_SOURCES
from scripts.data.data_sources.travel import TRAVEL_SOURCES
from scripts.data.data_sources.healthcare import HEALTHCARE_SOURCES
from scripts.data.data_sources.agent_frameworks import AGENT_FRAMEWORKS_SOURCES

DATA_SOURCES: List[Dict[str, Any]] = []
DATA_SOURCES.extend(AI_TOOLS_SOURCES)
DATA_SOURCES.extend(CAREER_SOURCES)
DATA_SOURCES.extend(EDUCATION_SOURCES)
DATA_SOURCES.extend(FINANCE_SOURCES)
DATA_SOURCES.extend(HOUSING_SOURCES)
DATA_SOURCES.extend(IMMIGRATION_SOURCES)
DATA_SOURCES.extend(TRAVEL_SOURCES)
DATA_SOURCES.extend(HEALTHCARE_SOURCES)
DATA_SOURCES.extend(AGENT_FRAMEWORKS_SOURCES)

__all__ = [
    "DATA_SOURCES",
    "AI_TOOLS_SOURCES",
    "CAREER_SOURCES",
    "EDUCATION_SOURCES",
    "FINANCE_SOURCES",
    "HOUSING_SOURCES",
    "IMMIGRATION_SOURCES",
    "TRAVEL_SOURCES",
    "HEALTHCARE_SOURCES",
    "AGENT_FRAMEWORKS_SOURCES",
]
