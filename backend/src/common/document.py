"""
Document Store 模式 - 极简灵活的数据存储

使用 Supabase 的 documents 表存储所有业务数据：
- 最少的结构化字段（id, type, timestamps）
- 所有业务数据存储在 data 字段（JSONB）
- 可选的系统级字段用于跨实体查询

使用示例：
    from src.common.document import DocumentStore
    
    store = DocumentStore()
    
    # 创建
    user = store.create("user", {"username": "john", "email": "john@example.com"})
    
    # 查询
    users = store.find("user", {"data->username": "john"})
    
    # 更新
    store.update(user["id"], {"email": "new@example.com"})
    
    # 删除
    store.delete(user["id"])
"""
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from src.common.supabase import get_supabase_admin
from src.common.errors import AppError, AppErrorCode


class DocumentStore:
    """通用文档存储服务"""
    
    TABLE = "documents"
    
    def __init__(self):
        self.client = get_supabase_admin()
    
    def create(
        self,
        doc_type: str,
        data: dict[str, Any],
        owner_id: Optional[str] = None,
        status: str = "active",
        tags: Optional[list[str]] = None,
    ) -> dict:
        """创建文档"""
        doc = {
            "id": str(uuid4()),
            "type": doc_type,
            "data": data,
            "owner_id": owner_id,
            "status": status,
            "tags": tags or [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        
        response = self.client.table(self.TABLE).insert(doc).execute()
        
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create document")
        
        return response.data[0]
    
    def get(self, doc_id: str) -> Optional[dict]:
        """根据 ID 获取文档"""
        response = (
            self.client.table(self.TABLE)
            .select("*")
            .eq("id", doc_id)
            .maybe_single()
            .execute()
        )
        return response.data
    
    def find(
        self,
        doc_type: str,
        filters: Optional[dict[str, Any]] = None,
        status: Optional[str] = "active",
        owner_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "created_at",
        ascending: bool = False,
    ) -> list[dict]:
        """查询文档列表"""
        query = self.client.table(self.TABLE).select("*").eq("type", doc_type)
        
        if status:
            query = query.eq("status", status)
        
        if owner_id:
            query = query.eq("owner_id", owner_id)
        
        # 处理 data 字段的过滤条件
        # Supabase 使用 data->key 语法（不是 data->>key）
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        
        query = query.order(order_by, desc=not ascending)
        query = query.range(offset, offset + limit - 1)
        
        response = query.execute()
        return response.data or []
    
    def find_one(
        self,
        doc_type: str,
        filters: Optional[dict[str, Any]] = None,
        status: Optional[str] = "active",
    ) -> Optional[dict]:
        """查询单个文档"""
        results = self.find(doc_type, filters, status, limit=1)
        return results[0] if results else None
    
    def update(
        self,
        doc_id: str,
        data_updates: Optional[dict[str, Any]] = None,
        status: Optional[str] = None,
        tags: Optional[list[str]] = None,
        merge: bool = True,
    ) -> Optional[dict]:
        """更新文档"""
        doc = self.get(doc_id)
        if not doc:
            return None
        
        updates = {"updated_at": datetime.now(timezone.utc).isoformat()}
        
        if data_updates:
            if merge:
                updates["data"] = {**doc["data"], **data_updates}
            else:
                updates["data"] = data_updates
        
        if status is not None:
            updates["status"] = status
        
        if tags is not None:
            updates["tags"] = tags
        
        response = (
            self.client.table(self.TABLE)
            .update(updates)
            .eq("id", doc_id)
            .execute()
        )
        
        return response.data[0] if response.data else None
    
    def delete(self, doc_id: str, hard: bool = False) -> bool:
        """删除文档（默认软删除）"""
        if hard:
            response = (
                self.client.table(self.TABLE)
                .delete()
                .eq("id", doc_id)
                .execute()
            )
        else:
            response = (
                self.client.table(self.TABLE)
                .update({
                    "status": "deleted",
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                })
                .eq("id", doc_id)
                .execute()
            )
        
        return bool(response.data)
    
    def count(
        self,
        doc_type: str,
        status: Optional[str] = "active",
        owner_id: Optional[str] = None,
    ) -> int:
        """统计文档数量"""
        query = (
            self.client.table(self.TABLE)
            .select("id", count="exact")
            .eq("type", doc_type)
        )
        
        if status:
            query = query.eq("status", status)
        
        if owner_id:
            query = query.eq("owner_id", owner_id)
        
        response = query.execute()
        return response.count or 0
    
    def add_tag(self, doc_id: str, tag: str) -> Optional[dict]:
        """添加标签"""
        doc = self.get(doc_id)
        if not doc:
            return None
        
        tags = doc.get("tags") or []
        if tag not in tags:
            tags.append(tag)
            return self.update(doc_id, tags=tags)
        
        return doc
    
    def remove_tag(self, doc_id: str, tag: str) -> Optional[dict]:
        """移除标签"""
        doc = self.get(doc_id)
        if not doc:
            return None
        
        tags = doc.get("tags") or []
        if tag in tags:
            tags.remove(tag)
            return self.update(doc_id, tags=tags)
        
        return doc
