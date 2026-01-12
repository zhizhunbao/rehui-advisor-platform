"""LLM Router - 模型管理 API"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import (
    CreateLLMModelRequest,
    UpdateLLMModelRequest,
    ChatRequest,
)
from .service import LLMService

router = APIRouter(prefix="/llm", tags=["llm"])


# ========== Models ==========
@router.get("/models", dependencies=[Depends(get_current_admin)])
def get_models(page: int = 1, limit: int = 50):
    """获取所有模型"""
    service = LLMService()
    data, total = service.find_all_models(page, limit)
    return success_response(data, meta={"total": total, "page": page, "limit": limit})


@router.get("/models/active")
def get_active_models():
    """获取可用模型列表（公开）"""
    service = LLMService()
    data = service.find_active_models()
    return success_response(data)


@router.get("/models/filters", dependencies=[Depends(get_current_admin)])
def get_model_filters():
    """获取模型筛选选项"""
    service = LLMService()
    data = service.get_model_filters()
    return success_response(data)


@router.get("/models/default")
def get_default_model():
    """获取默认模型"""
    service = LLMService()
    data = service.get_default_model()
    return success_response(data)


@router.get("/models/{id}", dependencies=[Depends(get_current_admin)])
def get_model(id: str):
    """获取单个模型"""
    service = LLMService()
    data = service.find_model_by_id(id)
    return success_response(data)


@router.post("/models", dependencies=[Depends(get_current_admin)])
def create_model(data: CreateLLMModelRequest):
    """创建模型"""
    service = LLMService()
    result = service.create_model(data.model_dump())
    return success_response(result)


@router.put("/models/{id}", dependencies=[Depends(get_current_admin)])
def update_model(id: str, data: UpdateLLMModelRequest):
    """更新模型"""
    service = LLMService()
    result = service.update_model(id, data.model_dump())
    return success_response(result)


@router.delete("/models/{id}", dependencies=[Depends(get_current_admin)])
def delete_model(id: str):
    """删除模型"""
    service = LLMService()
    service.delete_model(id)
    return success_response(None)


# ========== Sync ==========
@router.get("/sync/sources", dependencies=[Depends(get_current_admin)])
def get_sync_sources():
    """获取同步源列表（从 data_sources 表获取 category=llm-models 的链接）"""
    service = LLMService()
    data = service.get_sync_sources()
    return success_response(data)


@router.post("/sync", dependencies=[Depends(get_current_admin)])
def sync_models(source_id: str | None = None):
    """从 GitHub 同步模型数据
    
    Args:
        source_id: 可选，指定同步源 ID，不指定则同步所有源
    """
    service = LLMService()
    result = service.sync_from_github(source_id)
    return success_response(result)


# ========== Chat (测试用) ==========
@router.post("/chat", dependencies=[Depends(get_current_admin)])
def chat(data: ChatRequest):
    """测试 LLM 调用
    
    使用 prompt_templates 表中的 Prompt 模板调用 LLM
    """
    service = LLMService()
    result = service.chat(data.prompt_name, data.variables, data.model_id)
    return success_response({"content": result})


@router.post("/chat/stream", dependencies=[Depends(get_current_admin)])
def chat_stream(data: ChatRequest):
    """流式测试 LLM 调用"""
    service = LLMService()
    
    def generate():
        for chunk in service.chat_stream(data.prompt_name, data.variables, data.model_id):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
