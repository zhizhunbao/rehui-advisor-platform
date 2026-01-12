from src.modules.admin.router import router as admin_router

# 子模块路由
from src.modules.admin.auth import router as admin_auth_router
from src.modules.admin.config import router as config_router
from src.modules.admin.conversation import router as conversation_router
from src.modules.admin.crawler import router as crawler_router
from src.modules.admin.recommendation import router as recommendation_router
from src.modules.admin.subscription import router as subscription_router
from src.modules.admin.user import router as user_router

__all__ = [
    "admin_router",
    "admin_auth_router",
    "config_router",
    "conversation_router",
    "crawler_router",
    "recommendation_router",
    "subscription_router",
    "user_router",
]
