from pydantic import BaseModel


class FrontendLogRequest(BaseModel):
    level: str  # debug, info, warn, error
    message: str
    layer: str | None = None  # component, hook, service, store, util
    url: str | None = None
    userAgent: str | None = None
    timestamp: str | None = None
    error: str | None = None
    stack: str | None = None
    caller: dict | None = None
