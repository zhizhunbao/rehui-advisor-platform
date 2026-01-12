"""Scheduler 路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import CreateJobRequest, UpdateJobRequest
from .service import SchedulerService

router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/job-types")
def get_job_types():
    """获取可用的任务类型"""
    service = SchedulerService()
    return success_response(service.get_job_types())


@router.get("/jobs")
def get_jobs(
    page: int = 1,
    limit: int = 20,
    job_type: str | None = None,
    is_active: bool | None = None,
):
    """获取任务列表"""
    service = SchedulerService()
    data, total = service.find_all(page, limit, job_type, is_active)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/jobs/{id}")
def get_job(id: str):
    """获取任务详情"""
    service = SchedulerService()
    data = service.find_by_id(id)
    return success_response(data)


@router.post("/jobs")
def create_job(data: CreateJobRequest):
    """创建任务"""
    service = SchedulerService()
    result = service.create(data.model_dump())
    return success_response(result)


@router.put("/jobs/{id}")
def update_job(id: str, data: UpdateJobRequest):
    """更新任务"""
    service = SchedulerService()
    result = service.update(id, data.model_dump())
    return success_response(result)


@router.delete("/jobs/{id}")
def delete_job(id: str):
    """删除任务"""
    service = SchedulerService()
    service.delete(id)
    return success_response(None)


@router.post("/jobs/{id}/toggle")
def toggle_job(id: str):
    """启用/禁用任务"""
    service = SchedulerService()
    result = service.toggle(id)
    return success_response(result)


@router.post("/jobs/{id}/trigger")
def trigger_job(id: str):
    """手动触发任务"""
    service = SchedulerService()
    result = service.trigger(id)
    return success_response(result)


@router.get("/jobs/{id}/history")
def get_job_history(id: str, page: int = 1, limit: int = 20):
    """获取任务执行历史"""
    service = SchedulerService()
    data, total = service.get_history(id, page, limit)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/logs")
def get_scheduler_logs(page: int = 1, limit: int = 50, level: str | None = None):
    """获取调度日志"""
    service = SchedulerService()
    data, total = service.get_logs(page, limit, level)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})
