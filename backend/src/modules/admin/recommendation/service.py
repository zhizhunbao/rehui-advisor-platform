"""推荐方案管理服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.helper import paginate


DOC_TYPE = "admin_recommendation"


class RecommendationAdminService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        user_id: str | None = None,
        domain: str | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE, status="active")
        
        # 过滤
        recommendations = []
        for doc in docs:
            data = doc["data"]
            if user_id and data.get("user_id") != user_id:
                continue
            if domain and data.get("domain") != domain:
                continue
            recommendations.append(self._to_response(doc))
        
        # 排序
        recommendations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        paged, total = paginate(recommendations, page, limit)
        
        return paged, total

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def find_by_user(self, user_id: str, domain: str | None = None) -> list[dict]:
        docs = self.store.find(DOC_TYPE, status="active")
        
        recommendations = []
        for doc in docs:
            data = doc["data"]
            if data.get("user_id") != user_id:
                continue
            if domain and data.get("domain") != domain:
                continue
            recommendations.append(self._to_response(doc))
        
        # 按 ranking 排序
        recommendations.sort(key=lambda x: x.get("ranking", 0))
        return recommendations

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Recommendation {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return existing

        doc = self.store.update(id, data_updates=update_data)
        return self._to_response(doc)

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Recommendation {id} not found")
        self.store.delete(id)

    def delete_by_user(self, user_id: str) -> int:
        """删除用户的所有推荐"""
        docs = self.store.find(DOC_TYPE, status="active")
        deleted = 0
        for doc in docs:
            if doc["data"].get("user_id") == user_id:
                self.store.delete(doc["id"])
                deleted += 1
        return deleted

    def get_stats(self) -> dict:
        """获取推荐统计"""
        docs = self.store.find(DOC_TYPE, status="active")
        total = len(docs)

        # 按领域统计
        domain_counts: dict[str, int] = {}
        for doc in docs:
            domain = doc["data"].get("domain", "unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        return {
            "total": total,
            "by_domain": domain_counts,
        }

    def _to_response(self, doc: dict) -> dict:
        """转换为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "user_id": data.get("user_id"),
            "domain": data.get("domain"),
            "title": data.get("title"),
            "content": data.get("content"),
            "ranking": data.get("ranking"),
            "score": data.get("score"),
            "metadata": data.get("metadata", {}),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
