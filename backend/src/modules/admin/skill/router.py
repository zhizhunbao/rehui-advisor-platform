"""Skills 路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import UpdateSkillRequest, CreateCategoryLabelRequest, UpdateCategoryLabelRequest
from .service import SkillService

router = APIRouter(prefix="/skills", tags=["skills"])


# ========== 分类标签 API ==========
@router.get("/labels")
def get_all_labels():
    """获取所有分类和来源标签"""
    service = SkillService()
    labels = service.get_all_category_labels()
    return success_response(labels)


@router.get("/labels/{type}")
def get_labels_by_type(type: str):
    """获取指定类型的标签 (category/source)"""
    service = SkillService()
    labels = service.get_category_labels(type)
    return success_response(labels)


@router.post("/labels", dependencies=[Depends(get_current_admin)])
def create_label(data: CreateCategoryLabelRequest):
    """创建分类/来源标签"""
    service = SkillService()
    label = service.create_category_label(data.model_dump())
    return success_response(label)


@router.put("/labels/{id}", dependencies=[Depends(get_current_admin)])
def update_label(id: str, data: UpdateCategoryLabelRequest):
    """更新分类/来源标签"""
    service = SkillService()
    label = service.update_category_label(id, data.model_dump())
    return success_response(label)


@router.delete("/labels/{id}", dependencies=[Depends(get_current_admin)])
def delete_label(id: str):
    """删除分类/来源标签"""
    service = SkillService()
    service.delete_category_label(id)
    return success_response(None)


# ========== Skills API ==========
@router.get("/")
def get_skills(
    page: int = 1,
    limit: int = 20,
    category: str | None = None,
    source: str | None = None,
    search: str | None = None,
):
    """获取 Skills 列表"""
    service = SkillService()
    data, total = service.find_all(page, limit, category, source, search)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/stats")
def get_stats():
    """获取统计信息"""
    service = SkillService()
    stats = service.get_stats()
    return success_response(stats)


@router.get("/categories")
def get_categories():
    """获取所有分类"""
    service = SkillService()
    categories = service.get_categories()
    return success_response(categories)


@router.get("/sources")
def get_sources():
    """获取所有来源"""
    service = SkillService()
    sources = service.get_sources()
    return success_response(sources)


@router.get("/{id}")
def get_skill(id: str):
    """获取单个 Skill"""
    service = SkillService()
    skill = service.find_by_id(id)
    return success_response(skill)


# ========== Admin Routes ==========
@router.put("/{id}", dependencies=[Depends(get_current_admin)])
def update_skill(id: str, data: UpdateSkillRequest):
    """更新 Skill (管理员)"""
    service = SkillService()
    skill = service.update(id, data.model_dump())
    return success_response(skill)


@router.post("/{id}/toggle", dependencies=[Depends(get_current_admin)])
def toggle_skill(id: str):
    """切换 Skill 启用状态 (管理员)"""
    service = SkillService()
    skill = service.toggle_active(id)
    return success_response(skill)


@router.post("/sync", dependencies=[Depends(get_current_admin)])
def sync_skills():
    """从 GitHub 同步官方 Skills (管理员)"""
    service = SkillService()
    result = service.sync_from_github()
    return success_response(result)
