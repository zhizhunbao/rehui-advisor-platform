"""系统配置管理服务 - 使用 Supabase API"""
import json

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class ConfigService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "system_configs"

    def find_all(
        self,
        category: str | None = None,
        include_sensitive: bool = False,
    ) -> list[dict]:
        query = self.client.table(self.table).select("*")

        if category:
            query = query.eq("category", category)

        if not include_sensitive:
            query = query.eq("is_sensitive", False)

        query = query.order("category").order("key")
        response = query.execute()

        # 解析 JSON 值
        configs = []
        for config in response.data or []:
            config["parsed_value"] = self._parse_value(config.get("value"))
            configs.append(config)
        return configs

    def find_by_key(self, key: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("key", key)
            .maybe_single()
            .execute()
        )
        if response.data:
            response.data["parsed_value"] = self._parse_value(response.data.get("value"))
        return response.data

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if response.data:
            response.data["parsed_value"] = self._parse_value(response.data.get("value"))
        return response.data

    def get_value(self, key: str, default: any = None) -> any:
        """获取配置值（解析后的）"""
        config = self.find_by_key(key)
        if not config:
            return default
        return config.get("parsed_value", default)

    def create(self, data: dict) -> dict:
        # 检查 key 是否重复
        existing = self.find_by_key(data.get("key", ""))
        if existing:
            raise AppError(AppErrorCode.DUPLICATE, f"Config key '{data.get('key')}' already exists")

        # 序列化值
        if "value" in data and not isinstance(data["value"], str):
            data["value"] = json.dumps(data["value"])

        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create config")

        result = response.data[0]
        result["parsed_value"] = self._parse_value(result.get("value"))
        return result

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Config {id} not found")

        # 如果更新 key，检查是否重复
        if data.get("key") and data["key"] != existing["key"]:
            key_exists = self.find_by_key(data["key"])
            if key_exists:
                raise AppError(AppErrorCode.DUPLICATE, f"Config key '{data['key']}' already exists")

        # 序列化值
        if "value" in data and not isinstance(data["value"], str):
            data["value"] = json.dumps(data["value"])

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        response = (
            self.client.table(self.table)
            .update(update_data)
            .eq("id", id)
            .execute()
        )

        result = response.data[0]
        result["parsed_value"] = self._parse_value(result.get("value"))
        return result

    def update_by_key(self, key: str, value: any) -> dict:
        """通过 key 更新配置值"""
        existing = self.find_by_key(key)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Config key '{key}' not found")

        serialized_value = json.dumps(value) if not isinstance(value, str) else value

        response = (
            self.client.table(self.table)
            .update({"value": serialized_value})
            .eq("key", key)
            .execute()
        )

        result = response.data[0]
        result["parsed_value"] = self._parse_value(result.get("value"))
        return result

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Config {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()

    def get_categories(self) -> list[str]:
        """获取所有配置分类"""
        response = (
            self.client.table(self.table)
            .select("category")
            .execute()
        )
        categories = set()
        for config in response.data or []:
            if config.get("category"):
                categories.add(config["category"])
        return sorted(list(categories))

    def _parse_value(self, value: str | None) -> any:
        """解析 JSON 值"""
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
