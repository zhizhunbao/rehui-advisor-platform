"""抓取源管理服务 - 使用 Supabase API"""
from datetime import datetime

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


class CrawlerService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.sources_table = "crawl_sources"
        self.tasks_table = "crawl_tasks"

    # ========== CrawlSource CRUD ==========
    def find_all_sources(
        self,
        page: int = 1,
        limit: int = 20,
        domain_id: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.sources_table).select("*", count="exact")

        if domain_id:
            query = query.eq("domain_id", domain_id)
        if is_active is not None:
            query = query.eq("is_active", is_active)

        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def find_source_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.sources_table)
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )
        return response.data

    def create_source(self, data: dict) -> dict:
        response = self.client.table(self.sources_table).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create source")
        return response.data[0]

    def update_source(self, id: str, data: dict) -> dict:
        # 先检查是否存在
        existing = self.find_source_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {id} not found")

        # 过滤掉 None 值
        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        response = (
            self.client.table(self.sources_table)
            .update(update_data)
            .eq("id", id)
            .execute()
        )
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to update source")
        return response.data[0]

    def delete_source(self, id: str) -> None:
        existing = self.find_source_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {id} not found")

        self.client.table(self.sources_table).delete().eq("id", id).execute()

    def toggle_source_status(self, id: str) -> dict:
        existing = self.find_source_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {id} not found")

        new_status = not existing.get("is_active", True)
        response = (
            self.client.table(self.sources_table)
            .update({"is_active": new_status})
            .eq("id", id)
            .execute()
        )
        return response.data[0]

    # ========== CrawlTask Management ==========
    def find_tasks_by_source(
        self,
        source_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[dict], int]:
        query = (
            self.client.table(self.tasks_table)
            .select("*", count="exact")
            .eq("source_id", source_id)
            .order("created_at", desc=True)
            .range((page - 1) * limit, page * limit - 1)
        )
        response = query.execute()
        return response.data, response.count or 0

    def find_all_tasks(
        self,
        page: int = 1,
        limit: int = 20,
        status: str | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.tasks_table).select("*", count="exact")

        if status:
            query = query.eq("status", status)

        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def trigger_crawl(self, source_id: str) -> dict:
        """触发抓取任务"""
        source = self.find_source_by_id(source_id)
        if not source:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {source_id} not found")
        if not source.get("is_active"):
            raise AppError(AppErrorCode.VALIDATION_ERROR, "Cannot trigger inactive source")

        now = datetime.utcnow().isoformat()

        # 创建任务
        task_response = (
            self.client.table(self.tasks_table)
            .insert({
                "source_id": source_id,
                "status": "pending",
                "started_at": now,
            })
            .execute()
        )

        # 更新 source 的 last_run 信息
        self.client.table(self.sources_table).update({
            "last_run_at": now,
            "last_status": "pending",
        }).eq("id", source_id).execute()

        return task_response.data[0]

    def update_task_status(
        self,
        task_id: str,
        status: str,
        records_count: int | None = None,
        error_message: str | None = None,
    ) -> dict:
        """更新任务状态"""
        # 获取任务
        task_response = (
            self.client.table(self.tasks_table)
            .select("*")
            .eq("id", task_id)
            .single()
            .execute()
        )
        task = task_response.data
        if not task:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlTask {task_id} not found")

        update_data: dict = {"status": status}
        if records_count is not None:
            update_data["records_count"] = records_count
        if error_message:
            update_data["error_message"] = error_message
        if status in ("success", "failed"):
            update_data["finished_at"] = datetime.utcnow().isoformat()

        # 更新任务
        response = (
            self.client.table(self.tasks_table)
            .update(update_data)
            .eq("id", task_id)
            .execute()
        )

        # 更新 source 的 last_status
        self.client.table(self.sources_table).update({
            "last_status": status,
        }).eq("id", task["source_id"]).execute()

        return response.data[0]
