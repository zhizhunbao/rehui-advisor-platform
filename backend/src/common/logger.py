import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from src.common.config import get_settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, ensure_ascii=False)


class DatabaseHandler(logging.Handler):
    """将日志写入数据库的 Handler"""
    
    def __init__(self, modules_filter: list[str] | None = None):
        super().__init__()
        self.modules_filter = modules_filter or ["scheduler", "executor"]
    
    def emit(self, record: logging.LogRecord) -> None:
        # 只记录特定模块的日志到数据库
        module = getattr(record, "module", "") or ""
        message = record.getMessage()
        
        # 检查是否是调度相关的日志
        is_scheduler_log = (
            module in self.modules_filter or 
            "[Scheduler]" in message or
            "scheduler" in module.lower()
        )
        
        if not is_scheduler_log:
            return
        
        try:
            from src.common.supabase import get_supabase_admin
            client = get_supabase_admin()
            
            extra = {}
            if hasattr(record, "extra_data"):
                extra = record.extra_data
            
            client.table("system_logs").insert({
                "level": record.levelname.lower(),
                "module": module or "scheduler",
                "message": message,
                "extra": extra,
            }).execute()
        except Exception:
            # 忽略数据库写入错误，避免死循环
            pass


def setup_logger() -> logging.Logger:
    settings = get_settings()
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(exist_ok=True)

    _logger = logging.getLogger("app")
    _logger.setLevel(getattr(logging, settings.log_level.upper()))
    _logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JsonFormatter())
    _logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())
    _logger.addHandler(file_handler)

    # Database handler (只记录调度相关日志)
    db_handler = DatabaseHandler()
    db_handler.setLevel(logging.INFO)
    _logger.addHandler(db_handler)

    return _logger


logger = setup_logger()


def log_with_extra(level: str, message: str, module: str = "scheduler", **kwargs: Any) -> None:
    record = logger.makeRecord(
        logger.name,
        getattr(logging, level.upper()),
        "",
        0,
        message,
        (),
        None,
    )
    record.module = module  # type: ignore
    record.extra_data = kwargs  # type: ignore
    logger.handle(record)
