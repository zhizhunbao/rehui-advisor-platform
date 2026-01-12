from pydantic import BaseModel


# ========== LLM Model ==========
class CreateLLMModelRequest(BaseModel):
    name: str
    display_name: str
    provider: str
    api_endpoint: str
    version: str
    category: str
    deployment_type: str
    input_price: float
    output_price: float
    is_free: bool
    context_window: int
    max_output_tokens: int
    capabilities: list[str]
    description: str
    docker_image: str
    hardware_requirements: dict
    rate_limit: dict
    latency_ms: int
    quality_score: float
    license: str
    release_date: str
    is_deprecated: bool
    fallback_model_id: str
    is_active: bool
    is_default: bool
    config: dict
    sort_order: int


class UpdateLLMModelRequest(BaseModel):
    name: str
    display_name: str
    provider: str
    api_endpoint: str
    version: str
    category: str
    deployment_type: str
    input_price: float
    output_price: float
    is_free: bool
    context_window: int
    max_output_tokens: int
    capabilities: list[str]
    description: str
    docker_image: str
    hardware_requirements: dict
    rate_limit: dict
    latency_ms: int
    quality_score: float
    license: str
    release_date: str
    is_deprecated: bool
    fallback_model_id: str
    is_active: bool
    is_default: bool
    config: dict
    sort_order: int


# ========== Chat ==========
class ChatRequest(BaseModel):
    prompt_name: str
    variables: dict
    model_id: str
