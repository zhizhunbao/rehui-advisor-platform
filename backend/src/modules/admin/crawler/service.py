"""抓取源管理服务 - 使用 Document Store"""
from datetime import datetime, timezone

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.helper import paginate


DOC_TYPE_SOURCE = "admin_crawl_source"
DOC_TYPE_TASK = "admin_crawl_task"


class CrawlerService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    # ========== CrawlSource CRUD ==========
    def find_all_sources(
        self,
        page: int = 1,
        limit: int = 20,
        domain_id: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_SOURCE, status="active")
        
        # 过滤
        sources = []
        for doc in docs:
            data = doc["data"]
            if domain_id and data.get("domain_id") != domain_id:
                continue
            if is_active is not None and data.get("is_active") != is_active:
                continue
            sources.append(self._source_to_response(doc))
        
        # 排序
        sources.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        paged, total = paginate(sources, page, limit)
        
        return paged, total

    def find_source_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_SOURCE or doc["status"] == "deleted":
            return None
        return self._source_to_response(doc)

    def create_source(self, data: dict) -> dict:
        doc = self.store.create(DOC_TYPE_SOURCE, {
            "name": data.get("name"),
            "url": data.get("url"),
            "domain_id": data.get("domain_id"),
            "crawl_type": data.get("crawl_type"),
            "config": data.get("config", {}),
            "is_active": data.get("is_active", True),
            "last_run_at": None,
            "last_status": None,
        })
        return self._source_to_response(doc)

    def update_source(self, id: str, data: dict) -> dict:
        existing = self.find_source_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        doc = self.store.update(id, data_updates=update_data)
        return self._source_to_response(doc)

    def delete_source(self, id: str) -> None:
        existing = self.find_source_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {id} not found")
        self.store.delete(id)

    def toggle_source_status(self, id: str) -> dict:
        existing = self.find_source_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {id} not found")

        new_status = not existing.get("is_active", True)
        doc = self.store.update(id, data_updates={"is_active": new_status})
        return self._source_to_response(doc)

    # ========== CrawlTask Management ==========
    def find_tasks_by_source(
        self,
        source_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_TASK, status="active")
        
        # 过滤指定 source 的任务
        tasks = []
        for doc in docs:
            if doc["data"].get("source_id") == source_id:
                tasks.append(self._task_to_response(doc))
        
        # 排序
        tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        paged, total = paginate(tasks, page, limit)
        
        return paged, total

    def find_all_tasks(
        self,
        page: int = 1,
        limit: int = 20,
        status: str | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_TASK, status="active")
        
        # 过滤
        tasks = []
        for doc in docs:
            data = doc["data"]
            if status and data.get("status") != status:
                continue
            tasks.append(self._task_to_response(doc))
        
        # 排序
        tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        paged, total = paginate(tasks, page, limit)
        
        return paged, total

    def trigger_crawl(self, source_id: str) -> dict:
        """触发抓取任务"""
        source = self.find_source_by_id(source_id)
        if not source:
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlSource {source_id} not found")
        if not source.get("is_active"):
            raise AppError(AppErrorCode.VALIDATION_ERROR, "Cannot trigger inactive source")

        now = datetime.now(timezone.utc).isoformat()

        # 创建任务
        task_doc = self.store.create(DOC_TYPE_TASK, {
            "source_id": source_id,
            "status": "pending",
            "started_at": now,
            "finished_at": None,
            "records_count": None,
            "error_message": None,
        })

        # 更新 source 的最后运行信息
        self.store.update(source_id, data_updates={
            "last_run_at": now,
            "last_status": "pending",
        })

        return self._task_to_response(task_doc)

    def update_task_status(
        self,
        task_id: str,
        status: str,
        records_count: int | None = None,
        error_message: str | None = None,
    ) -> dict:
        """更新任务状态"""
        doc = self.store.get(task_id)
        if not doc or doc["type"] != DOC_TYPE_TASK or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, f"CrawlTask {task_id} not found")

        update_data: dict = {"status": status}
        if records_count is not None:
            update_data["records_count"] = records_count
        if error_message:
            update_data["error_message"] = error_message
        if status in ("success", "failed"):
            update_data["finished_at"] = datetime.now(timezone.utc).isoformat()

        task_doc = self.store.update(task_id, data_updates=update_data)

        # 更新 source 的状态
        source_id = doc["data"].get("source_id")
        if source_id:
            self.store.update(source_id, data_updates={"last_status": status})

        return self._task_to_response(task_doc)

    def _source_to_response(self, doc: dict) -> dict:
        """转换 source 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "name": data.get("name"),
            "url": data.get("url"),
            "domain_id": data.get("domain_id"),
            "crawl_type": data.get("crawl_type"),
            "config": data.get("config", {}),
            "is_active": data.get("is_active", True),
            "last_run_at": data.get("last_run_at"),
            "last_status": data.get("last_status"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }

    def _task_to_response(self, doc: dict) -> dict:
        """转换 task 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "source_id": data.get("source_id"),
            "status": data.get("status"),
            "started_at": data.get("started_at"),
            "finished_at": data.get("finished_at"),
            "records_count": data.get("records_count"),
            "error_message": data.get("error_message"),
            "created_at": doc.get("created_at"),
        }
