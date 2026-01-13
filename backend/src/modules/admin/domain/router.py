"""领域配置路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import (
    CreateDomainCategoryRequest,
    CreateDomainRequest,
    CreateQuestionRequest,
    UpdateDomainCategoryRequest,
    UpdateDomainRequest,
)
from .service import DomainCategoryService, DomainService, ProductLineService, QuestionService

router = APIRouter(prefix="/domains", tags=["domains"])


# ========== Product Line Routes ==========
@router.get("/product-lines")
def get_product_lines():
    """获取所有产品线"""
    service = ProductLineService()
    items = service.find_active()
    return success_response(items)


@router.get("/product-lines/{code}")
def get_product_line_by_code(code: str):
    """根据 code 获取产品线"""
    service = ProductLineService()
    item = service.find_by_code(code)
    return success_response(item)


# ========== Domain Category Routes ==========
@router.get("/categories")
def get_domain_categories(product_line_id: str | None = None):
    service = DomainCategoryService()
    categories = service.find_all(product_line_id)
    return success_response(categories)


@router.get("/categories/active")
def get_active_domain_categories(product_line_id: str | None = None):
    service = DomainCategoryService()
    categories = service.find_active(product_line_id)
    return success_response(categories)


@router.get("/categories/{id}")
def get_domain_category(id: str):
    service = DomainCategoryService()
    category = service.find_by_id(id)
    return success_response(category)


@router.post("/categories", dependencies=[Depends(get_current_admin)])
def create_domain_category(data: CreateDomainCategoryRequest):
    service = DomainCategoryService()
    category = service.create(data.model_dump())
    return success_response(category)


@router.put("/categories/{id}", dependencies=[Depends(get_current_admin)])
def update_domain_category(id: str, data: UpdateDomainCategoryRequest):
    service = DomainCategoryService()
    category = service.update(id, data.model_dump(exclude_none=True))
    return success_response(category)


@router.delete("/categories/{id}", dependencies=[Depends(get_current_admin)])
def delete_domain_category(id: str):
    service = DomainCategoryService()
    service.delete(id)
    return success_response(None)


# ========== Domain Routes ==========
@router.get("/")
def get_domains(category_id: str | None = None):
    service = DomainService()
    domains, total = service.find_all(category_id)
    return success_response(domains, meta={"total": total})


@router.get("/active")
def get_active_domains():
    """获取所有激活的领域配置（用户端使用）"""
    service = DomainService()
    domains = service.find_active()
    return success_response(domains)


@router.get("/grouped")
def get_grouped_domains(lang: str = "zh", product_line_id: str | None = None):
    """按分类分组返回领域配置（用户端使用）"""
    service = DomainService()
    grouped = service.find_grouped_by_category(lang, product_line_id)
    return success_response(grouped)


@router.get("/{id}")
def get_domain(id: str):
    service = DomainService()
    domain = service.find_by_id(id)
    return success_response(domain)


@router.post("/", dependencies=[Depends(get_current_admin)])
def create_domain(data: CreateDomainRequest):
    service = DomainService()
    domain = service.create(data.model_dump())
    return success_response(domain)


@router.put("/{id}", dependencies=[Depends(get_current_admin)])
def update_domain(id: str, data: UpdateDomainRequest):
    service = DomainService()
    domain = service.update(id, data.model_dump(exclude_none=True))
    return success_response(domain)


@router.delete("/{id}", dependencies=[Depends(get_current_admin)])
def delete_domain(id: str):
    service = DomainService()
    service.delete(id)
    return success_response(None)


# ========== Question Routes ==========
@router.get("/questions")
def get_questions(domain_id: str | None = None):
    service = QuestionService()
    questions = service.find_all(domain_id)
    return success_response(questions)


@router.post("/questions", dependencies=[Depends(get_current_admin)])
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


@router.delete("/questions/{id}", dependencies=[Depends(get_current_admin)])
def delete_question(id: str):
    service = QuestionService()
    service.delete(id)
    return success_response(None)
