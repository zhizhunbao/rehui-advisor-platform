from enum import Enum
from typing import Any


class AppErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    DUPLICATE = "DUPLICATE"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"


STATUS_CODE_MAP: dict[AppErrorCode, int] = {
    AppErrorCode.NOT_FOUND: 404,
    AppErrorCode.VALIDATION_ERROR: 400,
    AppErrorCode.UNAUTHORIZED: 401,
    AppErrorCode.FORBIDDEN: 403,
    AppErrorCode.DUPLICATE: 409,
    AppErrorCode.INTERNAL_ERROR: 500,
    AppErrorCode.EXTERNAL_SERVICE_ERROR: 502,
    AppErrorCode.CONFIGURATION_ERROR: 500,
}


class AppError(Exception):
    def __init__(
        self,
        code: AppErrorCode,
        message: str,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details
        self.status_code = STATUS_CODE_MAP.get(code, 500)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code.value, "message": self.message}
        if self.details:
            result["details"] = self.details
        return result
