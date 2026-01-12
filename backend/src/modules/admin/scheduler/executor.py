"""调度执行器 - 使用 APScheduler 实现真正的定时调度"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timezone

from src.common.logger import log_with_extra
from src.common.supabase import get_supabase_admin

# 全局调度器实例
_scheduler: BackgroundScheduler | None = None


def get_scheduler() -> BackgroundScheduler:
    """获取调度器单例"""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
    return _scheduler


def execute_job(job_id: str) -> None:
    """执行单个任务"""
    from src.modules.admin.scheduler.service import SchedulerService
    
    try:
        service = SchedulerService()
        job = service.find_by_id(job_id)
        
        if not job:
            log_with_extra("warn", f"[Scheduler] Job {job_id} not found", job_id=job_id)
            return
        
        if not job.get("is_active"):
            log_with_extra("info", f"[Scheduler] Job '{job['name']}' is disabled, skipping", 
                          job_id=job_id, job_name=job["name"])
            return
        
        log_with_extra("info", f"[Scheduler] Starting job: {job['name']}", 
                      job_id=job_id, job_name=job["name"], job_type=job["job_type"])
        
        result = service.trigger(job_id)
        
        log_with_extra("info", f"[Scheduler] Job completed: {job['name']} - {result.get('status')}", 
                      job_id=job_id, job_name=job["name"], status=result.get("status"),
                      execution_id=result.get("execution_id"))
        
    except Exception as e:
        log_with_extra("error", f"[Scheduler] Job execution failed: {job_id} - {str(e)}", 
                      job_id=job_id, error=str(e))


def parse_cron_expression(cron_expr: str) -> dict:
    """解析 cron 表达式为 APScheduler 参数"""
    parts = cron_expr.strip().split()
    
    if len(parts) != 5:
        raise ValueError(f"Invalid cron expression: {cron_expr}")
    
    minute, hour, day, month, day_of_week = parts
    
    return {
        "minute": minute,
        "hour": hour,
        "day": day,
        "month": month,
        "day_of_week": day_of_week,
    }


def load_jobs_from_db() -> None:
    """从数据库加载所有启用的任务到调度器"""
    scheduler = get_scheduler()
    client = get_supabase_admin()
    
    # 清除现有任务
    scheduler.remove_all_jobs()
    
    # 获取所有启用的任务
    response = (
        client.table("scheduled_jobs")
        .select("*")
        .eq("is_active", True)
        .execute()
    )
    
    jobs = response.data or []
    log_with_extra("info", f"[Scheduler] Loading {len(jobs)} active jobs from database")
    
    for job in jobs:
        try:
            cron_params = parse_cron_expression(job["cron_expression"])
            trigger = CronTrigger(**cron_params)
            
            scheduler.add_job(
                execute_job,
                trigger=trigger,
                args=[job["id"]],
                id=job["id"],
                name=job["name"],
                replace_existing=True,
            )
            
            # 计算下次执行时间并更新数据库
            next_run = trigger.get_next_fire_time(None, datetime.now(timezone.utc))
            if next_run:
                client.table("scheduled_jobs").update({
                    "next_run_at": next_run.isoformat()
                }).eq("id", job["id"]).execute()
            
            log_with_extra("info", f"[Scheduler] Loaded job: {job['name']} (cron: {job['cron_expression']}, next: {next_run})",
                          job_id=job["id"], job_name=job["name"], cron=job["cron_expression"])
            
        except Exception as e:
            log_with_extra("error", f"[Scheduler] Failed to load job '{job['name']}': {str(e)}",
                          job_id=job["id"], error=str(e))


def reload_job(job_id: str) -> None:
    """重新加载单个任务"""
    scheduler = get_scheduler()
    client = get_supabase_admin()
    
    # 先移除现有任务
    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass
    
    # 获取任务信息
    response = (
        client.table("scheduled_jobs")
        .select("*")
        .eq("id", job_id)
        .maybe_single()
        .execute()
    )
    
    job = response.data
    if not job or not job.get("is_active"):
        return
    
    try:
        cron_params = parse_cron_expression(job["cron_expression"])
        trigger = CronTrigger(**cron_params)
        
        scheduler.add_job(
            execute_job,
            trigger=trigger,
            args=[job["id"]],
            id=job["id"],
            name=job["name"],
            replace_existing=True,
        )
        
        # 更新下次执行时间
        next_run = trigger.get_next_fire_time(None, datetime.now(timezone.utc))
        if next_run:
            client.table("scheduled_jobs").update({
                "next_run_at": next_run.isoformat()
            }).eq("id", job["id"]).execute()
            
    except Exception as e:
        log_with_extra("error", f"Failed to reload job {job_id}: {str(e)}")


def start_scheduler() -> None:
    """启动调度器"""
    scheduler = get_scheduler()
    
    if scheduler.running:
        log_with_extra("info", "Scheduler already running")
        return
    
    load_jobs_from_db()
    scheduler.start()
    log_with_extra("info", "Scheduler started")


def stop_scheduler() -> None:
    """停止调度器"""
    scheduler = get_scheduler()
    
    if scheduler.running:
        scheduler.shutdown(wait=False)
        log_with_extra("info", "Scheduler stopped")
