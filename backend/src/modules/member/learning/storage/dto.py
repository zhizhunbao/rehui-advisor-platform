from pydantic import BaseModel
from datetime import datetime

from src.common.enum import FileType


class FileUploadResponse(BaseModel):
    id: str
    filename: str
    file_type: FileType
    size: int  # bytes
    path: str  # 存储路径
    url: str | None  # 下载 URL
    created_at: datetime

    class Config:
        from_attributes = True


class ConvertResponse(BaseModel):
    file_id: str
    markdown: str  # 转换后的 markdown 内容
    original_filename: str
