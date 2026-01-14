# LLM 模型数据定义
from typing import Any, Dict, List

LLM_MODELS: List[Dict[str, Any]] = [
    {
        "name": "gpt-4o",
        "display_name": "GPT-4o",
        "provider": "openai",
        "api_endpoint": "https://api.openai.com/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "gpt-4o-mini",
        "display_name": "GPT-4o Mini",
        "provider": "openai",
        "api_endpoint": "https://api.openai.com/v1",
        "is_active": True,
        "is_default": True,
        "config": {},
    },
    {
        "name": "claude-3-5-sonnet-20241022",
        "display_name": "Claude 3.5 Sonnet",
        "provider": "anthropic",
        "api_endpoint": "https://api.anthropic.com/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "deepseek-chat",
        "display_name": "DeepSeek Chat",
        "provider": "deepseek",
        "api_endpoint": "https://api.deepseek.com/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "gemini-2.0-flash",
        "display_name": "Gemini 2.0 Flash",
        "provider": "google",
        "api_endpoint": "https://generativelanguage.googleapis.com/v1beta",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "llama-3.3-70b-versatile",
        "display_name": "Llama 3.3 70B (Groq)",
        "provider": "groq",
        "api_endpoint": "https://api.groq.com/openai/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
]
