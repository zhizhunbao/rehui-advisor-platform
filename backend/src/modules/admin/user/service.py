"""用户管理服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.helper import paginate

DOC_TYPE = "admin_user"


class UserAdminService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        status: str | None = None,
        subscription_plan: str | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        filtered = []
        for doc in docs:
            data = doc["data"]
            
            if search:
                search_lower = search.lower()
                email = (data.get("email") or "").lower()
                name = (data.get("name") or "").lower()
                if search_lower not in email and search_lower not in name:
                    continue
            
            if status and data.get("status") != status:
                continue
            
            if subscription_plan and data.get("subscription_plan") != subscription_plan:
                continue
            
            filtered.append(doc)
        
        filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        paged, total = paginate(filtered, page, limit)
        
        return [self._to_response(doc) for doc in paged], total

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def find_by_email(self, email: str) -> dict | None:
        docs = self.store.find(DOC_TYPE, status="active")
        for doc in docs:
            if doc["data"].get("email") == email:
                return self._to_response(doc)
        return None

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"User {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        doc = self.store.update(id, data_updates=update_data)
        return self._to_response(doc)

    def toggle_status(self, id: str) -> dict:
        """切换用户状态"""
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"User {id} not found")

        current_status = existing.get("status", "active")
        new_status = "inactive" if current_status == "active" else "active"

        doc = self.store.update(id, data_updates={"status": new_status})
        return self._to_response(doc)

    def update_subscription(self, id: str, plan: str) -> dict:
        """更新用户订阅方案"""
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"User {id} not found")

        doc = self.store.update(id, data_updates={"subscription_plan": plan})
        return self._to_response(doc)

    def get_user_stats(self) -> dict:
        """获取用户统计信息"""
        docs = self.store.find(DOC_TYPE, status="active")
        
        total = len(docs)
        active = sum(1 for doc in docs if doc["data"].get("status") == "active")
        
        plan_counts: dict[str, int] = {}
        for doc in docs:
            plan = doc["data"].get("subscription_plan") or "free"
            plan_counts[plan] = plan_counts.get(plan, 0) + 1

        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "by_plan": plan_counts,
        }

    def _to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "email": data.get("email"),
            "name": data.get("name"),
            "avatar": data.get("avatar"),
            "status": data.get("status", "active"),
            "subscription_plan": data.get("subscription_plan", "free"),
            "quota_used": data.get("quota_used", 0),
            "quota_limit": data.get("quota_limit"),
            "last_login_at": data.get("last_login_at"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
