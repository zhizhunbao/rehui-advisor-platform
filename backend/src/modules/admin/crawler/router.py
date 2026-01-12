"""抓取源管理路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import CreateCrawlSourceRequest, UpdateCrawlSourceRequest
from .service import CrawlerService

router = APIRouter(
    prefix="/admin/crawlers",
    tags=["admin-crawlers"],
    dependencies=[Depends(get_current_admin)],
)


# ========== Source Routes ==========
@router.get("/sources")
def get_sources(
    page: int = 1,
    limit: int = 20,
    domain_id: str | None = None,
    is_active: bool | None = None,
):
    service = CrawlerService()
    sources, total = service.find_all_sources(page, limit, domain_id, is_active)
    return success_response(sources, meta={"total": total, "page": page, "limit": limit})


@router.get("/sources/{id}")
def get_source(id: str):
    service = CrawlerService()
    source = service.find_source_by_id(id)
    return success_response(source)


@router.post("/sources")
def create_source(data: CreateCrawlSourceRequest):
    service = CrawlerService()
    source = service.create_source(data.model_dump(exclude_unset=True))
    return success_response(source)


@router.put("/sources/{id}")
def update_source(id: str, data: UpdateCrawlSourceRequest):
    service = CrawlerService()
    source = service.update_source(id, data.model_dump(exclude_unset=True))
    return success_response(source)


@router.delete("/sources/{id}")
def delete_source(id: str):
    service = CrawlerService()
    service.delete_source(id)
    return success_response(None)


@router.post("/sources/{id}/toggle")
def toggle_source(id: str):
    service = CrawlerService()
    source = service.toggle_source_status(id)
    return success_response(source)


# ========== Task Routes ==========
@router.get("/tasks")
def get_tasks(
    page: int = 1,
    limit: int = 20,
    status: str | None = None,
):
    service = CrawlerService()
    tasks, total = service.find_all_tasks(page, limit, status)
    return success_response(tasks, meta={"total": total, "page": page, "limit": limit})


@router.get("/sources/{source_id}/tasks")
def get_source_tasks(
    source_id: str,
    page: int = 1,
    limit: int = 20,
):
    service = CrawlerService()
    tasks, total = service.find_tasks_by_source(source_id, page, limit)
    return success_response(tasks, meta={"total": total, "page": page, "limit": limit})


@router.post("/sources/{source_id}/trigger")
def trigger_crawl(source_id: str):
    service = CrawlerService()
    task = service.trigger_crawl(source_id)
    return success_response(task)


@router.put("/tasks/{task_id}/status")
def update_task_status(
    task_id: str,
    status: str,
    records_count: int | None = None,
    error_message: str | None = None,
):
    service = CrawlerService()
    task = service.update_task_status(task_id, status, records_count, error_message)
    return success_response(task)
