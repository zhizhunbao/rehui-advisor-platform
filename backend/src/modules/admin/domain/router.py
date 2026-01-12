"""领域配置路由 - 使用 Supabase API"""
from fastapi import APIRouter

from src.common.response import success_response
from src.common.supabase import get_supabase_admin

router = APIRouter(prefix="/domains", tags=["domains"])


@router.get("/active")
def get_active_domains():
    """获取所有激活的领域配置（用户端使用）"""
    client = get_supabase_admin()
    response = (
        client.table("domains")
        .select("*")
        .eq("is_active", True)
        .order("sort_order")
        .execute()
    )
    
    return success_response([
        {
            "id": d["id"],
            "code": d.get("code"),
            "name": d.get("name"),
            "nameEn": d.get("name_en"),
            "description": d.get("description"),
            "descriptionEn": d.get("description_en"),
            "icon": d.get("icon"),
            "color": d.get("color"),
            "prompt": d.get("prompt"),
            "promptEn": d.get("prompt_en"),
            "sortOrder": d.get("sort_order"),
        }
        for d in response.data
    ])
