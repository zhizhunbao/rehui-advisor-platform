"""系统配置管理路由 - 仅超级管理员可访问"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin, require_super_admin
from src.common.response import success_response
from .dto import CreateConfigRequest, UpdateConfigRequest, UpdateValueRequest
from .service import ConfigService

router = APIRouter(
    prefix="/admin/configs",
    tags=["admin-configs"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
def get_configs(
    category: str | None = None,
    include_sensitive: bool = False,
    admin=Depends(require_super_admin),
):
    """获取所有配置（仅超级管理员）"""
    service = ConfigService()
    configs = service.find_all(category, include_sensitive)
    return success_response(configs)


@router.get("/categories")
def get_categories(admin=Depends(require_super_admin)):
    """获取所有配置分类"""
    service = ConfigService()
    categories = service.get_categories()
    return success_response(categories)


@router.get("/key/{key}")
def get_config_by_key(key: str, admin=Depends(require_super_admin)):
    """通过 key 获取配置"""
    service = ConfigService()
    config = service.find_by_key(key)
    return success_response(config)


@router.get("/{id}")
def get_config(id: str, admin=Depends(require_super_admin)):
    """通过 ID 获取配置"""
    service = ConfigService()
    config = service.find_by_id(id)
    return success_response(config)


@router.post("/")
def create_config(data: CreateConfigRequest, admin=Depends(require_super_admin)):
    """创建配置（仅超级管理员）"""
    service = ConfigService()
    config = service.create(data.model_dump())
    return success_response(config)


@router.put("/{id}")
def update_config(id: str, data: UpdateConfigRequest, admin=Depends(require_super_admin)):
    """更新配置（仅超级管理员）"""
    service = ConfigService()
    config = service.update(id, data.model_dump(exclude_unset=True))
    return success_response(config)


@router.put("/key/{key}")
def update_config_by_key(key: str, data: UpdateValueRequest, admin=Depends(require_super_admin)):
    """通过 key 更新配置值（仅超级管理员）"""
    service = ConfigService()
    config = service.update_by_key(key, data.value)
    return success_response(config)


@router.delete("/{id}")
def delete_config(id: str, admin=Depends(require_super_admin)):
    """删除配置（仅超级管理员）"""
    service = ConfigService()
    service.delete(id)
    return success_response(None)
