"""Prompt 路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import UpdatePromptRequest, CreateCategoryLabelRequest, UpdateCategoryLabelRequest
from .service import PromptService

router = APIRouter(prefix="/prompts", tags=["prompts"])


# ========== 分类标签 API ==========
@router.get("/labels")
def get_all_labels():
    """获取所有分类和来源标签"""
    service = PromptService()
    return success_response(service.get_all_category_labels())


@router.get("/labels/{type}")
def get_labels_by_type(type: str):
    """获取指定类型的标签 (category/source)"""
    service = PromptService()
    return success_response(service.get_category_labels(type))


@router.post("/labels", dependencies=[Depends(get_current_admin)])
def create_label(data: CreateCategoryLabelRequest):
    """创建分类/来源标签"""
    service = PromptService()
    return success_response(service.create_category_label(data.model_dump()))


@router.put("/labels/{id}", dependencies=[Depends(get_current_admin)])
def update_label(id: str, data: UpdateCategoryLabelRequest):
    """更新分类/来源标签"""
    service = PromptService()
    return success_response(service.update_category_label(id, data.model_dump()))


@router.delete("/labels/{id}", dependencies=[Depends(get_current_admin)])
def delete_label(id: str):
    """删除分类/来源标签"""
    service = PromptService()
    service.delete_category_label(id)
    return success_response(None)


# ========== Prompts API ==========
@router.get("/")
def get_prompts(
    page: int = 1, limit: int = 20,
    category: str | None = None, source: str | None = None, search: str | None = None,
):
    service = PromptService()
    data, total = service.find_all(page, limit, category, source, search)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/stats")
def get_stats():
    service = PromptService()
    return success_response(service.get_stats())


@router.get("/categories")
def get_categories():
    service = PromptService()
    return success_response(service.get_categories())


@router.get("/sources")
def get_sources():
    service = PromptService()
    return success_response(service.get_sources())


@router.get("/{id}")
def get_prompt(id: str):
    service = PromptService()
    return success_response(service.find_by_id(id))


@router.put("/{id}", dependencies=[Depends(get_current_admin)])
def update_prompt(id: str, data: UpdatePromptRequest):
    service = PromptService()
    return success_response(service.update(id, data.model_dump()))


@router.post("/{id}/toggle", dependencies=[Depends(get_current_admin)])
def toggle_prompt(id: str):
    service = PromptService()
    return success_response(service.toggle_active(id))


@router.post("/sync", dependencies=[Depends(get_current_admin)])
def sync_prompts():
    service = PromptService()
    return success_response(service.sync_from_github())
