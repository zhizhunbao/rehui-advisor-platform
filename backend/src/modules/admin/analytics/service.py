"""统计分析服务 - 使用 Document Store"""
from src.common.document import DocumentStore


class AnalyticsService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def get_summary(self) -> dict:
        """获取统计摘要"""
        # 统计用户数
        total_users = self.store.count("member_user")

        # 统计会话数
        total_sessions = self.store.count("admin_chat_session")

        # 统计消息数
        total_messages = self.store.count("admin_chat_message")

        return {
            "total_users": total_users,
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "active_users_today": 0,
            "popular_domains": [],
            "recent_activity": [],
        }
