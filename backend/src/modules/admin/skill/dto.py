"""Skills DTO"""
from pydantic import BaseModel


class UpdateSkillRequest(BaseModel):
    description: str
    content: str
    is_active: bool


class CreateCategoryLabelRequest(BaseModel):
    type: str
    code: str
    name: str
    name_en: str
    color: str
    icon: str
    sort_order: int
    is_active: bool


class UpdateCategoryLabelRequest(BaseModel):
    code: str
    name: str
    name_en: str
    color: str
    icon: str
    sort_order: int
    is_active: bool
