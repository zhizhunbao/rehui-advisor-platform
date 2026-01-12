"""Scheduler DTOs"""
from pydantic import BaseModel


class CreateJobRequest(BaseModel):
    name: str
    description: str
    job_type: str
    cron_expression: str
    parameters: dict
    is_active: bool


class UpdateJobRequest(BaseModel):
    name: str
    description: str
    cron_expression: str
    parameters: dict
    is_active: bool


class JobTypeInfo(BaseModel):
    type: str
    name_zh: str
    name_en: str
    description_zh: str
    description_en: str
    parameters_schema: dict
