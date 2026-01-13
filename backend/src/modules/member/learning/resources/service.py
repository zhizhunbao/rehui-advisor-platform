"""Resource 服务"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import ResourceCreate, ResourceUpdate, ResourceResponse, ResourceType


DOC_TYPE = "learning_resource"


class ResourceService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def create(self, owner_id: str, data: ResourceCreate) -> ResourceResponse:
        doc_data = data.model_dump(exclude_none=True)
        doc_data["type"] = doc_data["type"].value
        
        doc = self.store.create(DOC_TYPE, doc_data, owner_id=owner_id)
        return self._to_response(doc)

    def list(
        self,
        owner_id: str,
        course_id: str | None = None,
        lab_id: str | None = None,
    ) -> list[ResourceResponse]:
        docs = self.store.find(DOC_TYPE, owner_id=owner_id, limit=1000)
        
        results = []
        for doc in docs:
            data = doc["data"]
            if course_id and data.get("course_id") != course_id:
                continue
            if lab_id and data.get("lab_id") != lab_id:
                continue
            results.append(self._to_response(doc))
        
        return results

    def get(self, id: str, owner_id: str) -> ResourceResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Resource {id} not found")
        return self._to_response(doc)

    def update(self, id: str, owner_id: str, data: ResourceUpdate) -> ResourceResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Resource {id} not found")
        
        update_data = data.model_dump(exclude_none=True)
        if "type" in update_data:
            update_data["type"] = update_data["type"].value
        
        updated = self.store.update(id, update_data)
        return self._to_response(updated)

    def delete(self, id: str, owner_id: str) -> bool:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Resource {id} not found")
        return self.store.delete(id)

    def _to_response(self, doc: dict) -> ResourceResponse:
        data = doc["data"]
        return ResourceResponse(
            id=doc["id"],
            url=data.get("url"),
            title=data.get("title"),
            description=data.get("description"),
            type=ResourceType(data.get("type", "link")),
            course_id=data.get("course_id"),
            lab_id=data.get("lab_id"),
            cached_content=data.get("cached_content"),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
