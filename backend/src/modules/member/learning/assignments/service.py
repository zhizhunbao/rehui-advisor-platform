"""Assignment 服务"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import AssignmentCreate, AssignmentUpdate, AssignmentResponse, AssignmentStatus


DOC_TYPE = "learning_assignment"


class AssignmentService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def create(self, owner_id: str, data: AssignmentCreate) -> AssignmentResponse:
        doc_data = data.model_dump(exclude_none=True)
        doc_data["status"] = AssignmentStatus.NOT_STARTED.value
        
        doc = self.store.create(DOC_TYPE, doc_data, owner_id=owner_id)
        return self._to_response(doc)

    def list_by_lab(self, lab_id: str, owner_id: str) -> list[AssignmentResponse]:
        docs = self.store.find(DOC_TYPE, owner_id=owner_id, limit=1000)
        return [self._to_response(doc) for doc in docs if doc["data"].get("lab_id") == lab_id]

    def get(self, id: str, owner_id: str) -> AssignmentResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Assignment {id} not found")
        return self._to_response(doc)

    def update(self, id: str, owner_id: str, data: AssignmentUpdate) -> AssignmentResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Assignment {id} not found")
        
        update_data = data.model_dump(exclude_none=True)
        if "status" in update_data:
            update_data["status"] = update_data["status"].value
        
        updated = self.store.update(id, update_data)
        return self._to_response(updated)

    def delete(self, id: str, owner_id: str) -> bool:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Assignment {id} not found")
        return self.store.delete(id)

    def _to_response(self, doc: dict) -> AssignmentResponse:
        data = doc["data"]
        return AssignmentResponse(
            id=doc["id"],
            lab_id=data.get("lab_id"),
            title=data.get("title"),
            notebook_file_id=data.get("notebook_file_id"),
            notes=data.get("notes"),
            status=AssignmentStatus(data.get("status", "not_started")),
            score=data.get("score"),
            feedback=data.get("feedback"),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
