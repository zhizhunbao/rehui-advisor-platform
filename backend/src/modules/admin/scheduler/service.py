"""Scheduler 服务 - 使用 Document Store"""
from datetime import datetime, timezone, timedelta

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode


DOC_TYPE_JOB = "admin_scheduled_job"
DOC_TYPE_EXECUTION = "admin_job_execution"


# 预设任务类型
JOB_TYPES = [
    {
        "type": "refresh_data_sources",
        "name_zh": "刷新数据源",
        "name_en": "Refresh Data Sources",
        "description_zh": "刷新数据源元数据（GitHub stars、forks 等）",
        "description_en": "Refresh data source metadata (GitHub stars, forks, etc.)",
        "parameters_schema": {
            "category": {"type": "string", "required": False, "description": "Filter by category"},
        },
    },
    {
        "type": "auto_discover",
        "name_zh": "自动探索",
        "name_en": "Auto Discover",
        "description_zh": "自动探索指定领域的新资源",
        "description_en": "Auto discover new resources for specified domain",
        "parameters_schema": {
            "domain": {"type": "string", "required": True, "description": "Domain to discover"},
            "limit_per_keyword": {"type": "integer", "required": False, "default": 10},
            "auto_import": {"type": "boolean", "required": False, "default": False},
        },
    },
    {
        "type": "crawl_sources",
        "name_zh": "数据抓取",
        "name_en": "Crawl Sources",
        "description_zh": "执行数据源抓取任务",
        "description_en": "Execute data source crawling",
        "parameters_schema": {
            "source_ids": {"type": "array", "required": False, "description": "Specific source IDs to crawl"},
            "category": {"type": "string", "required": False},
        },
    },
    {
        "type": "sync_llm_models",
        "name_zh": "同步 LLM 模型",
        "name_en": "Sync LLM Models",
        "description_zh": "从配置同步 LLM 模型列表",
        "description_en": "Sync LLM models from configuration",
        "parameters_schema": {},
    },
    {
        "type": "sync_prompts",
        "name_zh": "同步 Prompts",
        "name_en": "Sync Prompts",
        "description_zh": "从外部源同步 Prompt 模板",
        "description_en": "Sync prompt templates from external sources",
        "parameters_schema": {},
    },
    {
        "type": "sync_skills",
        "name_zh": "同步 Skills",
        "name_en": "Sync Skills",
        "description_zh": "从外部源同步 Skills",
        "description_en": "Sync skills from external sources",
        "parameters_schema": {},
    },
    {
        "type": "cleanup_old_data",
        "name_zh": "清理旧数据",
        "name_en": "Cleanup Old Data",
        "description_zh": "清理过期的执行记录和临时数据",
        "description_en": "Cleanup expired execution records and temporary data",
        "parameters_schema": {
            "days": {"type": "integer", "required": False, "default": 30, "description": "Keep data for N days"},
        },
    },
]


