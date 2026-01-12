"""保险服务路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .dto import InsuranceType, QuoteRequest
from .service import InsuranceService

router = APIRouter(prefix="/insurance", tags=["insurance"])


@router.post("/quotes")
def get_quotes(request: QuoteRequest):
    service = InsuranceService()
    quotes = service.get_quotes(request)
    return success_response([q.model_dump() for q in quotes])


@router.post("/quotes/compare")
def compare_quotes(request: QuoteRequest):
    service = InsuranceService()
    quotes = service.get_quotes(request)
    comparison = service.compare_quotes(quotes)
    return success_response(comparison.model_dump())


@router.post("/risk-assessment")
def assess_risk(request: QuoteRequest):
    service = InsuranceService()
    assessment = service.assess_risk(request)
    return success_response(assessment.model_dump())


@router.get("/providers")
def get_providers(insurance_type: InsuranceType | None = Query(None, alias="type")):
    service = InsuranceService()
    providers = service.get_providers(insurance_type)
    return success_response([p.model_dump() for p in providers])
