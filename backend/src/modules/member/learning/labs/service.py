"""Lab 服务"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import LabCreate, LabUpdate, LabResponse


DOC_TYPE = "learning_lab"


class LabService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def create(self, owner_id: str, data: LabCreate) -> LabResponse:
        doc = self.store.create(
            DOC_TYPE,
            data.model_dump(exclude_none=True, mode="json"),
            owner_id=owner_id,
        )
        return self._to_response(doc)

    def list_by_course(self, course_id: str, owner_id: str) -> list[LabResponse]:
        docs = self.store.find(DOC_TYPE, owner_id=owner_id, limit=1000)
        labs = [self._to_response(doc) for doc in docs if doc["data"].get("course_id") == course_id]
        return sorted(labs, key=lambda x: x.order)

    def get(self, id: str, owner_id: str) -> LabResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Lab {id} not found")
        return self._to_response(doc)

    def update(self, id: str, owner_id: str, data: LabUpdate) -> LabResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Lab {id} not found")
        
        updated = self.store.update(id, data.model_dump(exclude_none=True, mode="json"))
        return self._to_response(updated)

    def delete(self, id: str, owner_id: str) -> bool:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Lab {id} not found")
        return self.store.delete(id)

    def _to_response(self, doc: dict) -> LabResponse:
        data = doc["data"]
        return LabResponse(
            id=doc["id"],
            course_id=data.get("course_id"),
            title=data.get("title"),
            description=data.get("description"),
            instructions_md=data.get("instructions_md"),
            original_file_id=data.get("original_file_id"),
            due_date=data.get("due_date"),
            order=data.get("order", 0),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
