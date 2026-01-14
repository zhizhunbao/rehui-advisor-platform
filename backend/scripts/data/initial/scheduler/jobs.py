# 调度任务种子数据
from typing import Any, Dict, List

SCHEDULER_JOBS: List[Dict[str, Any]] = [
    {
        "name": "每1分钟刷新数据源",
        "description": "每1分钟刷新所有 GitHub 数据源的元数据（stars、forks等）",
        "job_type": "refresh_data_sources",
        "cron_expression": "*/1 * * * *",
        "parameters": {},
        "is_active": True,
    },
    {
        "name": "每2分钟自动探索 - 求职",
        "description": "每2分钟自动探索求职领域的新资源",
        "job_type": "auto_discover",
        "cron_expression": "*/2 * * * *",
        "parameters": {
            "domain": "job",
            "limit_per_keyword": 2,
            "auto_import": False,
        },
        "is_active": True,
    },
    {
        "name": "每2分钟自动探索 - 教育",
        "description": "每2分钟自动探索教育领域的新资源（错开1分钟）",
        "job_type": "auto_discover",
        "cron_expression": "1-59/2 * * * *",
        "parameters": {
            "domain": "education",
            "limit_per_keyword": 2,
            "auto_import": False,
        },
        "is_active": True,
    },
    {
        "name": "每3分钟自动探索 - 投资",
        "description": "每3分钟自动探索投资领域的新资源",
        "job_type": "auto_discover",
        "cron_expression": "*/3 * * * *",
        "parameters": {
            "domain": "investment",
            "limit_per_keyword": 2,
            "auto_import": False,
        },
        "is_active": False,
    },
    {
        "name": "每5分钟清理旧执行记录",
        "description": "每5分钟清理1天前的任务执行记录（job_executions表）",
        "job_type": "cleanup_old_data",
        "cron_expression": "*/5 * * * *",
        "parameters": {
            "days": 1,
        },
        "is_active": True,
    },
    {
        "name": "每3分钟同步 LLM 模型",
        "description": "每3分钟同步一次 LLM 模型配置",
        "job_type": "sync_llm_models",
        "cron_expression": "*/3 * * * *",
        "parameters": {},
        "is_active": False,
    },
    {
        "name": "每3分钟同步 Prompts",
        "description": "每3分钟同步 Prompt 模板",
        "job_type": "sync_prompts",
        "cron_expression": "*/3 * * * *",
        "parameters": {},
        "is_active": False,
    },
    {
        "name": "每3分钟同步 Skills",
        "description": "每3分钟同步 Skills",
        "job_type": "sync_skills",
        "cron_expression": "*/3 * * * *",
        "parameters": {},
        "is_active": False,
    },
]
