"""系统配置管理 DTO"""
from pydantic import BaseModel


class CreateConfigRequest(BaseModel):
    key: str
    value: str | int | float | bool | dict | list
    description: str | None = None
    category: str = "general"
    is_sensitive: bool = False


class UpdateConfigRequest(BaseModel):
    key: str | None = None
    value: str | int | float | bool | dict | list | None = None
    description: str | None = None
    category: str | None = None
    is_sensitive: bool | None = None


class UpdateValueRequest(BaseModel):
    value: str | int | float | bool | dict | list
