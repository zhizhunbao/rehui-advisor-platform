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

    return _logger


logger = setup_logger()


def log_with_extra(level: str, message: str, module: str = "app", **kwargs: Any) -> None:
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
