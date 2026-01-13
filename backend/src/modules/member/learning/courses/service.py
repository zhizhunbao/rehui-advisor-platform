"""课程服务"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from .dto import CourseCreate, CourseUpdate, CourseResponse


DOC_TYPE = "learning_course"


class CourseService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def create(self, owner_id: str, data: CourseCreate) -> CourseResponse:
        doc = self.store.create(
            DOC_TYPE,
            data.model_dump(exclude_none=True),
            owner_id=owner_id,
        )
        return self._to_response(doc)

    def list(self, owner_id: str) -> list[CourseResponse]:
        docs = self.store.find(DOC_TYPE, owner_id=owner_id)
        return [self._to_response(doc) for doc in docs]

    def get(self, id: str, owner_id: str) -> CourseResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Course {id} not found")
        return self._to_response(doc)

    def update(self, id: str, owner_id: str, data: CourseUpdate) -> CourseResponse:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Course {id} not found")
        
        updated = self.store.update(id, data.model_dump(exclude_none=True))
        return self._to_response(updated)

    def delete(self, id: str, owner_id: str) -> bool:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["owner_id"] != owner_id:
            raise AppError(AppErrorCode.NOT_FOUND, f"Course {id} not found")
        return self.store.delete(id)

    def _to_response(self, doc: dict) -> CourseResponse:
        data = doc["data"]
        return CourseResponse(
            id=doc["id"],
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description"),
            semester=data.get("semester"),
            instructor=data.get("instructor"),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
