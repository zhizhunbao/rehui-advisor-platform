# 数据定义模块 - 纯数据，无逻辑
from scripts.data.categories import CATEGORIES
from scripts.data.domains import DOMAINS
from scripts.data.prompts import PROMPTS
from scripts.data.llm_models import LLM_MODELS
from scripts.data.retrieval_engines import RETRIEVAL_ENGINES
from scripts.data.users import ADMIN_USERS, MEMBER_USERS
from scripts.data.agent_frameworks import AGENT_FRAMEWORKS
from scripts.data.scheduler_jobs import SCHEDULER_JOBS
from scripts.data.data_sources import DATA_SOURCES

__all__ = [
    "CATEGORIES",
    "DOMAINS",
    "PROMPTS",
    "LLM_MODELS",
    "RETRIEVAL_ENGINES",
    "ADMIN_USERS",
    "MEMBER_USERS",
    "AGENT_FRAMEWORKS",
    "SCHEDULER_JOBS",
    "DATA_SOURCES",
]
