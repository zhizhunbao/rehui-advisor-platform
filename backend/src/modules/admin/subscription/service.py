"""订阅方案管理服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.helper import paginate

DOC_TYPE = "admin_subscription"


class SubscriptionService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        is_active: bool | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        filtered = []
        for doc in docs:
            data = doc["data"]
            if is_active is not None and data.get("is_active") != is_active:
                continue
            filtered.append(doc)
        
        filtered.sort(key=lambda x: x["data"].get("sort_order", 0))
        paged, total = paginate(filtered, page, limit)
        
        return [self._to_response(doc) for doc in paged], total

    def find_active(self) -> list[dict]:
        """获取所有激活的订阅方案"""
        docs = self.store.find(DOC_TYPE, status="active")
        plans = [
            self._to_response(doc)
            for doc in docs
            if doc["data"].get("is_active", True)
        ]
        plans.sort(key=lambda x: x.get("sort_order", 0))
        return plans

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def find_by_name(self, name: str) -> dict | None:
        docs = self.store.find(DOC_TYPE, status="active")
        for doc in docs:
            if doc["data"].get("name") == name:
                return self._to_response(doc)
        return None

    def create(self, data: dict) -> dict:
        existing = self.find_by_name(data.get("name", ""))
        if existing:
            raise AppError(AppErrorCode.DUPLICATE, "Subscription plan name already exists")

        doc = self.store.create(DOC_TYPE, data)
        return self._to_response(doc)

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Subscription plan {id} not found")

        if data.get("name") and data["name"] != existing["name"]:
            name_exists = self.find_by_name(data["name"])
            if name_exists:
                raise AppError(AppErrorCode.DUPLICATE, "Subscription plan name already exists")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        doc = self.store.update(id, data_updates=update_data)
        return self._to_response(doc)

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Subscription plan {id} not found")

        # TODO: 检查是否有用户使用此方案
        self.store.delete(id)

    def toggle_status(self, id: str) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Subscription plan {id} not found")

        new_status = not existing.get("is_active", True)
        doc = self.store.update(id, data_updates={"is_active": new_status})
        return self._to_response(doc)

    def _to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "name": data.get("name"),
            "display_name": data.get("display_name"),
            "description": data.get("description"),
            "price_monthly": data.get("price_monthly"),
            "price_yearly": data.get("price_yearly"),
            "features": data.get("features", []),
            "limits": data.get("limits", {}),
            "sort_order": data.get("sort_order", 0),
            "is_active": data.get("is_active", True),
            "is_popular": data.get("is_popular", False),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
