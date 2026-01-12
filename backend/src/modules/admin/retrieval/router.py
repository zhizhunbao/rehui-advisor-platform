"""Retrieval Engine Router - 知识检索引擎 API"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import (
    CreateEngineRequest,
    UpdateEngineRequest,
    SetDefaultEngineRequest,
    SetDomainEngineRequest,
    TestEngineRequest,
    CompareEnginesRequest,
)
from .service import RetrievalEngineService

router = APIRouter(
    prefix="/retrieval",
    tags=["retrieval"],
    dependencies=[Depends(get_current_admin)],
)


# ========== 引擎类型 ==========
@router.get("/types")
def get_engine_types():
    """获取所有支持的引擎类型"""
    service = RetrievalEngineService()
    data = service.get_engine_types()
    return success_response(data)


@router.get("/types/{type}/schema")
def get_engine_type_schema(type: str):
    """获取引擎类型的配置 schema"""
    service = RetrievalEngineService()
    data = service.get_engine_type_schema(type)
    return success_response(data)


# ========== 引擎管理 ==========
@router.get("/engines")
def find_all_engines(
    page: int = 1,
    limit: int = 20,
    type: str | None = None,
    is_active: bool | None = None,
):
    """获取引擎列表"""
    service = RetrievalEngineService()
    data, total = service.find_all_engines(page, limit, type, is_active)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/engines/active")
def get_active_engines():
    """获取所有激活的引擎"""
    service = RetrievalEngineService()
    data = service.get_active_engines()
    return success_response(data)


@router.get("/engines/default")
def get_default_engine():
    """获取默认引擎"""
    service = RetrievalEngineService()
    data = service.get_default_engine()
    return success_response(data)


@router.get("/engines/{id}")
def find_engine_by_id(id: str):
    """获取单个引擎"""
    service = RetrievalEngineService()
    data = service.find_engine_by_id(id)
    return success_response(data)


@router.post("/engines")
def create_engine(data: CreateEngineRequest):
    """创建引擎"""
    service = RetrievalEngineService()
    result = service.create_engine(data.model_dump())
    return success_response(result)


@router.put("/engines/{id}")
def update_engine(id: str, data: UpdateEngineRequest):
    """更新引擎"""
    service = RetrievalEngineService()
    result = service.update_engine(id, data.model_dump())
    return success_response(result)


@router.delete("/engines/{id}")
def delete_engine(id: str):
    """删除引擎"""
    service = RetrievalEngineService()
    service.delete_engine(id)
    return success_response(None)


@router.post("/engines/default")
def set_default_engine(data: SetDefaultEngineRequest):
    """设置默认引擎"""
    service = RetrievalEngineService()
    result = service.set_default_engine(data.engine_id)
    return success_response(result)


# ========== 领域配置 ==========
@router.get("/domains")
def get_domain_configs():
    """获取所有领域配置"""
    service = RetrievalEngineService()
    data = service.get_domain_configs()
    return success_response(data)


@router.get("/domains/{domain}/engine")
def get_domain_engine(domain: str):
    """获取领域使用的引擎"""
    service = RetrievalEngineService()
    data = service.get_domain_engine(domain)
    return success_response(data)


@router.post("/domains")
def set_domain_engine(data: SetDomainEngineRequest):
    """设置领域引擎"""
    service = RetrievalEngineService()
    result = service.set_domain_engine(data.domain, data.engine_id)
    return success_response(result)


@router.delete("/domains/{domain}")
def delete_domain_config(domain: str):
    """删除领域配置（回退到默认引擎）"""
    service = RetrievalEngineService()
    service.delete_domain_config(domain)
    return success_response(None)


# ========== 统计 ==========
@router.get("/stats")
def get_stats():
    """获取统计信息"""
    service = RetrievalEngineService()
    data = service.get_stats()
    return success_response(data)


# ========== 测试/对比 ==========
@router.post("/test")
def test_engine(data: TestEngineRequest):
    """测试单个引擎"""
    service = RetrievalEngineService()
    result = service.retrieve(data.query, engine_id=data.engine_id)
    return success_response(result)


@router.post("/compare")
def compare_engines(data: CompareEnginesRequest):
    """对比多个引擎"""
    service = RetrievalEngineService()
    results = service.compare_engines(data.query, data.engine_ids, data.context)
    return success_response(results)
