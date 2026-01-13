"""LLM Service - 统一管理和调用 LLM 模型（使用 Document Store）"""
import json
import re
from datetime import datetime, timezone
from typing import Generator

import httpx
import requests

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.config import get_settings
from src.common.enum import RAW_GITHUB, GITHUB_API
from src.common.helper import paginate

DOC_TYPE_MODEL = "admin_llm_model"


class LLMService:
    def __init__(self) -> None:
        self.store = DocumentStore()
        self.settings = get_settings()

    # ========== Model Management ==========
    def find_all_models(self, page: int = 1, limit: int = 20) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_MODEL, status="active", limit=1000)
        docs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        paged, total = paginate(docs, page, limit)
        return [self._model_to_response(doc) for doc in paged], total

    def find_model_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_MODEL or doc["status"] == "deleted":
            return None
        return self._model_to_response(doc)

    def find_model_by_name(self, name: str) -> dict | None:
        docs = self.store.find(DOC_TYPE_MODEL, status="active")
        for doc in docs:
            if doc["data"].get("name") == name:
                return self._model_to_response(doc)
        return None

    def find_active_models(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE_MODEL, status="active")
        models = [
            self._model_to_response(doc)
            for doc in docs
            if doc["data"].get("is_active", True)
        ]
        models.sort(key=lambda x: x.get("display_name", ""))
        return models

    def get_model_filters(self) -> dict:
        """获取模型筛选选项"""
        docs = self.store.find(DOC_TYPE_MODEL, status="active")
        
        providers: dict[str, int] = {}
        categories: dict[str, int] = {}
        input_price_ranges = {"free": 0, "low": 0, "medium": 0, "high": 0}
        output_price_ranges = {"free": 0, "low": 0, "medium": 0, "high": 0}
        context_ranges = {"small": 0, "medium": 0, "large": 0, "xlarge": 0}
        
        for doc in docs:
            data = doc["data"]
            p = data.get("provider") or "unknown"
            providers[p] = providers.get(p, 0) + 1
            
            c = data.get("category") or "general"
            categories[c] = categories.get(c, 0) + 1
            
            input_price = data.get("input_price", 0)
            if data.get("is_free") or input_price == 0:
                input_price_ranges["free"] += 1
            elif input_price < 1:
                input_price_ranges["low"] += 1
            elif input_price < 10:
                input_price_ranges["medium"] += 1
            else:
                input_price_ranges["high"] += 1
            
            output_price = data.get("output_price", 0)
            if data.get("is_free") or output_price == 0:
                output_price_ranges["free"] += 1
            elif output_price < 1:
                output_price_ranges["low"] += 1
            elif output_price < 10:
                output_price_ranges["medium"] += 1
            else:
                output_price_ranges["high"] += 1
            
            ctx = data.get("context_window", 0)
            if ctx <= 8192:
                context_ranges["small"] += 1
            elif ctx <= 32768:
                context_ranges["medium"] += 1
            elif ctx <= 131072:
                context_ranges["large"] += 1
            else:
                context_ranges["xlarge"] += 1
        
        return {
            "providers": [{"provider": k, "count": v} for k, v in sorted(providers.items(), key=lambda x: -x[1])],
            "categories": [{"category": k, "count": v} for k, v in sorted(categories.items(), key=lambda x: -x[1])],
            "input_price_ranges": [
                {"value": "free", "label": "Free", "count": input_price_ranges["free"]},
                {"value": "low", "label": "<$1", "count": input_price_ranges["low"]},
                {"value": "medium", "label": "$1-10", "count": input_price_ranges["medium"]},
                {"value": "high", "label": ">$10", "count": input_price_ranges["high"]},
            ],
            "output_price_ranges": [
                {"value": "free", "label": "Free", "count": output_price_ranges["free"]},
                {"value": "low", "label": "<$1", "count": output_price_ranges["low"]},
                {"value": "medium", "label": "$1-10", "count": output_price_ranges["medium"]},
                {"value": "high", "label": ">$10", "count": output_price_ranges["high"]},
            ],
            "context_ranges": [
                {"value": "small", "label": "≤8K", "count": context_ranges["small"]},
                {"value": "medium", "label": "8K-32K", "count": context_ranges["medium"]},
                {"value": "large", "label": "32K-128K", "count": context_ranges["large"]},
                {"value": "xlarge", "label": ">128K", "count": context_ranges["xlarge"]},
            ],
        }

    def get_default_model(self) -> dict | None:
        docs = self.store.find(DOC_TYPE_MODEL, status="active")
        for doc in docs:
            data = doc["data"]
            if data.get("is_default") and data.get("is_active"):
                return self._model_to_response(doc)
        return None

    def create_model(self, data: dict) -> dict:
        if data.get("is_default"):
            self._clear_default_model()
        doc = self.store.create(DOC_TYPE_MODEL, data)
        return self._model_to_response(doc)

    def update_model(self, id: str, data: dict) -> dict:
        existing = self.find_model_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Model {id} not found")
        if data.get("is_default"):
            self._clear_default_model()
        doc = self.store.update(id, data_updates=data)
        return self._model_to_response(doc)

    def delete_model(self, id: str) -> None:
        existing = self.find_model_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Model {id} not found")
        self.store.delete(id)

    def _clear_default_model(self) -> None:
        docs = self.store.find(DOC_TYPE_MODEL, status="active")
        for doc in docs:
            if doc["data"].get("is_default"):
                self.store.update(doc["id"], data_updates={"is_default": False})

    # ========== LLM Invocation ==========
    def chat(self, prompt_name: str, variables: dict, model_id: str | None = None) -> str:
        """同步调用 LLM"""
        from src.modules.admin.prompt.service import PromptService
        prompt_service = PromptService()
        
        prompt = prompt_service.find_by_name_and_source(prompt_name, None)
        if not prompt:
            # 尝试只按名称查找
            docs = prompt_service.store.find("admin_prompt", status="active")
            for doc in docs:
                if doc["data"].get("name") == prompt_name:
                    prompt = prompt_service._prompt_to_response(doc)
                    break
        
        if not prompt:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt '{prompt_name}' not found")
        
        model = self.find_model_by_id(model_id) if model_id else self.get_default_model()
        if not model:
            raise AppError(AppErrorCode.NOT_FOUND, "No active LLM model available")
        
        messages = self._build_messages(prompt, variables)
        return self._call_llm(model, messages)

    def chat_stream(self, prompt_name: str, variables: dict, model_id: str | None = None) -> Generator[str, None, None]:
        """流式调用 LLM"""
        from src.modules.admin.prompt.service import PromptService
        prompt_service = PromptService()
        
        prompt = prompt_service.find_by_name_and_source(prompt_name, None)
        if not prompt:
            docs = prompt_service.store.find("admin_prompt", status="active")
            for doc in docs:
                if doc["data"].get("name") == prompt_name:
                    prompt = prompt_service._prompt_to_response(doc)
                    break
        
        if not prompt:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt '{prompt_name}' not found")
        
        model = self.find_model_by_id(model_id) if model_id else self.get_default_model()
        if not model:
            raise AppError(AppErrorCode.NOT_FOUND, "No active LLM model available")
        
        messages = self._build_messages(prompt, variables)
        yield from self._call_llm_stream(model, messages)

    def _build_messages(self, prompt: dict, variables: dict) -> list[dict]:
        messages = []
        if prompt.get("template"):
            user_content = prompt["template"]
            for key, value in variables.items():
                user_content = user_content.replace(f"{{{key}}}", str(value))
            messages.append({"role": "user", "content": user_content})
        return messages

    def _call_llm(self, model: dict, messages: list[dict], temperature: float = 0.7, max_tokens: int = 2000) -> str:
        api_endpoint = model.get("api_endpoint", "https://api.openai.com/v1")
        api_key = self._get_api_key(model)
        
        with httpx.Client(timeout=120) as client:
            response = client.post(
                f"{api_endpoint}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model["name"], "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
            )
            if response.status_code != 200:
                raise AppError(AppErrorCode.EXTERNAL_SERVICE_ERROR, f"LLM API error: {response.text}")
            return response.json()["choices"][0]["message"]["content"]

    def _call_llm_stream(self, model: dict, messages: list[dict], temperature: float = 0.7, max_tokens: int = 2000) -> Generator[str, None, None]:
        api_endpoint = model.get("api_endpoint", "https://api.openai.com/v1")
        api_key = self._get_api_key(model)
        
        with httpx.Client(timeout=120) as client:
            with client.stream(
                "POST", f"{api_endpoint}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model["name"], "messages": messages, "temperature": temperature, "max_tokens": max_tokens, "stream": True},
            ) as response:
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            content = chunk["choices"][0]["delta"].get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue

    def _get_api_key(self, model: dict) -> str:
        provider = model.get("provider", "").lower()
        config = model.get("config", {})
        if config.get("api_key"):
            return config["api_key"]
        key_mapping = {
            "openai": self.settings.openrouter_api_key,
            "gemini": self.settings.gemini_api_key,
            "groq": self.settings.groq_api_key,
            "cohere": self.settings.cohere_api_key,
            "openrouter": self.settings.openrouter_api_key,
        }
        api_key = key_mapping.get(provider, "")
        if not api_key:
            raise AppError(AppErrorCode.CONFIGURATION_ERROR, f"API key not configured for provider: {provider}")
        return api_key


    # ========== Sync from GitHub ==========
    def get_sync_sources(self) -> list[dict]:
        """获取 LLM 模型同步源"""
        from src.modules.admin.data_source.service import DataSourceService
        ds_service = DataSourceService()
        return ds_service.find_by_category("llm-models")

    def sync_from_github(self, source_id: str | None = None) -> dict:
        """从 GitHub 同步 LLM 模型数据"""
        if source_id:
            from src.modules.admin.data_source.service import DataSourceService
            ds_service = DataSourceService()
            source = ds_service.find_by_id(source_id)
            sources = [source] if source else []
        else:
            sources = self.get_sync_sources()
        
        if not sources:
            return {"synced": 0, "errors": [{"source": "none", "error": "No sync sources found"}]}
        
        total_synced = 0
        all_errors = []
        
        for source in sources:
            if not source:
                continue
            try:
                result = self._sync_from_source(source)
                total_synced += result.get("synced", 0)
                all_errors.extend(result.get("errors", []))
            except Exception as e:
                all_errors.append({"source": source.get("url", "unknown"), "error": str(e)})
        
        return {"synced": total_synced, "errors": all_errors}

    def _sync_from_source(self, source: dict) -> dict:
        url = source.get("url", "")
        name = source.get("name", "").lower()
        
        if "openrouter" in url.lower() or "openrouter" in name:
            return self._sync_from_openrouter()
        elif "litellm" in url.lower() or "litellm" in name:
            return self._sync_from_litellm()
        elif "ollama" in url.lower() or "ollama" in name:
            return self._sync_from_ollama()
        else:
            return {"synced": 0, "errors": [{"source": url, "error": "No parser implemented"}]}

    def _sync_from_openrouter(self) -> dict:
        synced = 0
        errors = []
        try:
            response = requests.get("https://openrouter.ai/api/v1/models", timeout=30)
            if response.status_code != 200:
                return {"synced": 0, "errors": [{"source": "openrouter", "error": f"API error: {response.status_code}"}]}
            
            for model in response.json().get("data", []):
                try:
                    model_id = model.get("id", "")
                    if not model_id:
                        continue
                    
                    provider = model_id.split("/")[0] if "/" in model_id else "openrouter"
                    pricing = model.get("pricing", {})
                    raw_input = float(pricing.get("prompt", 0))
                    raw_output = float(pricing.get("completion", 0))
                    input_price = 0 if raw_input < 0 else raw_input * 1_000_000
                    output_price = 0 if raw_output < 0 else raw_output * 1_000_000
                    
                    capabilities = []
                    if model.get("architecture", {}).get("modality") == "multimodal":
                        capabilities.append("vision")
                    
                    model_data = {
                        "name": model_id,
                        "display_name": model.get("name", model_id),
                        "provider": provider,
                        "api_endpoint": "https://openrouter.ai/api/v1",
                        "category": self._detect_category(model_id, model.get("description", "")),
                        "deployment_type": "api",
                        "input_price": input_price,
                        "output_price": output_price,
                        "is_free": input_price == 0 and output_price == 0,
                        "context_window": model.get("context_length", 4096),
                        "max_output_tokens": model.get("top_provider", {}).get("max_completion_tokens", 4096),
                        "capabilities": capabilities,
                        "description": model.get("description", ""),
                        "is_active": True,
                        "is_default": False,
                    }
                    synced += self._upsert_model(model_data)
                except Exception as e:
                    errors.append({"model": model.get("id", "unknown"), "error": str(e)})
        except Exception as e:
            errors.append({"source": "openrouter", "error": str(e)})
        return {"synced": synced, "errors": errors}

    def _sync_from_litellm(self) -> dict:
        synced = 0
        errors = []
        url = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                return {"synced": 0, "errors": [{"source": "litellm", "error": f"HTTP {response.status_code}"}]}
            
            for model_id, info in response.json().items():
                if model_id.startswith("sample_spec"):
                    continue
                try:
                    provider = info.get("litellm_provider", "unknown")
                    input_price = float(info.get("input_cost_per_token", 0)) * 1_000_000
                    output_price = float(info.get("output_cost_per_token", 0)) * 1_000_000
                    
                    capabilities = []
                    if info.get("supports_vision"):
                        capabilities.append("vision")
                    if info.get("supports_function_calling"):
                        capabilities.append("function_calling")
                    
                    model_data = {
                        "name": model_id,
                        "display_name": model_id.replace("-", " ").title(),
                        "provider": provider,
                        "api_endpoint": self._get_provider_endpoint(provider),
                        "category": self._detect_category(model_id, ""),
                        "deployment_type": "api",
                        "input_price": input_price,
                        "output_price": output_price,
                        "is_free": input_price == 0 and output_price == 0,
                        "context_window": info.get("max_tokens", 4096),
                        "max_output_tokens": info.get("max_output_tokens", 4096),
                        "capabilities": capabilities,
                        "is_active": True,
                        "is_default": False,
                    }
                    synced += self._upsert_model(model_data)
                except Exception as e:
                    errors.append({"model": model_id, "error": str(e)})
        except Exception as e:
            errors.append({"source": "litellm", "error": str(e)})
        return {"synced": synced, "errors": errors}

    def _sync_from_ollama(self) -> dict:
        synced = 0
        errors = []
        ollama_models = [
            {"name": "llama3.3", "display_name": "Llama 3.3", "context": 131072},
            {"name": "llama3.2", "display_name": "Llama 3.2", "context": 131072},
            {"name": "gemma2", "display_name": "Gemma 2", "context": 8192},
            {"name": "qwen2.5", "display_name": "Qwen 2.5", "context": 131072},
            {"name": "phi4", "display_name": "Phi 4", "context": 16384},
            {"name": "mistral", "display_name": "Mistral", "context": 32768},
            {"name": "deepseek-v3", "display_name": "DeepSeek V3", "context": 131072},
        ]
        for model in ollama_models:
            try:
                model_data = {
                    "name": f"ollama/{model['name']}",
                    "display_name": model["display_name"],
                    "provider": "ollama",
                    "api_endpoint": "http://localhost:11434/api",
                    "category": self._detect_category(model["name"], ""),
                    "deployment_type": "local",
                    "input_price": 0,
                    "output_price": 0,
                    "is_free": True,
                    "context_window": model.get("context", 4096),
                    "max_output_tokens": 4096,
                    "is_active": True,
                    "is_default": False,
                }
                synced += self._upsert_model(model_data)
            except Exception as e:
                errors.append({"model": model["name"], "error": str(e)})
        return {"synced": synced, "errors": errors}

    def _upsert_model(self, data: dict) -> int:
        existing = self.find_model_by_name(data["name"])
        if existing:
            update_data = {k: v for k, v in data.items() if k not in ["is_active", "is_default", "config"]}
            self.store.update(existing["id"], data_updates=update_data)
        else:
            self.store.create(DOC_TYPE_MODEL, data)
        return 1

    def _detect_category(self, model_id: str, description: str) -> str:
        text = (model_id + " " + description).lower()
        if any(k in text for k in ["code", "coder", "codex"]):
            return "coding"
        if any(k in text for k in ["vision", "image", "multimodal"]):
            return "vision"
        if any(k in text for k in ["embed", "embedding"]):
            return "embedding"
        if any(k in text for k in ["reason", "o1", "o3"]):
            return "reasoning"
        return "chat"

    def _get_provider_endpoint(self, provider: str) -> str:
        endpoints = {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "groq": "https://api.groq.com/openai/v1",
            "deepseek": "https://api.deepseek.com/v1",
            "cohere": "https://api.cohere.ai/v1",
        }
        return endpoints.get(provider.lower(), "")

    def _model_to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "name": data.get("name"),
            "display_name": data.get("display_name"),
            "provider": data.get("provider"),
            "api_endpoint": data.get("api_endpoint"),
            "category": data.get("category"),
            "deployment_type": data.get("deployment_type"),
            "input_price": data.get("input_price", 0),
            "output_price": data.get("output_price", 0),
            "is_free": data.get("is_free", False),
            "context_window": data.get("context_window", 4096),
            "max_output_tokens": data.get("max_output_tokens", 4096),
            "capabilities": data.get("capabilities", []),
            "description": data.get("description", ""),
            "release_date": data.get("release_date"),
            "is_active": data.get("is_active", True),
            "is_default": data.get("is_default", False),
            "is_deprecated": data.get("is_deprecated", False),
            "config": data.get("config", {}),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
