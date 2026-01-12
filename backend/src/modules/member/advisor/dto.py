from pydantic import BaseModel
from typing import Literal


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    lang: Literal["zh", "en"] = "zh"


class ChatStreamChunk(BaseModel):
    text: str
    sources: list[str] = []
