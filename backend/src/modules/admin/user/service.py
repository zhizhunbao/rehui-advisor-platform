"""用户管理服务 - 使用 Supabase API"""
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class UserAdminService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "users"

    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        status: str | None = None,
        subscription_plan: str | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.table).select("*", count="exact")

        # 搜索过滤
        if search:
            query = query.or_(f"email.ilike.%{search}%,name.ilike.%{search}%")

        # 状态过滤
        if status:
            query = query.eq("status", status)

        # 订阅方案过滤
        if subscription_plan:
            query = query.eq("subscription_plan", subscription_plan)

        # 排序和分页
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

    def find_by_email(self, email: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("email", email)
            .maybe_single()
            .execute()
        )
        return response.data

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"User {id} not found")

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

    def toggle_status(self, id: str) -> dict:
        """切换用户状态（active/inactive）"""
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"User {id} not found")

        current_status = existing.get("status", "active")
        new_status = "inactive" if current_status == "active" else "active"

        response = (
            self.client.table(self.table)
            .update({"status": new_status})
            .eq("id", id)
            .execute()
        )
        return response.data[0]

    def update_subscription(self, id: str, plan: str) -> dict:
        """更新用户订阅方案"""
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"User {id} not found")

        response = (
            self.client.table(self.table)
            .update({"subscription_plan": plan})
            .eq("id", id)
            .execute()
        )
        return response.data[0]

    def get_user_stats(self) -> dict:
        """获取用户统计信息"""
        # 总用户数
        total_response = (
            self.client.table(self.table)
            .select("id", count="exact")
            .execute()
        )
        total = total_response.count or 0

        # 活跃用户数
        active_response = (
            self.client.table(self.table)
            .select("id", count="exact")
            .eq("status", "active")
            .execute()
        )
        active = active_response.count or 0

        # 按订阅方案统计
        plans_response = (
            self.client.table(self.table)
            .select("subscription_plan")
            .execute()
        )
        plan_counts: dict[str, int] = {}
        for user in plans_response.data or []:
            plan = user.get("subscription_plan") or "free"
            plan_counts[plan] = plan_counts.get(plan, 0) + 1

        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "by_plan": plan_counts,
        }
