"""Domain DTO"""
from pydantic import BaseModel


# ========== Domain Category ==========
class CreateDomainCategoryRequest(BaseModel):
    code: str
    name: str
    name_en: str
    description: str
    description_en: str
    icon: str
    color: str
    sort_order: int


class UpdateDomainCategoryRequest(BaseModel):
    name: str | None = None
    name_en: str | None = None
    description: str | None = None
    description_en: str | None = None
    icon: str | None = None
    color: str | None = None
    is_active: bool | None = None
    sort_order: int | None = None


# ========== Domain ==========
class CreateDomainRequest(BaseModel):
    code: str
    name: str
    name_en: str
    description: str
    description_en: str
    icon: str
    color: str
    prompt: str
    prompt_en: str
    category_id: str
    sort_order: int


class UpdateDomainRequest(BaseModel):
    name: str | None = None
    name_en: str | None = None
    description: str | None = None
    description_en: str | None = None
    icon: str | None = None
    color: str | None = None
    prompt: str | None = None
    prompt_en: str | None = None
    category_id: str | None = None
    is_active: bool | None = None
    sort_order: int | None = None


# ========== Question ==========
class QuestionOptionDto(BaseModel):
    text: str
    text_en: str
    value: str


class CreateQuestionRequest(BaseModel):
    domain_id: str
    text: str
    text_en: str
    type: str
    options: list[QuestionOptionDto] | None = None
    sort_order: int
