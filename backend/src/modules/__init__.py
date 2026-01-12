"""模块统一导出 - 外部只需从这里导入"""

# ========== Admin 模块 - 管理端功能 ==========
from src.modules.admin import (
    admin_router,
    admin_auth_router,
    crawler_router,
    user_router,
    subscription_router,
    recommendation_router as admin_recommendation_router,
    conversation_router,
    config_router,
)
from src.modules.admin.data_source import data_source_router
from src.modules.admin.llm import llm_router
from src.modules.admin.log import log_router
from src.modules.admin.prompt import prompt_router
from src.modules.admin.retrieval import retrieval_router
from src.modules.admin.scheduler import scheduler_router
from src.modules.admin.skill import skill_router

# ========== Member 模块 - 会员端功能 ==========
from src.modules.member.advisor import advisor_router
from src.modules.member.auth import auth_router
from src.modules.member.recommendation import recommendation_router
from src.modules.member.search import search_router
from src.modules.member.car import router as car_router
from src.modules.member.education import router as education_router
from src.modules.member.flight import router as flight_router
from src.modules.member.hotel import router as hotel_router
from src.modules.member.house import router as house_router
from src.modules.member.insurance import router as insurance_router
from src.modules.member.investment import router as investment_router
from src.modules.member.job import router as job_router

# ========== Admin 模块 - 管理端功能 ==========
from src.modules.admin.domain import router as domain_router

__all__ = [
    # Admin
    "admin_router",
    "admin_auth_router",
    "crawler_router",
    "user_router",
    "subscription_router",
    "admin_recommendation_router",
    "conversation_router",
    "config_router",
    "data_source_router",
    "llm_router",
    "log_router",
    "prompt_router",
    "retrieval_router",
    "scheduler_router",
    "skill_router",
    # Member
    "advisor_router",
    "auth_router",
    "recommendation_router",
    "search_router",
    # Shared
    "car_router",
    "domain_router",
    "education_router",
    "flight_router",
    "hotel_router",
    "house_router",
    "insurance_router",
    "investment_router",
    "job_router",
]
