from pydantic import BaseModel


class DomainCategoryBase(BaseModel):
    code: str
    name: str
    name_en: str
    description: str
    description_en: str
    icon: str
    color: str
    sort_order: int


class CreateDomainCategoryRequest(DomainCategoryBase):
    pass


class UpdateDomainCategoryRequest(BaseModel):
    name: str
    name_en: str
    description: str
    description_en: str
    icon: str
    color: str
    is_active: bool
    sort_order: int


class DomainBase(BaseModel):
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


class CreateDomainRequest(DomainBase):
    pass


class UpdateDomainRequest(BaseModel):
    name: str
    name_en: str
    description: str
    description_en: str
    icon: str
    color: str
    prompt: str
    prompt_en: str
    category_id: str
    is_active: bool
    sort_order: int


class DomainResponse(DomainBase):
    id: str
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class PromptBase(BaseModel):
    name: str
    description: str
    content: str
    content_en: str
    category: str


class CreatePromptRequest(PromptBase):
    pass


class UpdatePromptRequest(BaseModel):
    name: str
    description: str
    content: str
    content_en: str
    category: str
    is_active: bool


class PromptResponse(PromptBase):
    id: str
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class QuestionOptionDto(BaseModel):
    text: str
    text_en: str
    value: str


class CreateQuestionRequest(BaseModel):
    domain_id: str
    text: str
    text_en: str
    type: str
    options: list[QuestionOptionDto]
    sort_order: int


class QuestionResponse(BaseModel):
    id: str
    domain_id: str
    text: str
    text_en: str
    type: str
    options: list[dict]
    sort_order: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class AnalyticsSummaryResponse(BaseModel):
    total_users: int
    total_sessions: int
    total_messages: int
    active_users_today: int
    popular_domains: list[dict]
    recent_activity: list[dict]
