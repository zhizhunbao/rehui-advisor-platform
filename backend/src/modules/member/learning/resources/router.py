"""Resource 路由"""
from fastapi import APIRouter, Depends, Query

from src.common.auth import get_current_user
from src.common.response import success_response
from .dto import ResourceCreate, ResourceUpdate
from .service import ResourceService

router = APIRouter(prefix="/resources", tags=["learning-resources"])


@router.post("")
def create_resource(data: ResourceCreate, user: dict = Depends(get_current_user)):
    service = ResourceService()
    resource = service.create(user["id"], data)
    return success_response(resource.model_dump(mode="json"))


@router.get("")
def list_resources(
    course_id: str | None = Query(None, alias="courseId"),
    lab_id: str | None = Query(None, alias="labId"),
    user: dict = Depends(get_current_user),
):
    service = ResourceService()
    resources = service.list(user["id"], course_id=course_id, lab_id=lab_id)
    return success_response([r.model_dump(mode="json") for r in resources])


@router.get("/{id}")
def get_resource(id: str, user: dict = Depends(get_current_user)):
    service = ResourceService()
    resource = service.get(id, user["id"])
    return success_response(resource.model_dump(mode="json"))


@router.put("/{id}")
def update_resource(id: str, data: ResourceUpdate, user: dict = Depends(get_current_user)):
    service = ResourceService()
    resource = service.update(id, user["id"], data)
    return success_response(resource.model_dump(mode="json"))


@router.delete("/{id}")
def delete_resource(id: str, user: dict = Depends(get_current_user)):
    service = ResourceService()
    service.delete(id, user["id"])
    return success_response(None)
