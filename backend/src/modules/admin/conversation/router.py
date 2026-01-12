"""对话记录管理路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .service import ConversationAdminService

router = APIRouter(
    prefix="/admin/conversations",
    tags=["admin-conversations"],
    dependencies=[Depends(get_current_admin)],
)


# ========== Root (alias for sessions) ==========
@router.get("")
def get_conversations(
    page: int = 1,
    limit: int = 20,
    user_id: str | None = None,
    domain: str | None = None,
):
    """获取对话列表（sessions 的别名）"""
    service = ConversationAdminService()
    sessions, total = service.find_all_sessions(page, limit, user_id, domain)
    return success_response(sessions, meta={"total": total, "page": page, "limit": limit})


# ========== Sessions ==========
@router.get("/sessions")
def get_sessions(
    page: int = 1,
    limit: int = 20,
    user_id: str | None = None,
    domain: str | None = None,
):
    service = ConversationAdminService()
    sessions, total = service.find_all_sessions(page, limit, user_id, domain)
    return success_response(sessions, meta={"total": total, "page": page, "limit": limit})


@router.get("/sessions/{id}")
def get_session(id: str):
    service = ConversationAdminService()
    session = service.find_session_by_id(id)
    return success_response(session)


@router.get("/sessions/{session_id}/messages")
def get_session_messages(
    session_id: str,
    page: int = 1,
    limit: int = 50,
):
    service = ConversationAdminService()
    messages, total = service.find_messages_by_session(session_id, page, limit)
    return success_response(messages, meta={"total": total, "page": page, "limit": limit})


@router.delete("/sessions/{id}")
def delete_session(id: str):
    service = ConversationAdminService()
    service.delete_session(id)
    return success_response(None)


# ========== Messages ==========
@router.get("/messages")
def get_messages(
    page: int = 1,
    limit: int = 50,
    role: str | None = None,
):
    service = ConversationAdminService()
    messages, total = service.find_all_messages(page, limit, role)
    return success_response(messages, meta={"total": total, "page": page, "limit": limit})


@router.delete("/messages/{id}")
def delete_message(id: str):
    service = ConversationAdminService()
    service.delete_message(id)
    return success_response(None)


# ========== Stats ==========
@router.get("/stats")
def get_conversation_stats():
    service = ConversationAdminService()
    stats = service.get_stats()
    return success_response(stats)
