"""对话记录管理服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode


DOC_TYPE_SESSION = "admin_chat_session"
DOC_TYPE_MESSAGE = "admin_chat_message"


class ConversationAdminService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    # ========== Sessions ==========
    def find_all_sessions(
        self,
        page: int = 1,
        limit: int = 20,
        user_id: str | None = None,
        domain: str | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_SESSION, status="active")
        
        # 过滤
        sessions = []
        for doc in docs:
            data = doc["data"]
            if user_id and data.get("user_id") != user_id:
                continue
            if domain and data.get("domain") != domain:
                continue
            sessions.append(self._session_to_response(doc))
        
        # 排序
        sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        total = len(sessions)
        start = (page - 1) * limit
        end = start + limit
        
        return sessions[start:end], total

    def find_session_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_SESSION or doc["status"] == "deleted":
            return None
        return self._session_to_response(doc)

    def delete_session(self, id: str) -> None:
        existing = self.find_session_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Session {id} not found")

        # 先删除关联的消息
        messages = self.store.find(DOC_TYPE_MESSAGE, status="active")
        for msg in messages:
            if msg["data"].get("session_id") == id:
                self.store.delete(msg["id"], hard=True)
        
        # 再删除会话
        self.store.delete(id, hard=True)

    # ========== Messages ==========
    def find_messages_by_session(
        self,
        session_id: str,
        page: int = 1,
        limit: int = 50,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_MESSAGE, status="active")
        
        # 过滤指定 session 的消息
        messages = []
        for doc in docs:
            if doc["data"].get("session_id") == session_id:
                messages.append(self._message_to_response(doc))
        
        # 按时间正序排序
        messages.sort(key=lambda x: x.get("created_at", ""))
        
        # 分页
        total = len(messages)
        start = (page - 1) * limit
        end = start + limit
        
        return messages[start:end], total

    def find_all_messages(
        self,
        page: int = 1,
        limit: int = 50,
        role: str | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_MESSAGE, status="active")
        
        # 过滤
        messages = []
        for doc in docs:
            data = doc["data"]
            if role and data.get("role") != role:
                continue
            messages.append(self._message_to_response(doc))
        
        # 排序
        messages.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        total = len(messages)
        start = (page - 1) * limit
        end = start + limit
        
        return messages[start:end], total

    def delete_message(self, id: str) -> None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_MESSAGE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"Message {id} not found")
        self.store.delete(id, hard=True)

    # ========== Stats ==========
    def get_stats(self) -> dict:
        """获取对话统计"""
        sessions = self.store.find(DOC_TYPE_SESSION, status="active")
        messages = self.store.find(DOC_TYPE_MESSAGE, status="active")
        
        total_sessions = len(sessions)
        total_messages = len(messages)
        
        # 按领域统计会话
        domain_counts: dict[str, int] = {}
        for doc in sessions:
            domain = doc["data"].get("domain", "unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "by_domain": domain_counts,
        }

    def _session_to_response(self, doc: dict) -> dict:
        """转换 session 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "user_id": data.get("user_id"),
            "domain": data.get("domain"),
            "title": data.get("title"),
            "metadata": data.get("metadata", {}),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }

    def _message_to_response(self, doc: dict) -> dict:
        """转换 message 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "session_id": data.get("session_id"),
            "role": data.get("role"),
            "content": data.get("content"),
            "metadata": data.get("metadata", {}),
            "created_at": doc.get("created_at"),
        }
