"""管理员服务 - 使用 Supabase API"""
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class DomainCategoryService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "domain_categories"

    def find_all(self) -> list[dict]:
        response = (
            self.client.table(self.table)
            .select("*")
            .order("sort_order")
            .execute()
        )
        return response.data

    def find_active(self) -> list[dict]:
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

    def create(self, data: dict) -> dict:
        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create domain category")
        return response.data[0]

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain category {id} not found")
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        return response.data[0]

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain category {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()


class DomainService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "domains"

    def find_all(self, category_id: str | None = None) -> list[dict]:
        # Join prompt_templates to get linked prompt info
        query = self.client.table(self.table).select(
            "*, prompt_templates(id, name, template, template_en)"
        )
        if category_id:
            query = query.eq("category_id", category_id)
        response = query.order("sort_order").execute()
        return response.data

    def find_active(self) -> list[dict]:
        response = (
            self.client.table(self.table)
            .select("*, prompt_templates(id, name, template, template_en)")
            .eq("is_active", True)
            .order("sort_order")
            .execute()
        )
        return response.data

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*, prompt_templates(id, name, template, template_en)")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def create(self, data: dict) -> dict:
        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create domain")
        return response.data[0]

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain {id} not found")
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        return response.data[0]

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()


class PromptService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "prompt_templates"

    def find_all(self) -> list[dict]:
        response = self.client.table(self.table).select("*").execute()
        return response.data

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )
        return response.data

    def create(self, data: dict) -> dict:
        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create prompt")
        return response.data[0]

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt {id} not found")
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        return response.data[0]

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()


class QuestionService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "questions"

    def find_all(self, domain_id: str | None = None) -> list[dict]:
        query = self.client.table(self.table).select("*")
        if domain_id:
            query = query.eq("domain_id", domain_id)
        query = query.order("sort_order")
        response = query.execute()
        return response.data

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )
        return response.data

    def create(self, data: dict) -> dict:
        response = self.client.table(self.table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create question")
        return response.data[0]

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Question {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()


class AnalyticsService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()

    def get_summary(self) -> dict:
        # Total users
        users_response = (
            self.client.table("users")
            .select("id", count="exact")
            .execute()
        )
        total_users = users_response.count or 0

        return {
            "total_users": total_users,
            "total_sessions": 0,
            "total_messages": 0,
            "active_users_today": 0,
            "popular_domains": [],
            "recent_activity": [],
        }
