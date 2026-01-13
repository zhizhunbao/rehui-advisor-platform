"""Learning 模块主路由"""
from fastapi import APIRouter

from .courses.router import router as courses_router
from .labs.router import router as labs_router
from .assignments.router import router as assignments_router
from .resources.router import router as resources_router
from .storage.router import router as storage_router

router = APIRouter(prefix="/learning", tags=["learning"])

# 注册子路由
router.include_router(courses_router)
router.include_router(labs_router)
router.include_router(assignments_router)
router.include_router(resources_router)
router.include_router(storage_router)
