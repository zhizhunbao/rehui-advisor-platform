"""Lab 路由"""
from fastapi import APIRouter, Depends, Query

from src.common.auth import get_current_user
from src.common.response import success_response
from .dto import LabCreate, LabUpdate
from .service import LabService

router = APIRouter(prefix="/labs", tags=["learning-labs"])


@router.post("")
def create_lab(data: LabCreate, user: dict = Depends(get_current_user)):
    service = LabService()
    lab = service.create(user["id"], data)
    return success_response(lab.model_dump(mode="json"))


@router.get("")
def list_labs(
    course_id: str = Query(..., alias="courseId"),
    user: dict = Depends(get_current_user),
):
    service = LabService()
    labs = service.list_by_course(course_id, user["id"])
    return success_response([lab.model_dump(mode="json") for lab in labs])


@router.get("/{id}")
def get_lab(id: str, user: dict = Depends(get_current_user)):
    service = LabService()
    lab = service.get(id, user["id"])
    return success_response(lab.model_dump(mode="json"))


@router.put("/{id}")
def update_lab(id: str, data: LabUpdate, user: dict = Depends(get_current_user)):
    service = LabService()
    lab = service.update(id, user["id"], data)
    return success_response(lab.model_dump(mode="json"))


@router.delete("/{id}")
def delete_lab(id: str, user: dict = Depends(get_current_user)):
    service = LabService()
    service.delete(id, user["id"])
    return success_response(None)
