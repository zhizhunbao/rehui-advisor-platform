"""文件存储服务"""
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.config import get_settings
from .dto import FileType, FileUploadResponse


DOC_TYPE = "learning_file"
UPLOAD_DIR = Path("uploads/learning")


class StorageService:
    def __init__(self) -> None:
        self.store = DocumentStore()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def upload(
        self,
        owner_id: str,
        filename: str,
        content: bytes,
        category: str = "general",  # labs, assignments, resources
    ) -> FileUploadResponse:
        file_id = str(uuid4())
        file_type = self._detect_file_type(filename)
        
        # 存储路径: uploads/learning/{owner_id}/{category}/{file_id}/{filename}
        file_dir = UPLOAD_DIR / owner_id / category / file_id
        file_dir.mkdir(parents=True, exist_ok=True)
        file_path = file_dir / filename
        
        # 写入文件
        file_path.write_bytes(content)
        
        # 保存元数据
        doc = self.store.create(
            DOC_TYPE,
            {
                "filename": filename,
                "file_type": file_type.value,
                "size": len(content),
                "path": str(file_path),
                "category": category,
            },
            owner_id=owner_id,
        )
        
        return self._to_response(doc)

    def get(self, file_id: str, owner_id: str) -> FileUploadResponse:
        doc = self.store.get(file_id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"File {file_id} not found")
        return self._to_response(doc)

    def get_content(self, file_id: str, owner_id: str) -> tuple[str, bytes]:
        """返回 (filename, content)"""
        doc = self.store.get(file_id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"File {file_id} not found")
        
        file_path = Path(doc["data"]["path"])
        if not file_path.exists():
            raise AppError(AppErrorCode.NOT_FOUND, "File content not found")
        
        return doc["data"]["filename"], file_path.read_bytes()

    def delete(self, file_id: str, owner_id: str) -> bool:
        doc = self.store.get(file_id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"File {file_id} not found")
        
        # 删除文件
        file_path = Path(doc["data"]["path"])
        if file_path.exists():
            file_path.unlink()
            # 尝试删除空目录
            try:
                file_path.parent.rmdir()
            except OSError:
                pass
        
        return self.store.delete(file_id)

    def list(self, owner_id: str, category: str | None = None) -> list[FileUploadResponse]:
        docs = self.store.find(DOC_TYPE, owner_id=owner_id, limit=1000)
        
        results = []
        for doc in docs:
            if category and doc["data"].get("category") != category:
                continue
            results.append(self._to_response(doc))
        
        return results

    def _detect_file_type(self, filename: str) -> FileType:
        ext = filename.lower().split(".")[-1] if "." in filename else ""
        mapping = {
            "docx": FileType.DOCX,
            "doc": FileType.DOCX,
            "pdf": FileType.PDF,
            "ipynb": FileType.NOTEBOOK,
            "md": FileType.MARKDOWN,
            "png": FileType.IMAGE,
            "jpg": FileType.IMAGE,
            "jpeg": FileType.IMAGE,
            "gif": FileType.IMAGE,
        }
        return mapping.get(ext, FileType.OTHER)

    def _to_response(self, doc: dict) -> FileUploadResponse:
        data = doc["data"]
        return FileUploadResponse(
            id=doc["id"],
            filename=data.get("filename"),
            file_type=FileType(data.get("file_type", "other")),
            size=data.get("size", 0),
            path=data.get("path"),
            url=f"/api/learning/storage/{doc['id']}/download",
            created_at=doc["created_at"],
        )
