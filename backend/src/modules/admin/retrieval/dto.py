"""Retrieval Engine DTOs"""
from pydantic import BaseModel


class CreateEngineRequest(BaseModel):
    name: str
    display_name: str
    type: str
    description: str
    config: dict
    is_active: bool


class UpdateEngineRequest(BaseModel):
    display_name: str
    description: str
    config: dict
    is_active: bool


class SetDefaultEngineRequest(BaseModel):
    engine_id: str


class SetDomainEngineRequest(BaseModel):
    domain: str
    engine_id: str


class TestEngineRequest(BaseModel):
    engine_id: str
    query: str
    context: dict


class CompareEnginesRequest(BaseModel):
    engine_ids: list[str]
    query: str
    context: dict
