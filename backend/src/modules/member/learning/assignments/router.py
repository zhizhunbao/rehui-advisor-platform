"""Assignment 路由"""
from fastapi import APIRouter, Depends, Query

from src.common.auth import get_current_user
from src.common.response import success_response
from .dto import AssignmentCreate, AssignmentUpdate
from .service import AssignmentService

router = APIRouter(prefix="/assignments", tags=["learning-assignments"])


@router.post("")
def create_assignment(data: AssignmentCreate, user: dict = Depends(get_current_user)):
    service = AssignmentService()
    assignment = service.create(user["id"], data)
    return success_response(assignment.model_dump(mode="json"))


@router.get("")
def list_assignments(
    lab_id: str = Query(..., alias="labId"),
    user: dict = Depends(get_current_user),
):
    service = AssignmentService()
    assignments = service.list_by_lab(lab_id, user["id"])
    return success_response([a.model_dump(mode="json") for a in assignments])


@router.get("/{id}")
def get_assignment(id: str, user: dict = Depends(get_current_user)):
    service = AssignmentService()
    assignment = service.get(id, user["id"])
    return success_response(assignment.model_dump(mode="json"))


@router.put("/{id}")
def update_assignment(id: str, data: AssignmentUpdate, user: dict = Depends(get_current_user)):
    service = AssignmentService()
    assignment = service.update(id, user["id"], data)
    return success_response(assignment.model_dump(mode="json"))


@router.delete("/{id}")
def delete_assignment(id: str, user: dict = Depends(get_current_user)):
    service = AssignmentService()
    service.delete(id, user["id"])
    return success_response(None)
