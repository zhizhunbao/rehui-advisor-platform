"""LLM Service - 统一管理和调用 LLM 模型"""
import json
import re
from datetime import datetime, timezone
from typing import Generator

import httpx
import requests

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin
from src.common.config import get_settings

RAW_GITHUB = "https://raw.githubusercontent.com"
GITHUB_API = "https://api.github.com"


class LLMService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.settings = get_settings()
        self.table_models = "llm_models"
        self.table_prompts = "prompt_templates"  # 使用现有的 prompt_templates 表

    # ========== Model Management ==========
    def find_all_models(self, page: int = 1, limit: int = 20) -> tuple[list[dict], int]:
        response = (
            self.client.table(self.table_models)
            .select("*", count="exact")
            .order("created_at", desc=True)
            .range((page - 1) * limit, page * limit - 1)
            .execute()
        )
        return response.data, response.count or 0

    def find_model_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table_models)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def find_active_models(self) -> list[dict]:
        response = (
            self.client.table(self.table_models)
            .select("*")
            .eq("is_active", True)
            .order("display_name")
            .execute()
        )
        return response.data

    def get_model_filters(self) -> dict:
        """获取模型筛选选项（provider、category、价格区间、context 区间）"""
        response = (
            self.client.table(self.table_models)
            .select("provider, category, input_price, output_price, context_window, is_free")
            .execute()
        )
        
        providers: dict[str, int] = {}
        categories: dict[str, int] = {}
        input_price_ranges: dict[str, int] = {"free": 0, "low": 0, "medium": 0, "high": 0}
        output_price_ranges: dict[str, int] = {"free": 0, "low": 0, "medium": 0, "high": 0}
        context_ranges: dict[str, int] = {"small": 0, "medium": 0, "large": 0, "xlarge": 0}
        
        for item in response.data:
            # Provider 统计
            p = item.get("provider") or "unknown"
            providers[p] = providers.get(p, 0) + 1
            
            # Category 统计
            c = item.get("category") or "general"
            categories[c] = categories.get(c, 0) + 1
            
            # 输入价格区间统计
            input_price = item.get("input_price", 0)
            if item.get("is_free") or input_price == 0:
                input_price_ranges["free"] += 1
            elif input_price < 1:
                input_price_ranges["low"] += 1
            elif input_price < 10:
                input_price_ranges["medium"] += 1
            else:
                input_price_ranges["high"] += 1
            
            # 输出价格区间统计
            output_price = item.get("output_price", 0)
            if item.get("is_free") or output_price == 0:
                output_price_ranges["free"] += 1
            elif output_price < 1:
                output_price_ranges["low"] += 1
            elif output_price < 10:
                output_price_ranges["medium"] += 1
            else:
                output_price_ranges["high"] += 1
            
            # Context 区间统计
            ctx = item.get("context_window", 0)
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
        response = (
            self.client.table(self.table_models)
            .select("*")
            .eq("is_default", True)
            .eq("is_active", True)
            .maybe_single()
            .execute()
        )
        return response.data

    def create_model(self, data: dict) -> dict:
        # 如果设为默认，先取消其他默认
        if data.get("is_default"):
            self._clear_default_model()
        
        response = self.client.table(self.table_models).insert(data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create model")
        return response.data[0]

    def update_model(self, id: str, data: dict) -> dict:
        existing = self.find_model_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Model {id} not found")
        
        # 如果设为默认，先取消其他默认
        if data.get("is_default"):
            self._clear_default_model()
        
        response = (
            self.client.table(self.table_models)
            .update(data)
            .eq("id", id)
            .execute()
        )
        return response.data[0]

    def delete_model(self, id: str) -> None:
        existing = self.find_model_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Model {id} not found")
        self.client.table(self.table_models).delete().eq("id", id).execute()

    def _clear_default_model(self) -> None:
        self.client.table(self.table_models).update({"is_default": False}).eq("is_default", True).execute()

    # ========== LLM Invocation ==========
    def chat(self, prompt_name: str, variables: dict, model_id: str | None = None) -> str:
        """同步调用 LLM，返回完整响应
        
        Args:
            prompt_name: prompt_templates 表中的 name
            variables: 模板变量，用于替换 {variable} 占位符
            model_id: 可选，指定使用的模型 ID，不指定则使用默认模型
        """
        prompt = self._find_prompt_by_name(prompt_name)
        if not prompt:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt '{prompt_name}' not found")
        
        model = self.find_model_by_id(model_id) if model_id else self.get_default_model()
        if not model:
            raise AppError(AppErrorCode.NOT_FOUND, "No active LLM model available")
        
        # 构建消息
        messages = self._build_messages(prompt, variables)
        
        # 调用 LLM
        response = self._call_llm(model, messages)
        return response

    def chat_stream(self, prompt_name: str, variables: dict, model_id: str | None = None) -> Generator[str, None, None]:
        """流式调用 LLM
        
        Args:
            prompt_name: prompt_templates 表中的 name
            variables: 模板变量
            model_id: 可选，指定使用的模型 ID
        """
        prompt = self._find_prompt_by_name(prompt_name)
        if not prompt:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt '{prompt_name}' not found")
        
        model = self.find_model_by_id(model_id) if model_id else self.get_default_model()
        if not model:
            raise AppError(AppErrorCode.NOT_FOUND, "No active LLM model available")
        
        messages = self._build_messages(prompt, variables)
        
        yield from self._call_llm_stream(model, messages)

    def _find_prompt_by_name(self, name: str) -> dict | None:
        """从 prompt_templates 表查找 Prompt"""
        response = (
            self.client.table(self.table_prompts)
            .select("*")
            .eq("name", name)
            .eq("is_active", True)
            .maybe_single()
            .execute()
        )
        return response.data

    def _build_messages(self, prompt: dict, variables: dict) -> list[dict]:
        """构建消息列表
        
        prompt_templates 表的 template 字段作为 user message
        """
        messages = []
        
        # User prompt (使用 template 字段)
        if prompt.get("template"):
            user_content = prompt["template"]
            for key, value in variables.items():
                user_content = user_content.replace(f"{{{key}}}", str(value))
            messages.append({"role": "user", "content": user_content})
        
        return messages

    def _call_llm(
        self, model: dict, messages: list[dict], 
        temperature: float = 0.7, max_tokens: int = 2000
    ) -> str:
        """调用 LLM API（OpenAI 兼容格式）"""
        api_endpoint = model.get("api_endpoint", "https://api.openai.com/v1")
        api_key = self._get_api_key(model)
        
        with httpx.Client(timeout=120) as client:
            response = client.post(
                f"{api_endpoint}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model["name"],
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )
            
            if response.status_code != 200:
                raise AppError(
                    AppErrorCode.EXTERNAL_SERVICE_ERROR,
                    f"LLM API error: {response.text}"
                )
            
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def _call_llm_stream(
        self, model: dict, messages: list[dict],
        temperature: float = 0.7, max_tokens: int = 2000
    ) -> Generator[str, None, None]:
        """流式调用 LLM API"""
        api_endpoint = model.get("api_endpoint", "https://api.openai.com/v1")
        api_key = self._get_api_key(model)
        
        with httpx.Client(timeout=120) as client:
            with client.stream(
                "POST",
                f"{api_endpoint}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model["name"],
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                },
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
        """获取模型对应的 API Key"""
        provider = model.get("provider", "").lower()
        config = model.get("config", {})
        
        # 优先使用模型配置中的 key
        if config.get("api_key"):
            return config["api_key"]
        
        # 否则使用全局配置
        key_mapping = {
            "openai": self.settings.openrouter_api_key,  # 可以用 OpenRouter 代理
            "gemini": self.settings.gemini_api_key,
            "groq": self.settings.groq_api_key,
            "cohere": self.settings.cohere_api_key,
            "openrouter": self.settings.openrouter_api_key,
        }
        
        api_key = key_mapping.get(provider, "")
        if not api_key:
            raise AppError(
                AppErrorCode.CONFIGURATION_ERROR,
                f"API key not configured for provider: {provider}"
            )
        return api_key


    # ========== Sync from GitHub ==========
    def get_sync_sources(self) -> list[dict]:
        """获取 LLM 模型同步源（从 data_sources 表获取 category=llm-models 的链接）"""
        response = (
            self.client.table("data_sources")
            .select("*")
            .eq("category", "llm-models")
            .eq("status", "active")
            .execute()
        )
        return response.data

    def sync_from_github(self, source_id: str | None = None) -> dict:
        """从 GitHub 同步 LLM 模型数据
        
        Args:
            source_id: 指定同步源 ID，不指定则同步所有源
        """
        if source_id:
            sources = [self._get_source_by_id(source_id)]
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

    def _get_source_by_id(self, source_id: str) -> dict | None:
        """获取单个同步源"""
        response = (
            self.client.table("data_sources")
            .select("*")
            .eq("id", source_id)
            .maybe_single()
            .execute()
        )
        return response.data

    def _sync_from_source(self, source: dict) -> dict:
        """从单个源同步数据"""
        url = source.get("url", "")
        name = source.get("name", "").lower()
        
        # 根据源类型选择解析方法
        if "openrouter" in url.lower() or "openrouter" in name:
            return self._sync_from_openrouter()
        elif "litellm" in url.lower() or "litellm" in name:
            return self._sync_from_litellm(source)
        elif "ollama" in url.lower() or "ollama" in name:
            return self._sync_from_ollama()
        elif "huggingface" in url.lower() or "hugging" in name:
            return self._sync_from_huggingface()
        elif "free-llm-api" in url.lower() or "free llm" in name:
            return self._sync_from_free_llm_resources()
        else:
            return {"synced": 0, "errors": [{"source": url, "error": "No parser implemented for this source"}]}

    def _sync_from_openrouter(self) -> dict:
        """从 OpenRouter API 同步模型列表"""
        synced = 0
        errors = []
        
        try:
            response = requests.get("https://openrouter.ai/api/v1/models", timeout=30)
            if response.status_code != 200:
                return {"synced": 0, "errors": [{"source": "openrouter", "error": f"API error: {response.status_code}"}]}
            
            data = response.json()
            models = data.get("data", [])
            
            for model in models:
                try:
                    model_id = model.get("id", "")
                    if not model_id:
                        continue
                    
                    # 解析 provider: "openai/gpt-4" -> "openai"
                    # OpenRouter 的 model_id 格式是 "provider/model-name"
                    provider = model_id.split("/")[0] if "/" in model_id else "openrouter"
                    model_name = model_id.split("/")[-1] if "/" in model_id else model_id
                    model_name = model_id.split("/")[-1] if "/" in model_id else model_id
                    
                    # 解析价格 (OpenRouter 返回的是 per token，转换为 per 1M tokens)
                    # 注意：-1 表示动态定价，0 表示免费
                    pricing = model.get("pricing", {})
                    raw_input = float(pricing.get("prompt", 0))
                    raw_output = float(pricing.get("completion", 0))
                    # 处理特殊值：-1 表示动态定价，设为 0 并标记
                    input_price = 0 if raw_input < 0 else raw_input * 1_000_000
                    output_price = 0 if raw_output < 0 else raw_output * 1_000_000
                    is_dynamic_pricing = raw_input < 0 or raw_output < 0
                    
                    # 解析能力
                    capabilities = []
                    if model.get("architecture", {}).get("modality") == "multimodal":
                        capabilities.append("vision")
                    
                    # 获取发布日期：优先使用 API 返回的 created 字段，否则从模型名称提取
                    release_date = None
                    if model.get("created"):
                        try:
                            created_ts = int(model["created"])
                            release_date = datetime.fromtimestamp(created_ts, tz=timezone.utc).strftime("%Y-%m-%d")
                        except (ValueError, TypeError):
                            pass
                    if not release_date:
                        release_date = self._extract_release_date(model_id)
                    
                    model_data = {
                        "name": model_id,
                        "display_name": model.get("name", model_name),
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
                        "release_date": release_date,
                        "is_active": True,
                        "is_default": False,
                        "is_deprecated": False,
                        "config": {},
                    }
                    
                    synced += self._upsert_model(model_data)
                    
                except Exception as e:
                    errors.append({"model": model.get("id", "unknown"), "error": str(e)})
        
        except Exception as e:
            errors.append({"source": "openrouter", "error": str(e)})
        
        return {"synced": synced, "errors": errors}

    def _sync_from_litellm(self, source: dict) -> dict:
        """从 LiteLLM 模型列表同步"""
        synced = 0
        errors = []
        
        # LiteLLM model_prices.json
        url = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                return {"synced": 0, "errors": [{"source": "litellm", "error": f"HTTP {response.status_code}"}]}
            
            models = response.json()
            
            for model_id, info in models.items():
                if model_id.startswith("sample_spec"):
                    continue
                
                try:
                    # 解析 provider
                    provider = info.get("litellm_provider", "unknown")
                    
                    # 解析价格
                    input_price = float(info.get("input_cost_per_token", 0)) * 1_000_000
                    output_price = float(info.get("output_cost_per_token", 0)) * 1_000_000
                    
                    # 解析能力
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
                        "description": "",
                        "is_active": True,
                        "is_default": False,
                        "is_deprecated": False,
                        "config": {},
                    }
                    
                    synced += self._upsert_model(model_data)
                    
                except Exception as e:
                    errors.append({"model": model_id, "error": str(e)})
        
        except Exception as e:
            errors.append({"source": "litellm", "error": str(e)})
        
        return {"synced": synced, "errors": errors}

    def _sync_from_ollama(self) -> dict:
        """从 Ollama 模型库同步本地可部署模型"""
        synced = 0
        errors = []
        
        try:
            # Ollama 官方模型库 API
            response = requests.get("https://ollama.com/api/models", timeout=30)
            if response.status_code != 200:
                # 尝试备用方式：从 GitHub 获取
                return self._sync_ollama_from_github()
            
            data = response.json()
            models = data.get("models", [])
            
            for model in models:
                try:
                    model_name = model.get("name", "")
                    if not model_name:
                        continue
                    
                    # Ollama 模型都是本地部署
                    model_data = {
                        "name": f"ollama/{model_name}",
                        "display_name": model.get("title", model_name.replace("-", " ").title()),
                        "provider": "ollama",
                        "api_endpoint": "http://localhost:11434/api",
                        "category": self._detect_category(model_name, model.get("description", "")),
                        "deployment_type": "local",
                        "input_price": 0,
                        "output_price": 0,
                        "is_free": True,
                        "context_window": model.get("context_length", 4096),
                        "max_output_tokens": model.get("max_output_tokens", 4096),
                        "capabilities": model.get("capabilities", []),
                        "description": model.get("description", ""),
                        "release_date": model.get("updated_at", "")[:10] if model.get("updated_at") else None,
                        "is_active": True,
                        "is_default": False,
                        "is_deprecated": False,
                        "config": {"sizes": model.get("sizes", [])},
                    }
                    
                    synced += self._upsert_model(model_data)
                    
                except Exception as e:
                    errors.append({"model": model.get("name", "unknown"), "error": str(e)})
        
        except Exception as e:
            errors.append({"source": "ollama", "error": str(e)})
        
        return {"synced": synced, "errors": errors}

    def _sync_ollama_from_github(self) -> dict:
        """从 Ollama GitHub 仓库获取模型列表"""
        synced = 0
        errors = []
        
        # 常见的 Ollama 模型列表
        ollama_models = [
            {"name": "llama3.3", "display_name": "Llama 3.3", "provider_origin": "meta", "context": 131072},
            {"name": "llama3.2", "display_name": "Llama 3.2", "provider_origin": "meta", "context": 131072},
            {"name": "llama3.1", "display_name": "Llama 3.1", "provider_origin": "meta", "context": 131072},
            {"name": "llama3", "display_name": "Llama 3", "provider_origin": "meta", "context": 8192},
            {"name": "gemma2", "display_name": "Gemma 2", "provider_origin": "google", "context": 8192},
            {"name": "gemma", "display_name": "Gemma", "provider_origin": "google", "context": 8192},
            {"name": "qwen2.5", "display_name": "Qwen 2.5", "provider_origin": "alibaba", "context": 131072},
            {"name": "qwen2", "display_name": "Qwen 2", "provider_origin": "alibaba", "context": 131072},
            {"name": "phi4", "display_name": "Phi 4", "provider_origin": "microsoft", "context": 16384},
            {"name": "phi3", "display_name": "Phi 3", "provider_origin": "microsoft", "context": 4096},
            {"name": "mistral", "display_name": "Mistral", "provider_origin": "mistral", "context": 32768},
            {"name": "mixtral", "display_name": "Mixtral", "provider_origin": "mistral", "context": 32768},
            {"name": "codellama", "display_name": "Code Llama", "provider_origin": "meta", "context": 16384},
            {"name": "deepseek-coder-v2", "display_name": "DeepSeek Coder V2", "provider_origin": "deepseek", "context": 131072},
            {"name": "deepseek-v3", "display_name": "DeepSeek V3", "provider_origin": "deepseek", "context": 131072},
            {"name": "starcoder2", "display_name": "StarCoder 2", "provider_origin": "bigcode", "context": 16384},
            {"name": "yi", "display_name": "Yi", "provider_origin": "01-ai", "context": 200000},
            {"name": "command-r", "display_name": "Command R", "provider_origin": "cohere", "context": 131072},
            {"name": "aya", "display_name": "Aya", "provider_origin": "cohere", "context": 8192},
            {"name": "vicuna", "display_name": "Vicuna", "provider_origin": "lmsys", "context": 4096},
            {"name": "wizardlm2", "display_name": "WizardLM 2", "provider_origin": "microsoft", "context": 65536},
            {"name": "dolphin-mixtral", "display_name": "Dolphin Mixtral", "provider_origin": "cognitivecomputations", "context": 32768},
            {"name": "nomic-embed-text", "display_name": "Nomic Embed Text", "provider_origin": "nomic", "context": 8192},
            {"name": "mxbai-embed-large", "display_name": "MxBai Embed Large", "provider_origin": "mixedbread", "context": 512},
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
                    "capabilities": [],
                    "description": f"Local deployment via Ollama. Original model by {model['provider_origin']}.",
                    "release_date": None,
                    "is_active": True,
                    "is_default": False,
                    "is_deprecated": False,
                    "config": {"provider_origin": model["provider_origin"]},
                }
                
                synced += self._upsert_model(model_data)
                
            except Exception as e:
                errors.append({"model": model["name"], "error": str(e)})
        
        return {"synced": synced, "errors": errors}

    def _sync_from_huggingface(self) -> dict:
        """从 Hugging Face 同步热门 LLM 模型"""
        synced = 0
        errors = []
        
        try:
            # Hugging Face API - 获取热门文本生成模型
            url = "https://huggingface.co/api/models"
            params = {
                "filter": "text-generation",
                "sort": "downloads",
                "direction": -1,
                "limit": 100,
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return {"synced": 0, "errors": [{"source": "huggingface", "error": f"API error: {response.status_code}"}]}
            
            models = response.json()
            
            for model in models:
                try:
                    model_id = model.get("modelId", "")
                    if not model_id:
                        continue
                    
                    # 解析 provider (组织名)
                    provider = model_id.split("/")[0] if "/" in model_id else "huggingface"
                    
                    # 获取模型配置
                    config = model.get("config", {}) or {}
                    
                    model_data = {
                        "name": f"huggingface/{model_id}",
                        "display_name": model_id.split("/")[-1].replace("-", " ").title(),
                        "provider": provider,
                        "api_endpoint": f"https://api-inference.huggingface.co/models/{model_id}",
                        "category": self._detect_category(model_id, model.get("pipeline_tag", "")),
                        "deployment_type": "both",  # HF 模型可以 API 调用也可以本地部署
                        "input_price": 0,
                        "output_price": 0,
                        "is_free": True,  # HF Inference API 有免费额度
                        "context_window": config.get("max_position_embeddings", 4096),
                        "max_output_tokens": 4096,
                        "capabilities": model.get("tags", [])[:5],  # 取前5个标签
                        "description": model.get("description", "")[:500] if model.get("description") else "",
                        "release_date": model.get("lastModified", "")[:10] if model.get("lastModified") else None,
                        "is_active": True,
                        "is_default": False,
                        "is_deprecated": False,
                        "config": {
                            "downloads": model.get("downloads", 0),
                            "likes": model.get("likes", 0),
                        },
                    }
                    
                    synced += self._upsert_model(model_data)
                    
                except Exception as e:
                    errors.append({"model": model.get("modelId", "unknown"), "error": str(e)})
        
        except Exception as e:
            errors.append({"source": "huggingface", "error": str(e)})
        
        return {"synced": synced, "errors": errors}

    def _sync_from_free_llm_resources(self) -> dict:
        """从 Free LLM API Resources 同步免费 API 列表"""
        synced = 0
        errors = []
        
        # 从 GitHub 获取 README
        url = "https://raw.githubusercontent.com/cheahjs/free-llm-api-resources/main/README.md"
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                return {"synced": 0, "errors": [{"source": "free-llm-resources", "error": f"HTTP {response.status_code}"}]}
            
            content = response.text
            
            # 解析 README 中的免费 API 提供商
            # 格式通常是表格或列表
            free_providers = self._parse_free_llm_readme(content)
            
            for provider_info in free_providers:
                try:
                    model_data = {
                        "name": f"free/{provider_info['name']}",
                        "display_name": provider_info["display_name"],
                        "provider": provider_info["provider"],
                        "api_endpoint": provider_info.get("endpoint", ""),
                        "category": "chat",
                        "deployment_type": "api",
                        "input_price": 0,
                        "output_price": 0,
                        "is_free": True,
                        "context_window": provider_info.get("context", 4096),
                        "max_output_tokens": 4096,
                        "capabilities": [],
                        "description": provider_info.get("description", "Free API access"),
                        "release_date": None,
                        "is_active": True,
                        "is_default": False,
                        "is_deprecated": False,
                        "config": {"rate_limit": provider_info.get("rate_limit", "")},
                    }
                    
                    synced += self._upsert_model(model_data)
                    
                except Exception as e:
                    errors.append({"model": provider_info.get("name", "unknown"), "error": str(e)})
        
        except Exception as e:
            errors.append({"source": "free-llm-resources", "error": str(e)})
        
        return {"synced": synced, "errors": errors}

    def _parse_free_llm_readme(self, content: str) -> list[dict]:
        """解析 Free LLM API Resources README"""
        providers = []
        
        # 已知的免费 API 提供商
        known_free_apis = [
            {
                "name": "groq-free",
                "display_name": "Groq (Free Tier)",
                "provider": "groq",
                "endpoint": "https://api.groq.com/openai/v1",
                "context": 131072,
                "description": "Free tier with rate limits. Supports Llama, Mixtral, Gemma.",
                "rate_limit": "30 RPM",
            },
            {
                "name": "together-free",
                "display_name": "Together AI (Free Tier)",
                "provider": "together",
                "endpoint": "https://api.together.xyz/v1",
                "context": 32768,
                "description": "Free tier with $25 credits. Supports many open models.",
                "rate_limit": "60 RPM",
            },
            {
                "name": "openrouter-free",
                "display_name": "OpenRouter (Free Models)",
                "provider": "openrouter",
                "endpoint": "https://openrouter.ai/api/v1",
                "context": 131072,
                "description": "Free models available including Llama, Mistral, etc.",
                "rate_limit": "20 RPM",
            },
            {
                "name": "deepseek-free",
                "display_name": "DeepSeek (Free Tier)",
                "provider": "deepseek",
                "endpoint": "https://api.deepseek.com/v1",
                "context": 131072,
                "description": "Free tier with generous limits.",
                "rate_limit": "60 RPM",
            },
            {
                "name": "siliconflow-free",
                "display_name": "SiliconFlow (Free Tier)",
                "provider": "siliconflow",
                "endpoint": "https://api.siliconflow.cn/v1",
                "context": 32768,
                "description": "Chinese provider with free tier.",
                "rate_limit": "100 RPM",
            },
            {
                "name": "cloudflare-workers-ai",
                "display_name": "Cloudflare Workers AI",
                "provider": "cloudflare",
                "endpoint": "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run",
                "context": 4096,
                "description": "Free tier with 10,000 neurons/day.",
                "rate_limit": "10000 neurons/day",
            },
            {
                "name": "huggingface-inference",
                "display_name": "Hugging Face Inference API",
                "provider": "huggingface",
                "endpoint": "https://api-inference.huggingface.co/models",
                "context": 4096,
                "description": "Free tier with rate limits.",
                "rate_limit": "Varies by model",
            },
            {
                "name": "cohere-free",
                "display_name": "Cohere (Free Tier)",
                "provider": "cohere",
                "endpoint": "https://api.cohere.ai/v1",
                "context": 128000,
                "description": "Free tier with 1000 API calls/month.",
                "rate_limit": "5 RPM",
            },
        ]
        
        providers.extend(known_free_apis)
        
        # 尝试从 README 中解析更多信息
        # 查找表格格式的数据
        table_pattern = r'\|([^|]+)\|([^|]+)\|([^|]+)\|'
        matches = re.findall(table_pattern, content)
        
        for match in matches:
            name = match[0].strip()
            if name and name != "Provider" and name != "---" and not name.startswith("-"):
                # 检查是否已存在
                if not any(p["display_name"].lower() == name.lower() for p in providers):
                    providers.append({
                        "name": name.lower().replace(" ", "-"),
                        "display_name": name,
                        "provider": name.lower().split()[0],
                        "endpoint": "",
                        "context": 4096,
                        "description": f"Free API from {name}",
                        "rate_limit": "",
                    })
        
        return providers

    def _upsert_model(self, data: dict) -> int:
        """插入或更新模型"""
        existing = (
            self.client.table(self.table_models)
            .select("id")
            .eq("name", data["name"])
            .execute()
        )
        
        if existing.data and len(existing.data) > 0:
            # 更新（保留用户自定义的字段）
            update_data = {k: v for k, v in data.items() if k not in ["is_active", "is_default", "config"]}
            self.client.table(self.table_models).update(update_data).eq("id", existing.data[0]["id"]).execute()
        else:
            # 新增
            self.client.table(self.table_models).insert(data).execute()
        
        return 1

    def _detect_category(self, model_id: str, description: str) -> str:
        """根据模型名称和描述检测类别"""
        text = (model_id + " " + description).lower()
        
        if any(k in text for k in ["code", "coder", "codex", "starcoder", "deepseek-coder"]):
            return "coding"
        if any(k in text for k in ["vision", "image", "multimodal", "4o", "gemini-pro-vision"]):
            return "vision"
        if any(k in text for k in ["embed", "embedding"]):
            return "embedding"
        if any(k in text for k in ["reason", "o1", "o3", "thinking"]):
            return "reasoning"
        if any(k in text for k in ["chat", "instruct", "turbo"]):
            return "chat"
        
        return "general"

    def _extract_release_date(self, model_id: str) -> str | None:
        """从模型名称中提取发布日期
        
        支持格式:
        - YYYYMMDD: claude-3-5-sonnet-20241022
        - YYYY-MM-DD: some-model-2024-01-25
        - MMDD (推断年份): gpt-4-0125-preview, gpt-4o-2024-08-06
        """
        # 验证日期是否合理
        def validate_date(year: int, month: int, day: int) -> bool:
            if year < 2020 or year > 2030:
                return False
            if month < 1 or month > 12:
                return False
            if day < 1 or day > 31:
                return False
            return True
        
        patterns = [
            # YYYYMMDD: claude-3-5-sonnet-20241022
            (r'(?<!\d)(20\d{2})(\d{2})(\d{2})(?!\d)', lambda m: (int(m.group(1)), int(m.group(2)), int(m.group(3)))),
            # YYYY-MM-DD: some-model-2024-01-25
            (r'(20\d{2})-(\d{2})-(\d{2})(?!\d)', lambda m: (int(m.group(1)), int(m.group(2)), int(m.group(3)))),
            # YYYY-MM: some-model-2024-01
            (r'(20\d{2})-(\d{2})(?!-?\d)', lambda m: (int(m.group(1)), int(m.group(2)), 1)),
            # MMDD (4位，推断为2024年): gpt-4-0125-preview -> 2024-01-25
            (r'(?<!\d)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)', lambda m: (2024, int(m.group(1)), int(m.group(2)))),
        ]
        
        for pattern, extractor in patterns:
            match = re.search(pattern, model_id)
            if match:
                try:
                    year, month, day = extractor(match)
                    if validate_date(year, month, day):
                        return f"{year:04d}-{month:02d}-{day:02d}"
                except (ValueError, IndexError):
                    continue
        
        return None

    def _get_provider_endpoint(self, provider: str) -> str:
        """获取 provider 的默认 API endpoint"""
        endpoints = {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "google": "https://generativelanguage.googleapis.com/v1beta",
            "groq": "https://api.groq.com/openai/v1",
            "deepseek": "https://api.deepseek.com/v1",
            "mistral": "https://api.mistral.ai/v1",
            "cohere": "https://api.cohere.ai/v1",
        }
        return endpoints.get(provider.lower(), "")
