# Member 模块 - 会员端功能

# 核心模块
from src.modules.member.advisor import router as advisor_router
from src.modules.member.auth import router as auth_router
from src.modules.member.recommendation import router as recommendation_router
from src.modules.member.search import router as search_router

# 业务领域模块
from src.modules.member.car import router as car_router
from src.modules.member.education import router as education_router
from src.modules.member.flight import router as flight_router
from src.modules.member.hotel import router as hotel_router
from src.modules.member.house import router as house_router
from src.modules.member.insurance import router as insurance_router
from src.modules.member.investment import router as investment_router
from src.modules.member.job import router as job_router
from src.modules.member.learning.router import router as learning_router

__all__ = [
    # 核心模块
    "advisor_router",
    "auth_router",
    "recommendation_router",
    "search_router",
    # 业务领域模块
    "car_router",
    "education_router",
    "flight_router",
    "hotel_router",
    "house_router",
    "insurance_router",
    "investment_router",
    "job_router",
    "learning_router",
]
