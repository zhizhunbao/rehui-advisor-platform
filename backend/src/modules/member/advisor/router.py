"""顾问服务路由 - 使用 Supabase API"""
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.common.auth import check_quota
from src.common.supabase import get_supabase_admin
from .dto import ChatRequest, ChatStreamChunk
from .service import AdvisorService

router = APIRouter(prefix="/advisor", tags=["advisor"])


@router.post("/chat")
def chat(
    data: ChatRequest,
    user: dict = Depends(check_quota),
):
    service = AdvisorService()
    client = get_supabase_admin()

    async def generate():
        try:
            messages = [{"role": m.role, "content": m.content} for m in data.messages]
            async for chunk in service.stream_chat(messages, data.lang):
                if chunk.done:
                    break
                response = ChatStreamChunk(text=chunk.text, sources=[])
                yield f"data: {json.dumps(response.model_dump())}\n\n"

            # 成功完成后递增配额
            client.table("users").update({
                "search_count": user.get("search_count", 0) + 1,
                "last_search_at": datetime.now(timezone.utc).isoformat(),
            }).eq("id", user["id"]).execute()

            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/health")
def health():
    from src.common.response import success_response
    return success_response({"status": "ok", "service": "advisor"})
