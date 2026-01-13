# Learning 模块 - AI 课程学习管理

from src.modules.member.learning.courses import router as courses_router
from src.modules.member.learning.labs import router as labs_router
from src.modules.member.learning.assignments import router as assignments_router
from src.modules.member.learning.resources import router as resources_router
from src.modules.member.learning.storage import router as storage_router

__all__ = [
    "courses_router",
    "labs_router",
    "assignments_router",
    "resources_router",
    "storage_router",
]
