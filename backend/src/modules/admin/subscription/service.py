"""订阅方案管理服务 - 使用 Supabase API"""
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class SubscriptionService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "subscription_plans"

    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        is_active: bool | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.table).select("*", count="exact")

        if is_active is not None:
            query = query.eq("is_active", is_active)

        query = query.order("sort_order")
        query = query.range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def find_active(self) -> list[dict]:
        """获取所有激活的订阅方案（用于前端展示）"""
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("is_active", True)
            .order("sort_order")
            .execute()
        )
        return response.data

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def find_by_name(self, name: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("name", name)
            .maybe_single()
            .execute()
        )
        return response.data

    def create(self, data: dict) -> dict:
        # 检查名称是否重复
        existing = self.find_by_name(data.get("name", ""))
        if existing:
            raise AppError(AppErrorCode.DUPLICATE, "Subscription plan name already exists")

        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create subscription plan")
        return response.data[0]

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Subscription plan {id} not found")

        # 如果更新名称，检查是否重复
        if data.get("name") and data["name"] != existing["name"]:
            name_exists = self.find_by_name(data["name"])
            if name_exists:
                raise AppError(AppErrorCode.DUPLICATE, "Subscription plan name already exists")

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
            raise AppError(AppErrorCode.NOT_FOUND, f"Subscription plan {id} not found")

        # 检查是否有用户使用此方案
        users_response = (
            self.client.table("users")
            .select("id", count="exact")
            .eq("subscription_plan", existing.get("name"))
            .execute()
        )
        if users_response.count and users_response.count > 0:
            raise AppError(
                AppErrorCode.VALIDATION_ERROR,
                f"Cannot delete: {users_response.count} users are using this plan"
            )

        self.client.table(self.table).delete().eq("id", id).execute()

    def toggle_status(self, id: str) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Subscription plan {id} not found")

        new_status = not existing.get("is_active", True)
        response = (
            self.client.table(self.table)
            .update({"is_active": new_status})
            .eq("id", id)
            .execute()
        )
        return response.data[0]