class SchedulerService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    # ========== 任务类型 ==========
    def get_job_types(self) -> list[dict]:
        return JOB_TYPES

    # ========== 查询 ==========
    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        job_type: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_JOB, status="active")
        
        # 过滤
        jobs = []
        for doc in docs:
            data = doc["data"]
            if job_type and data.get("job_type") != job_type:
                continue
            if is_active is not None and data.get("is_active") != is_active:
                continue
            jobs.append(self._to_response(doc))
        
        # 排序
        jobs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        total = len(jobs)
        start = (page - 1) * limit
        end = start + limit
        
        return jobs[start:end], total

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_JOB or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    # ========== 创建 ==========
    def create(self, data: dict) -> dict:
        # 验证任务类型
        valid_types = [t["type"] for t in JOB_TYPES]
        if data.get("job_type") not in valid_types:
            raise AppError(
                AppErrorCode.VALIDATION_ERROR,
                f"Invalid job type: {data.get('job_type')}. Valid types: {valid_types}",
            )

        doc = self.store.create(DOC_TYPE_JOB, {
            "name": data["name"],
            "description": data.get("description", ""),
            "job_type": data["job_type"],
            "cron_expression": data["cron_expression"],
            "parameters": data.get("parameters", {}),
            "is_active": data.get("is_active", True),
            "last_run_at": None,
            "last_status": None,
        })
        
        return self._to_response(doc)

    # ========== 更新 ==========
    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Job {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        doc = self.store.update(id, data_updates=update_data)
        
        # 重新加载调度任务
        from src.modules.admin.scheduler.executor import reload_job
        reload_job(id)
        
        return self._to_response(doc)

    def toggle(self, id: str) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Job {id} not found")

        new_status = not existing.get("is_active", True)
        doc = self.store.update(id, data_updates={"is_active": new_status})
        
        # 重新加载调度任务
        from src.modules.admin.scheduler.executor import reload_job
        reload_job(id)
        
        return self._to_response(doc)

    # ========== 删除 ==========
    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Job {id} not found")
        self.store.delete(id)

    # ========== 手动触发 ==========
    def trigger(self, id: str) -> dict:
        job = self.find_by_id(id)
        if not job:
            raise AppError(AppErrorCode.NOT_FOUND, f"Job {id} not found")

        # 创建执行记录
        execution = self._create_execution(id)

        try:
            # 执行任务
            result = self._execute_job(job)

            # 更新执行记录为成功
            self._update_execution(
                execution["id"],
                status="success",
                result=result,
            )

            # 更新任务的最后执行信息
            self._update_job_last_run(id, "success")

            return {
                "execution_id": execution["id"],
                "status": "success",
                "result": result,
            }
        except Exception as e:
            # 更新执行记录为失败
            self._update_execution(
                execution["id"],
                status="failed",
                error_message=str(e),
            )

            # 更新任务的最后执行信息
            self._update_job_last_run(id, "failed")

            raise AppError(AppErrorCode.INTERNAL_ERROR, f"Job execution failed: {str(e)}")

    def _execute_job(self, job: dict) -> dict:
        """执行具体任务逻辑"""
        from src.common.logger import log_with_extra
        
        job_type = job["job_type"]
        parameters = job.get("parameters", {})
        job_name = job.get("name", job_type)

        log_with_extra("info", f"[Scheduler] Executing job: {job_name}", 
                      job_id=job["id"], job_type=job_type, parameters=parameters)

        if job_type == "refresh_data_sources":
            return self._execute_refresh_data_sources(job, parameters)
        elif job_type == "auto_discover":
            return self._execute_auto_discover(job, parameters)
        elif job_type == "crawl_sources":
            return self._execute_crawl_sources(job, parameters)
        elif job_type == "sync_llm_models":
            return self._execute_sync_llm_models(job, parameters)
        elif job_type == "sync_prompts":
            return self._execute_sync_prompts(job, parameters)
        elif job_type == "sync_skills":
            return self._execute_sync_skills(job, parameters)
        elif job_type == "cleanup_old_data":
            return self._execute_cleanup_old_data(job, parameters)
        else:
            return {"message": f"Unknown job type: {job_type}"}


    def _execute_refresh_data_sources(self, job: dict, parameters: dict) -> dict:
        from src.common.logger import log_with_extra
        from src.modules.admin.data_source.service import DataSourceService
        
        service = DataSourceService()
        category = parameters.get("category")
        
        log_with_extra("info", f"[Scheduler] Starting refresh data sources", 
                      job_id=job["id"], category=category or "all")
        
        result = service.refresh_all(category=category)
        
        refreshed = result.get("refreshed", 0)
        errors = result.get("errors", [])
        
        log_with_extra("info", f"[Scheduler] Refresh completed: {refreshed} refreshed, {len(errors)} errors",
                      job_id=job["id"], refreshed=refreshed, error_count=len(errors))
        
        if errors:
            for err in errors[:5]:
                log_with_extra("warn", f"[Scheduler] Refresh error: {err.get('url')} - {err.get('error')}",
                              job_id=job["id"], url=err.get("url"))
        
        return result

    def _execute_auto_discover(self, job: dict, parameters: dict) -> dict:
        from src.common.logger import log_with_extra
        from src.modules.admin.data_source.service import DataSourceService
        from src.common.supabase import get_supabase_admin
        
        service = DataSourceService()
        domain = parameters.get("domain")
        
        if not domain:
            log_with_extra("error", f"[Scheduler] Auto discover failed: domain is required",
                          job_id=job["id"])
            return {"error": "domain is required"}
        
        limit_per_keyword = parameters.get("limit_per_keyword", 10)
        auto_import = parameters.get("auto_import", False)
        
        log_with_extra("info", f"[Scheduler] Starting auto discover for domain: {domain}",
                      job_id=job["id"], domain=domain, limit_per_keyword=limit_per_keyword, auto_import=auto_import)
        
        result = service.auto_discover(
            domain=domain,
            limit_per_keyword=limit_per_keyword,
        )
        
        discovered_count = result.get("total", 0)
        strategies_used = result.get("strategies_used", [])
        
        strategy_summary = ", ".join([f"{s['strategy']}:{s['count']}" for s in strategies_used])
        
        log_with_extra("info", f"[Scheduler] Discovered {discovered_count} URLs via strategies: {strategy_summary}",
                      job_id=job["id"], domain=domain, discovered=discovered_count, strategies=strategies_used)
        
        new_count = sum(1 for r in result.get("results", []) if not r.get("already_exists"))
        existing_count = discovered_count - new_count
        
        log_with_extra("info", f"[Scheduler] Discovery breakdown: {new_count} new, {existing_count} already exist",
                      job_id=job["id"], domain=domain, new_count=new_count, existing_count=existing_count)
        
        if auto_import and result.get("results"):
            new_items = [r for r in result["results"] if not r.get("already_exists")]
            
            if new_items:
                client = get_supabase_admin()
                domain_info = client.table("domains").select("id, category_id").eq("code", domain).maybe_single().execute()
                category_id = domain_info.data.get("category_id") if domain_info.data else None
                domain_id = domain_info.data.get("id") if domain_info.data else None
                
                import_result = service.batch_import(
                    items=new_items,
                    category_id=category_id or "",
                    domain_id=domain_id or "",
                )
                result["import_result"] = import_result
                
                added = import_result.get("added", 0)
                skipped = import_result.get("skipped", 0)
                import_errors = len(import_result.get("errors", []))
                
                log_with_extra("info", f"[Scheduler] Auto import completed: {added} added, {skipped} skipped, {import_errors} errors",
                              job_id=job["id"], domain=domain, added=added, skipped=skipped, import_errors=import_errors)
            else:
                log_with_extra("info", f"[Scheduler] No new items to import",
                              job_id=job["id"], domain=domain)
                result["import_result"] = {"added": 0, "skipped": 0, "errors": []}
        
        return result

    def _execute_crawl_sources(self, job: dict, parameters: dict) -> dict:
        from src.common.logger import log_with_extra
        
        log_with_extra("info", f"[Scheduler] Crawl sources not implemented yet",
                      job_id=job["id"], parameters=parameters)
        return {"message": "Crawl sources not implemented yet", "parameters": parameters}

    def _execute_sync_llm_models(self, job: dict, parameters: dict) -> dict:
        from src.common.logger import log_with_extra
        
        log_with_extra("info", f"[Scheduler] Sync LLM models not implemented yet",
                      job_id=job["id"])
        return {"message": "Sync LLM models not implemented yet"}

    def _execute_sync_prompts(self, job: dict, parameters: dict) -> dict:
        from src.common.logger import log_with_extra
        
        log_with_extra("info", f"[Scheduler] Sync prompts not implemented yet",
                      job_id=job["id"])
        return {"message": "Sync prompts not implemented yet"}

    def _execute_sync_skills(self, job: dict, parameters: dict) -> dict:
        from src.common.logger import log_with_extra
        
        log_with_extra("info", f"[Scheduler] Sync skills not implemented yet",
                      job_id=job["id"])
        return {"message": "Sync skills not implemented yet"}

    def _execute_cleanup_old_data(self, job: dict, parameters: dict) -> dict:
        from src.common.logger import log_with_extra
        from src.common.supabase import get_supabase_admin
        
        days = parameters.get("days", 30)
        
        log_with_extra("info", f"[Scheduler] Starting cleanup old data (older than {days} days)",
                      job_id=job["id"], days=days)
        
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # 清理旧的执行记录 (从 documents 表)
            executions = self.store.find(DOC_TYPE_EXECUTION, status="active")
            deleted_executions = 0
            for exec_doc in executions:
                created_at = exec_doc.get("created_at", "")
                if created_at and created_at < cutoff_date.isoformat():
                    self.store.delete(exec_doc["id"], hard=True)
                    deleted_executions += 1
            
            # 清理旧的系统日志
            client = get_supabase_admin()
            logs_count_response = (
                client.table("system_logs")
                .select("id", count="exact")
                .lt("created_at", cutoff_date.isoformat())
                .execute()
            )
            logs_to_delete = logs_count_response.count or 0
            
            if logs_to_delete > 0:
                client.table("system_logs").delete().lt(
                    "created_at", cutoff_date.isoformat()
                ).execute()
            
            log_with_extra("info", f"[Scheduler] Cleanup completed: {deleted_executions} execution records, {logs_to_delete} logs deleted",
                          job_id=job["id"], days=days, executions_deleted=deleted_executions, logs_deleted=logs_to_delete)
            
            return {
                "message": f"Cleaned up records older than {days} days",
                "executions_deleted": deleted_executions,
                "logs_deleted": logs_to_delete,
            }
        except Exception as e:
            log_with_extra("error", f"[Scheduler] Cleanup failed: {str(e)}",
                          job_id=job["id"], error=str(e))
            raise

    # ========== 执行记录 ==========
    def _create_execution(self, job_id: str) -> dict:
        doc = self.store.create(DOC_TYPE_EXECUTION, {
            "job_id": job_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "status": "running",
            "finished_at": None,
            "result": None,
            "error_message": None,
        })
        return doc

    def _update_execution(
        self,
        execution_id: str,
        status: str,
        result: dict | None = None,
        error_message: str | None = None,
    ) -> None:
        update_data = {
            "status": status,
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        if result is not None:
            update_data["result"] = result
        if error_message is not None:
            update_data["error_message"] = error_message

        self.store.update(execution_id, data_updates=update_data)

    def _update_job_last_run(self, job_id: str, status: str) -> None:
        self.store.update(job_id, data_updates={
            "last_run_at": datetime.now(timezone.utc).isoformat(),
            "last_status": status,
        })

    def get_history(
        self,
        job_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[dict], int]:
        job = self.find_by_id(job_id)
        if not job:
            raise AppError(AppErrorCode.NOT_FOUND, f"Job {job_id} not found")

        docs = self.store.find(DOC_TYPE_EXECUTION, status="active")
        
        # 过滤指定 job 的执行记录
        executions = []
        for doc in docs:
            if doc["data"].get("job_id") == job_id:
                executions.append(self._execution_to_response(doc))
        
        # 排序
        executions.sort(key=lambda x: x.get("started_at", ""), reverse=True)
        
        # 分页
        total = len(executions)
        start = (page - 1) * limit
        end = start + limit
        
        return executions[start:end], total

    def get_logs(
        self,
        page: int = 1,
        limit: int = 50,
        level: str | None = None,
    ) -> tuple[list[dict], int]:
        """获取系统日志（调度相关）"""
        from src.common.supabase import get_supabase_admin
        
        client = get_supabase_admin()
        query = client.table("system_logs").select("*", count="exact")
        
        if level:
            query = query.eq("level", level)
        
        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)
        
        response = query.execute()
        return response.data, response.count or 0

    def _to_response(self, doc: dict) -> dict:
        """转换 job 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "name": data.get("name"),
            "description": data.get("description"),
            "job_type": data.get("job_type"),
            "cron_expression": data.get("cron_expression"),
            "parameters": data.get("parameters", {}),
            "is_active": data.get("is_active", True),
            "last_run_at": data.get("last_run_at"),
            "last_status": data.get("last_status"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }

    def _execution_to_response(self, doc: dict) -> dict:
        """转换 execution 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "job_id": data.get("job_id"),
            "started_at": data.get("started_at"),
            "finished_at": data.get("finished_at"),
            "status": data.get("status"),
            "result": data.get("result"),
            "error_message": data.get("error_message"),
            "created_at": doc.get("created_at"),
        }
