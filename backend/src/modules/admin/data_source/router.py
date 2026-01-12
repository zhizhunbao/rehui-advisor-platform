"""Data Source 路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import (
    CreateDataSourceRequest,
    UpdateDataSourceRequest,
    BatchAddRequest,
    GitHubDiscoverRequest,
    BatchImportRequest,
)
from .service import DataSourceService

router = APIRouter(prefix="/data-sources", tags=["data-sources"])


@router.get("/")
def get_sources(
    page: int = 1,
    limit: int = 20,
    type: str | None = None,
    category_id: str | None = None,
    domain_id: str | None = None,
    domain_code: str | None = None,
    status: str | None = None,
    language: str | None = None,
    search: str | None = None,
):
    service = DataSourceService()
    data, total = service.find_all(
        page, limit, type,
        category_id, domain_id, status, language, search,
        domain_code=domain_code
    )
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/stats")
def get_stats():
    service = DataSourceService()
    return success_response(service.get_stats())


@router.get("/categories")
def get_categories():
    service = DataSourceService()
    return success_response(service.get_categories())


@router.get("/categories/{category_id}/domains")
def get_domains_by_category(category_id: str):
    """获取指定分类下的所有领域"""
    service = DataSourceService()
    return success_response(service.get_domains_by_category(category_id))


@router.get("/domains")
def get_all_domains():
    """获取所有领域"""
    service = DataSourceService()
    return success_response(service.get_domains_by_category(None))


@router.get("/types")
def get_types():
    service = DataSourceService()
    return success_response(service.get_types())


@router.get("/statuses")
def get_statuses():
    service = DataSourceService()
    return success_response(service.get_statuses())


@router.get("/languages")
def get_languages():
    service = DataSourceService()
    return success_response(service.get_languages())


@router.get("/{id}")
def get_source(id: str):
    service = DataSourceService()
    return success_response(service.find_by_id(id))


@router.post("/", dependencies=[Depends(get_current_admin)])
def create_source(data: CreateDataSourceRequest):
    service = DataSourceService()
    return success_response(service.create(data.model_dump()))


@router.post("/batch", dependencies=[Depends(get_current_admin)])
def batch_add(data: BatchAddRequest):
    service = DataSourceService()
    return success_response(service.batch_add(data.urls, data.type, data.category_id))


@router.put("/{id}", dependencies=[Depends(get_current_admin)])
def update_source(id: str, data: UpdateDataSourceRequest):
    service = DataSourceService()
    return success_response(service.update(id, data.model_dump()))


@router.post("/{id}/refresh", dependencies=[Depends(get_current_admin)])
def refresh_source(id: str):
    service = DataSourceService()
    return success_response(service.refresh(id))


@router.post("/refresh-all", dependencies=[Depends(get_current_admin)])
def refresh_all(category: str | None = None):
    service = DataSourceService()
    return success_response(service.refresh_all(category))


@router.delete("/{id}", dependencies=[Depends(get_current_admin)])
def delete_source(id: str):
    service = DataSourceService()
    service.delete(id)
    return success_response(None)


# ========== 探索功能 ==========
@router.post("/discover/github", dependencies=[Depends(get_current_admin)])
def discover_github(data: GitHubDiscoverRequest):
    service = DataSourceService()
    results = service.discover_github(
        query=data.query,
        sort=data.sort,
        order=data.order,
        per_page=data.per_page,
    )
    return success_response(results)


@router.post("/discover/import", dependencies=[Depends(get_current_admin)])
def batch_import(data: BatchImportRequest):
    service = DataSourceService()
    result = service.batch_import(data.items, data.category_id, data.domain_id)
    return success_response(result)


@router.get("/discover/domains", dependencies=[Depends(get_current_admin)])
def get_domain_keywords():
    service = DataSourceService()
    return success_response(service.get_domain_keywords())


@router.post("/discover/auto/{domain}", dependencies=[Depends(get_current_admin)])
def auto_discover(domain: str, limit_per_keyword: int = 10):
    service = DataSourceService()
    result = service.auto_discover(domain, limit_per_keyword)
    return success_response(result)


@router.get("/discover/stats", dependencies=[Depends(get_current_admin)])
def get_discovery_stats(category: str | None = None):
    """获取探索统计信息，用于优化探索策略"""
    service = DataSourceService()
    return success_response(service.get_discovery_stats(category))
