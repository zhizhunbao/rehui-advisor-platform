"""系统配置管理服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode


DOC_TYPE = "admin_config"


class ConfigService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(
        self,
        category: str | None = None,
        include_sensitive: bool = False,
    ) -> list[dict]:
        docs = self.store.find(DOC_TYPE, status="active")
        
        configs = []
        for doc in docs:
            data = doc["data"]
            
            # 过滤分类
            if category and data.get("category") != category:
                continue
            
            # 过滤敏感配置
            if not include_sensitive and data.get("is_sensitive"):
                continue
            
            configs.append(self._to_response(doc))
        
        # 排序
        configs.sort(key=lambda x: (x.get("category", ""), x.get("key", "")))
        return configs

    def find_by_key(self, key: str) -> dict | None:
        # 使用 Supabase 的 JSONB 查询语法
        docs = self.store.find(DOC_TYPE, status="active")
        for doc in docs:
            if doc["data"].get("key") == key:
                return self._to_response(doc)
        return None

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def get_value(self, key: str, default=None):
        """获取配置值"""
        config = self.find_by_key(key)
        if not config:
            return default
        return config.get("value", default)

    def create(self, data: dict) -> dict:
        # 检查 key 是否重复
        existing = self.find_by_key(data.get("key", ""))
        if existing:
            raise AppError(AppErrorCode.DUPLICATE, f"Config key '{data.get('key')}' already exists")

        doc = self.store.create(DOC_TYPE, {
            "key": data["key"],
            "value": data["value"],
            "description": data.get("description"),
            "category": data.get("category", "general"),
            "is_sensitive": data.get("is_sensitive", False),
        })
        
        return self._to_response(doc)

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Config {id} not found")

        # 如果更新 key，检查是否重复
        if data.get("key") and data["key"] != existing["key"]:
            key_exists = self.find_by_key(data["key"])
            if key_exists:
                raise AppError(AppErrorCode.DUPLICATE, f"Config key '{data['key']}' already exists")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        doc = self.store.update(id, data_updates=update_data)
        return self._to_response(doc)

    def update_by_key(self, key: str, value) -> dict:
        """通过 key 更新配置值"""
        existing = self.find_by_key(key)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Config key '{key}' not found")

        doc = self.store.update(existing["id"], data_updates={"value": value})
        return self._to_response(doc)

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Config {id} not found")
        self.store.delete(id)

    def get_categories(self) -> list[str]:
        """获取所有配置分类"""
        docs = self.store.find(DOC_TYPE, status="active")
        categories = set()
        for doc in docs:
            category = doc["data"].get("category")
            if category:
                categories.add(category)
        return sorted(list(categories))

    def _to_response(self, doc: dict) -> dict:
        """转换为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "key": data.get("key"),
            "value": data.get("value"),
            "description": data.get("description"),
            "category": data.get("category"),
            "is_sensitive": data.get("is_sensitive", False),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
