"""管理员路由 - 使用 Supabase API"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import (
    CreateDomainCategoryRequest,
    CreateDomainRequest,
    CreatePromptRequest,
    CreateQuestionRequest,
    UpdateDomainCategoryRequest,
    UpdateDomainRequest,
    UpdatePromptRequest,
)
from .service import (
    AnalyticsService,
    DomainCategoryService,
    DomainService,
    PromptService,
    QuestionService,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)


# ========== Domain Category Routes ==========
@router.get("/domain-categories")
def get_domain_categories():
    service = DomainCategoryService()
    categories = service.find_all()
    return success_response(categories)


@router.get("/domain-categories/{id}")
def get_domain_category(id: str):
    service = DomainCategoryService()
    category = service.find_by_id(id)
    return success_response(category)


@router.post("/domain-categories")
def create_domain_category(data: CreateDomainCategoryRequest):
    service = DomainCategoryService()
    category = service.create(data.model_dump())
    return success_response(category)


@router.put("/domain-categories/{id}")
def update_domain_category(id: str, data: UpdateDomainCategoryRequest):
    service = DomainCategoryService()
    category = service.update(id, data.model_dump())
    return success_response(category)


@router.delete("/domain-categories/{id}")
def delete_domain_category(id: str):
    service = DomainCategoryService()
    service.delete(id)
    return success_response(None)


# ========== Domain Routes ==========
@router.get("/domains")
def get_domains(category_id: str | None = None):
    service = DomainService()
    domains = service.find_all(category_id)
    return success_response(domains)


@router.get("/domains/{id}")
def get_domain(id: str):
    service = DomainService()
    domain = service.find_by_id(id)
    return success_response(domain)


@router.post("/domains")
def create_domain(data: CreateDomainRequest):
    service = DomainService()
    domain = service.create(data.model_dump())
    return success_response(domain)


@router.put("/domains/{id}")
def update_domain(id: str, data: UpdateDomainRequest):
    service = DomainService()
    domain = service.update(id, data.model_dump())
    return success_response(domain)


@router.delete("/domains/{id}")
def delete_domain(id: str):
    service = DomainService()
    service.delete(id)
    return success_response(None)


# ========== Prompt Routes ==========
@router.get("/prompts")
def get_prompts():
    service = PromptService()
    prompts = service.find_all()
    return success_response(prompts)


@router.get("/prompts/{id}")
def get_prompt(id: str):
    service = PromptService()
    prompt = service.find_by_id(id)
    return success_response(prompt)


@router.post("/prompts")
def create_prompt(data: CreatePromptRequest):
    service = PromptService()
    prompt = service.create(data.model_dump())
    return success_response(prompt)


@router.put("/prompts/{id}")
def update_prompt(id: str, data: UpdatePromptRequest):
    service = PromptService()
    prompt = service.update(id, data.model_dump())
    return success_response(prompt)


@router.delete("/prompts/{id}")
def delete_prompt(id: str):
    service = PromptService()
    service.delete(id)
    return success_response(None)


# ========== Question Routes ==========
@router.get("/questions")
def get_questions(domain_id: str | None = None):
    service = QuestionService()
    questions = service.find_all(domain_id)
    return success_response(questions)


@router.post("/questions")
def create_question(data: CreateQuestionRequest):
    service = QuestionService()
    question_data = {
        "domain_id": data.domain_id,
        "text": data.text,
        "text_en": data.text_en,
        "type": data.type,
        "options": [o.model_dump() for o in data.options] if data.options else None,
        "sort_order": data.sort_order,
    }
    question = service.create(question_data)
    return success_response(question)


@router.delete("/questions/{id}")
def delete_question(id: str):
    service = QuestionService()
    service.delete(id)
    return success_response(None)


# ========== Analytics Routes ==========
@router.get("/analytics/summary")
def get_analytics_summary():
    service = AnalyticsService()
    summary = service.get_summary()
    return success_response(summary)
