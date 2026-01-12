"""推荐方案管理服务 - 使用 Supabase API"""
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class RecommendationAdminService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "recommendations"

    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        user_id: str | None = None,
        domain: str | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.table).select("*", count="exact")

        if user_id:
            query = query.eq("user_id", user_id)
        if domain:
            query = query.eq("domain", domain)

        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def find_by_user(self, user_id: str, domain: str | None = None) -> list[dict]:
        query = (
            self.client.table(self.table)
            .select("*")
            .eq("user_id", user_id)
        )
        if domain:
            query = query.eq("domain", domain)
        query = query.order("ranking")
        response = query.execute()
        return response.data

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Recommendation {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        response = (
            self.client.table(self.table)
            .update(update_data)
            .eq("id", id)
            .execute()
        )
        return response.data[0]

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Recommendation {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()

    def delete_by_user(self, user_id: str) -> int:
        """删除用户的所有推荐"""
        response = (
            self.client.table(self.table)
            .delete()
            .eq("user_id", user_id)
            .execute()
        )
        return len(response.data) if response.data else 0

    def get_stats(self) -> dict:
        """获取推荐统计"""
        # 总推荐数
        total_response = (
            self.client.table(self.table)
            .select("id", count="exact")
            .execute()
        )
        total = total_response.count or 0

        # 按领域统计
        domain_response = (
            self.client.table(self.table)
            .select("domain")
            .execute()
        )
        domain_counts: dict[str, int] = {}
        for rec in domain_response.data or []:
            domain = rec.get("domain", "unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        return {
            "total": total,
            "by_domain": domain_counts,
        }
