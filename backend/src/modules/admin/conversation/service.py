"""对话记录管理服务 - 使用 Supabase API"""
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class ConversationAdminService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.sessions_table = "chat_sessions"
        self.messages_table = "chat_messages"

    # ========== Sessions ==========
    def find_all_sessions(
        self,
        page: int = 1,
        limit: int = 20,
        user_id: str | None = None,
        domain: str | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.sessions_table).select("*", count="exact")

        if user_id:
            query = query.eq("user_id", user_id)
        if domain:
            query = query.eq("domain", domain)

        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def find_session_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.sessions_table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def delete_session(self, id: str) -> None:
        existing = self.find_session_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Session {id} not found")

        # 先删除关联的消息
        self.client.table(self.messages_table).delete().eq("session_id", id).execute()
        # 再删除会话
        self.client.table(self.sessions_table).delete().eq("id", id).execute()

    # ========== Messages ==========
    def find_messages_by_session(
        self,
        session_id: str,
        page: int = 1,
        limit: int = 50,
    ) -> tuple[list[dict], int]:
        query = (
            self.client.table(self.messages_table)
            .select("*", count="exact")
            .eq("session_id", session_id)
            .order("created_at")
            .range((page - 1) * limit, page * limit - 1)
        )
        response = query.execute()
        return response.data, response.count or 0

    def find_all_messages(
        self,
        page: int = 1,
        limit: int = 50,
        role: str | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.messages_table).select("*", count="exact")

        if role:
            query = query.eq("role", role)

        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def delete_message(self, id: str) -> None:
        response = (
            self.client.table(self.messages_table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response.data:
            raise AppError(AppErrorCode.NOT_FOUND, f"Message {id} not found")
        self.client.table(self.messages_table).delete().eq("id", id).execute()

    # ========== Stats ==========
    def get_stats(self) -> dict:
        """获取对话统计"""
        # 总会话数
        sessions_response = (
            self.client.table(self.sessions_table)
            .select("id", count="exact")
            .execute()
        )
        total_sessions = sessions_response.count or 0

        # 总消息数
        messages_response = (
            self.client.table(self.messages_table)
            .select("id", count="exact")
            .execute()
        )
        total_messages = messages_response.count or 0

        # 按领域统计会话
        domain_response = (
            self.client.table(self.sessions_table)
            .select("domain")
            .execute()
        )
        domain_counts: dict[str, int] = {}
        for session in domain_response.data or []:
            domain = session.get("domain", "unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "by_domain": domain_counts,
        }
