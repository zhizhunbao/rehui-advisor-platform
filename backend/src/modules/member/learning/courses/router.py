"""课程路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_user
from src.common.response import success_response
from .dto import CourseCreate, CourseUpdate
from .service import CourseService

router = APIRouter(prefix="/courses", tags=["learning-courses"])


@router.post("")
def create_course(data: CourseCreate, user: dict = Depends(get_current_user)):
    service = CourseService()
    course = service.create(user["id"], data)
    return success_response(course.model_dump())


@router.get("")
def list_courses(user: dict = Depends(get_current_user)):
    service = CourseService()
    courses = service.list(user["id"])
    return success_response([c.model_dump() for c in courses])


@router.get("/{id}")
def get_course(id: str, user: dict = Depends(get_current_user)):
    service = CourseService()
    course = service.get(id, user["id"])
    return success_response(course.model_dump())


@router.put("/{id}")
def update_course(id: str, data: CourseUpdate, user: dict = Depends(get_current_user)):
    service = CourseService()
    course = service.update(id, user["id"], data)
    return success_response(course.model_dump())


@router.delete("/{id}")
def delete_course(id: str, user: dict = Depends(get_current_user)):
    service = CourseService()
    service.delete(id, user["id"])
    return success_response(None)
