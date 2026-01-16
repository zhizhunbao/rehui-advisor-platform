# LLM API Provider 领域发现脚本
from pathlib import Path
from typing import Any

from scripts.data.domain.tags import get_domain_match_tags
from scripts.discover.base import DomainDiscoverScript, ScriptResult


# ============================================================
# Provider 元信息 - 公司、国家等
# ============================================================
PROVIDER_META: dict[str, dict[str, str]] = {
    # 国际
    "openai": {"company": "OpenAI", "country": "🇺🇸 美国"},
    "anthropic": {"company": "Anthropic", "country": "🇺🇸 美国"},
    "gemini": {"company": "Google", "country": "🇺🇸 美国"},
    "xai": {"company": "xAI", "country": "🇺🇸 美国"},
    "groq": {"company": "Groq", "country": "🇺🇸 美国"},
    "mistral": {"company": "Mistral AI", "country": "🇫🇷 法国"},
    "cohere": {"company": "Cohere", "country": "🇨🇦 加拿大"},
    "ai21": {"company": "AI21 Labs", "country": "🇮🇱 以色列"},
    "together": {"company": "Together AI", "country": "🇺🇸 美国"},
    "fireworks": {"company": "Fireworks AI", "country": "🇺🇸 美国"},
    "replicate": {"company": "Replicate", "country": "🇺🇸 美国"},
    "huggingface": {"company": "Hugging Face", "country": "🇺🇸 美国"},
    "perplexity": {"company": "Perplexity AI", "country": "🇺🇸 美国"},
    "cerebras": {"company": "Cerebras", "country": "🇺🇸 美国"},
    "sambanova": {"company": "SambaNova", "country": "🇺🇸 美国"},
    "openrouter": {"company": "OpenRouter", "country": "🇺🇸 美国"},
    "cloudflare": {"company": "Cloudflare", "country": "🇺🇸 美国"},
    # 中国
    "deepseek": {"company": "深度求索", "country": "🇨🇳 中国"},
    "moonshot": {"company": "月之暗面", "country": "🇨🇳 中国"},
    "zhipu": {"company": "智谱AI", "country": "🇨🇳 中国"},
    "qwen": {"company": "阿里云", "country": "🇨🇳 中国"},
    "ernie": {"company": "百度", "country": "🇨🇳 中国"},
    "doubao": {"company": "字节跳动", "country": "🇨🇳 中国"},
    "baichuan": {"company": "百川智能", "country": "🇨🇳 中国"},
    "yi": {"company": "零一万物", "country": "🇨🇳 中国"},
    "minimax": {"company": "MiniMax", "country": "🇨🇳 中国"},
}


# ============================================================
# Provider 官方 GitHub 仓库 - 直接维护，不靠搜索
# ============================================================
PROVIDER_OFFICIAL_REPOS: dict[str, list[dict[str, str]]] = {
    # ==================== 国际 ====================
    "openai": [
        {"repo": "openai/openai-python", "desc": "OpenAI Python SDK"},
        {"repo": "openai/openai-node", "desc": "OpenAI Node.js SDK"},
    ],
    "anthropic": [
        {"repo": "anthropics/anthropic-sdk-python", "desc": "Anthropic Python SDK"},
        {"repo": "anthropics/anthropic-sdk-typescript", "desc": "Anthropic TypeScript SDK"},
    ],
    "gemini": [
        {"repo": "google-gemini/generative-ai-python", "desc": "Google Generative AI Python SDK"},
        {"repo": "google-gemini/generative-ai-js", "desc": "Google Generative AI JS SDK"},
    ],
    "xai": [
        {"repo": "xai-org/grok-1", "desc": "xAI Grok-1 开源模型"},
        {"repo": "xai-org/grok-prompts", "desc": "xAI Grok 系统提示词"},
    ],
    "groq": [
        {"repo": "groq/groq-python", "desc": "Groq Python SDK"},
        {"repo": "groq/groq-typescript", "desc": "Groq TypeScript SDK"},
    ],
    "mistral": [
        {"repo": "mistralai/client-python", "desc": "Mistral AI Python SDK"},
        {"repo": "mistralai/client-ts", "desc": "Mistral AI TypeScript SDK"},
    ],
    "cohere": [
        {"repo": "cohere-ai/cohere-python", "desc": "Cohere Python SDK"},
        {"repo": "cohere-ai/cohere-typescript", "desc": "Cohere TypeScript SDK"},
    ],
    "ai21": [
        {"repo": "AI21Labs/ai21-python", "desc": "AI21 Labs Python SDK"},
    ],
    "together": [
        {"repo": "togethercomputer/together-python", "desc": "Together AI Python SDK"},
    ],
    "fireworks": [
        {"repo": "fw-ai-external/python-sdk", "desc": "Fireworks AI Python SDK"},
    ],
    "replicate": [
        {"repo": "replicate/replicate-python", "desc": "Replicate Python SDK"},
        {"repo": "replicate/replicate-javascript", "desc": "Replicate JavaScript SDK"},
    ],
    "huggingface": [
        {"repo": "huggingface/huggingface_hub", "desc": "Hugging Face Hub Python SDK"},
        {"repo": "huggingface/transformers", "desc": "Hugging Face Transformers"},
    ],
    "perplexity": [
        {"repo": "nathanrchn/perplexityai", "desc": "Perplexity AI Python API (社区)"},
    ],
    # ==================== 中国 ====================
    "deepseek": [
        {"repo": "deepseek-ai/DeepSeek-V3", "desc": "DeepSeek V3 模型"},
        {"repo": "deepseek-ai/DeepSeek-R1", "desc": "DeepSeek R1 推理模型"},
        {"repo": "deepseek-ai/DeepSeek-Coder-V2", "desc": "DeepSeek Coder V2"},
    ],
    "moonshot": [
        {"repo": "MoonshotAI/Kimi-K2", "desc": "月之暗面 Kimi-K2 模型"},
    ],
    "zhipu": [
        {"repo": "zhipuai/zhipuai-sdk-python-v4", "desc": "智谱AI Python SDK"},
    ],
    "qwen": [
        {"repo": "QwenLM/Qwen2.5", "desc": "通义千问 Qwen2.5"},
        {"repo": "QwenLM/Qwen-Agent", "desc": "Qwen Agent 框架"},
    ],
    "ernie": [
        {"repo": "PaddlePaddle/ERNIE-SDK", "desc": "百度文心一言 ERNIE SDK"},
    ],
    "doubao": [
        {"repo": "volcengine/volc-sdk-python", "desc": "火山引擎(豆包) Python SDK"},
    ],
    "baichuan": [
        {"repo": "baichuan-inc/Baichuan2", "desc": "百川智能 Baichuan2"},
    ],
    "yi": [
        {"repo": "01-ai/Yi", "desc": "零一万物 Yi 模型"},
    ],
    "minimax": [
        {"repo": "MiniMax-AI/MiniMax-01", "desc": "MiniMax-01 模型"},
    ],
}


# ============================================================
# 免费 LLM Provider 注册信息（API Key 获取等）
# ============================================================
LLM_PROVIDER_REGISTRY: list[dict[str, Any]] = [
    # ==================== 国际 - 付费为主 ====================
    {
        "name": "OpenAI",
        "code": "openai",
        "console_url": "https://platform.openai.com/api-keys",
        "docs_url": "https://platform.openai.com/docs",
        "free_tier": "无免费额度，需充值",
        "env_key": "OPENAI_API_KEY",
        "models": ["gpt-4o", "gpt-4o-mini", "o1", "o1-mini"],
    },
    {
        "name": "Anthropic",
        "code": "anthropic",
        "console_url": "https://console.anthropic.com/settings/keys",
        "docs_url": "https://docs.anthropic.com/",
        "free_tier": "$5 免费额度（需验证手机）",
        "env_key": "ANTHROPIC_API_KEY",
        "models": ["claude-sonnet-4", "claude-opus-4", "claude-3.5-haiku"],
    },
    {
        "name": "xAI (Grok)",
        "code": "xai",
        "console_url": "https://console.x.ai/",
        "docs_url": "https://docs.x.ai/",
        "free_tier": "$25/月 免费额度（Beta期间）",
        "env_key": "XAI_API_KEY",
        "models": ["grok-4", "grok-3", "grok-2"],
    },
    {
        "name": "Mistral AI",
        "code": "mistral",
        "console_url": "https://console.mistral.ai/api-keys",
        "docs_url": "https://docs.mistral.ai/",
        "free_tier": "Experiment 计划免费",
        "env_key": "MISTRAL_API_KEY",
        "models": ["mistral-large", "mistral-small", "codestral"],
    },
    {
        "name": "AI21 Labs",
        "code": "ai21",
        "console_url": "https://studio.ai21.com/account/api-key",
        "docs_url": "https://docs.ai21.com/",
        "free_tier": "免费试用额度",
        "env_key": "AI21_API_KEY",
        "models": ["jamba-1.5-large", "jamba-1.5-mini"],
    },
    {
        "name": "Perplexity",
        "code": "perplexity",
        "console_url": "https://www.perplexity.ai/settings/api",
        "docs_url": "https://docs.perplexity.ai/",
        "free_tier": "无免费额度",
        "env_key": "PERPLEXITY_API_KEY",
        "models": ["sonar-pro", "sonar"],
    },
    # ==================== 国际 - 免费/低成本 ====================
    {
        "name": "Groq",
        "code": "groq",
        "console_url": "https://console.groq.com/keys",
        "docs_url": "https://console.groq.com/docs",
        "free_tier": "免费，有速率限制",
        "env_key": "GROQ_API_KEY",
        "models": ["llama-3.3-70b", "llama-3.1-8b-instant", "mixtral-8x7b"],
    },
    {
        "name": "Google Gemini",
        "code": "gemini",
        "console_url": "https://aistudio.google.com/apikey",
        "docs_url": "https://ai.google.dev/docs",
        "free_tier": "免费，15 RPM / 1M tokens/day",
        "env_key": "GEMINI_API_KEY",
        "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    },
    {
        "name": "Cerebras",
        "code": "cerebras",
        "console_url": "https://cloud.cerebras.ai/",
        "docs_url": "https://inference-docs.cerebras.ai/",
        "free_tier": "免费，速度极快",
        "env_key": "CEREBRAS_API_KEY",
        "models": ["llama-3.3-70b", "llama-3.1-8b"],
    },
    {
        "name": "SambaNova",
        "code": "sambanova",
        "console_url": "https://cloud.sambanova.ai/",
        "docs_url": "https://docs.sambanova.ai/",
        "free_tier": "免费",
        "env_key": "SAMBANOVA_API_KEY",
        "models": ["Meta-Llama-3.3-70B-Instruct", "Meta-Llama-3.1-8B-Instruct"],
    },
    {
        "name": "Together AI",
        "code": "together",
        "console_url": "https://api.together.xyz/settings/api-keys",
        "docs_url": "https://docs.together.ai/",
        "free_tier": "$5 免费额度",
        "env_key": "TOGETHER_API_KEY",
        "models": ["meta-llama/Llama-3.3-70B-Instruct-Turbo", "mistralai/Mixtral-8x7B"],
    },
    {
        "name": "Cohere",
        "code": "cohere",
        "console_url": "https://dashboard.cohere.com/api-keys",
        "docs_url": "https://docs.cohere.com/",
        "free_tier": "Trial key 免费",
        "env_key": "COHERE_API_KEY",
        "models": ["command-r-plus", "command-r", "command"],
    },
    {
        "name": "OpenRouter",
        "code": "openrouter",
        "console_url": "https://openrouter.ai/keys",
        "docs_url": "https://openrouter.ai/docs",
        "free_tier": "部分模型免费 (带 :free 后缀)",
        "env_key": "OPENROUTER_API_KEY",
        "models": ["deepseek/deepseek-r1:free", "google/gemma-2-9b-it:free"],
    },
    {
        "name": "Fireworks AI",
        "code": "fireworks",
        "console_url": "https://fireworks.ai/api-keys",
        "docs_url": "https://docs.fireworks.ai/",
        "free_tier": "$1 免费额度",
        "env_key": "FIREWORKS_API_KEY",
        "models": ["llama-v3p3-70b-instruct", "mixtral-8x7b-instruct"],
    },
    {
        "name": "Cloudflare Workers AI",
        "code": "cloudflare",
        "console_url": "https://dash.cloudflare.com/?to=/:account/ai",
        "docs_url": "https://developers.cloudflare.com/workers-ai/",
        "free_tier": "10k tokens/day 免费",
        "env_key": "CLOUDFLARE_API_TOKEN",
        "models": ["@cf/meta/llama-3.1-8b-instruct", "@cf/mistral/mistral-7b-instruct"],
    },
    {
        "name": "Hugging Face Inference",
        "code": "huggingface",
        "console_url": "https://huggingface.co/settings/tokens",
        "docs_url": "https://huggingface.co/docs/api-inference/",
        "free_tier": "Serverless 免费，有速率限制",
        "env_key": "HF_TOKEN",
        "models": ["meta-llama/Llama-3.2-3B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"],
    },
    {
        "name": "Replicate",
        "code": "replicate",
        "console_url": "https://replicate.com/account/api-tokens",
        "docs_url": "https://replicate.com/docs",
        "free_tier": "$10 免费额度",
        "env_key": "REPLICATE_API_TOKEN",
        "models": ["meta/llama-2-70b-chat", "mistralai/mixtral-8x7b-instruct"],
    },
    # ==================== 中国 ====================
    {
        "name": "DeepSeek",
        "code": "deepseek",
        "console_url": "https://platform.deepseek.com/api_keys",
        "docs_url": "https://platform.deepseek.com/api-docs",
        "free_tier": "新用户赠送额度",
        "env_key": "DEEPSEEK_API_KEY",
        "models": ["deepseek-chat", "deepseek-reasoner"],
    },
    {
        "name": "月之暗面 (Kimi)",
        "code": "moonshot",
        "console_url": "https://platform.moonshot.cn/console/api-keys",
        "docs_url": "https://platform.moonshot.cn/docs",
        "free_tier": "新用户赠送额度",
        "env_key": "MOONSHOT_API_KEY",
        "models": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
    },
    {
        "name": "智谱AI",
        "code": "zhipu",
        "console_url": "https://open.bigmodel.cn/usercenter/apikeys",
        "docs_url": "https://open.bigmodel.cn/dev/api",
        "free_tier": "新用户赠送额度",
        "env_key": "ZHIPU_API_KEY",
        "models": ["glm-4-plus", "glm-4-flash"],
    },
    {
        "name": "通义千问",
        "code": "qwen",
        "console_url": "https://dashscope.console.aliyun.com/apiKey",
        "docs_url": "https://help.aliyun.com/zh/dashscope/",
        "free_tier": "新用户赠送额度",
        "env_key": "DASHSCOPE_API_KEY",
        "models": ["qwen-max", "qwen-plus", "qwen-turbo"],
    },
    {
        "name": "百度文心一言",
        "code": "ernie",
        "console_url": "https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application",
        "docs_url": "https://cloud.baidu.com/doc/WENXINWORKSHOP/",
        "free_tier": "新用户赠送额度",
        "env_key": "QIANFAN_API_KEY",
        "models": ["ernie-4.0", "ernie-3.5", "ernie-speed"],
    },
    {
        "name": "字节豆包",
        "code": "doubao",
        "console_url": "https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey",
        "docs_url": "https://www.volcengine.com/docs/82379",
        "free_tier": "新用户赠送额度",
        "env_key": "ARK_API_KEY",
        "models": ["doubao-pro", "doubao-lite"],
    },
]


class DiscoverLLMProvidersScript(DomainDiscoverScript):
    """LLM API 服务商资源发现 - 只保存官方 SDK 仓库"""

    NAME = "discover_llm_providers"
    DESCRIPTION = "发现 LLM API 服务商的官方仓库"
    DOMAIN_CODE = "llm_providers"
    MIN_QUALITY_SCORE = 50.0

    @property
    def KEYWORDS(self) -> list[str]:
        return []  # 不搜索，直接用官方仓库

    def _get_domain_tags(self) -> list[dict[str, Any]]:
        return get_domain_match_tags(self.DOMAIN_CODE)

    def _init_sources(self) -> None:
        self.SOURCES = []  # 不使用搜索源

    def run(self) -> str:
        """直接保存官方仓库到 raw_data，先验证仓库是否存在"""
        import requests
        import os
        from datetime import datetime
        from dotenv import load_dotenv
        
        load_dotenv(Path(__file__).parents[3] / ".env", override=True)
        token = os.getenv("GITHUB_TOKEN", "")
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        
        print("\n" + "=" * 80)
        print("验证 LLM Provider 官方 SDK 仓库")
        print("=" * 80)
        
        # 构建并验证资源列表
        resources = []
        invalid_repos = []
        current_provider = None
        
        for provider_code, repo_list in PROVIDER_OFFICIAL_REPOS.items():
            # 打印 provider 分组头
            meta = PROVIDER_META.get(provider_code, {})
            company = meta.get("company", provider_code)
            country = meta.get("country", "")
            
            if current_provider != provider_code:
                print(f"\n【{company}】{country}")
                current_provider = provider_code
            
            provider_info = next(
                (p for p in LLM_PROVIDER_REGISTRY if p["code"] == provider_code),
                None
            )
            for repo_info in repo_list:
                repo_full = repo_info["repo"]
                # 验证仓库是否存在
                api_url = f"https://api.github.com/repos/{repo_full}"
                try:
                    resp = requests.get(api_url, headers=headers, timeout=10)
                    if resp.status_code == 200:
                        repo_data = resp.json()
                        stars = repo_data.get("stargazers_count", 0)
                        updated_at = repo_data.get("updated_at", "")
                        # 格式化更新日期
                        if updated_at:
                            dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                            updated_str = dt.strftime("%Y-%m-%d")
                        else:
                            updated_str = "N/A"
                        
                        print(f"  ✓ {repo_full:<45} ⭐{stars:<8} 📅 {updated_str}")
                        
                        resources.append({
                            "url": f"https://github.com/{repo_full}",
                            "name": repo_full.split("/")[-1],
                            "description": repo_info["desc"],
                            "category": "sdk",
                            "source": "official",
                            "repo": repo_full,
                            "platform": "github",
                            "tags": [provider_code],
                            "metadata": {
                                "provider": provider_code,
                                "provider_name": provider_info["name"] if provider_info else company,
                                "company": company,
                                "country": country,
                                "console_url": provider_info["console_url"] if provider_info else None,
                                "docs_url": provider_info["docs_url"] if provider_info else None,
                                "free_tier": provider_info["free_tier"] if provider_info else None,
                                "env_key": provider_info["env_key"] if provider_info else None,
                                "stars": stars,
                                "updated_at": updated_at,
                            },
                            "is_active": True,
                        })
                    else:
                        print(f"  ✗ {repo_full:<45} - 不存在或无法访问")
                        invalid_repos.append(repo_full)
                except Exception as e:
                    print(f"  ✗ {repo_full:<45} - 请求失败: {e}")
                    invalid_repos.append(repo_full)
        
        print(f"\n" + "=" * 80)
        print(f"验证完成: {len(resources)} 个有效, {len(invalid_repos)} 个无效")
        
        if invalid_repos:
            print("\n无效仓库:")
            for repo in invalid_repos:
                print(f"  - {repo}")
        
        # 保存到文件
        output_path = Path(__file__).parent.parent / "raw_data" / "raw_llm_providers_urls.py"
        self._save_to_file(output_path, resources)
        
        return ScriptResult(
            success=True,
            message=f"Saved {len(resources)} verified repos",
            created=len(resources),
            updated=0,
            deleted=0,
        )
    
    def _save_to_file(self, path: Path, resources: list[dict]) -> None:
        """保存资源到 Python 文件（格式化输出）"""
        lines = [
            "# llm_providers 领域 URL 资源 - 官方 SDK 仓库",
            "from typing import Any",
            "",
            "RAW_LLM_PROVIDERS_URLS: list[dict[str, Any]] = [",
        ]
        
        for r in resources:
            lines.append("    {")
            lines.append(f'        "url": "{r["url"]}",')
            lines.append(f'        "name": "{r["name"]}",')
            lines.append(f'        "description": "{r["description"]}",')
            lines.append(f'        "category": "{r["category"]}",')
            lines.append(f'        "source": "{r["source"]}",')
            lines.append(f'        "repo": "{r["repo"]}",')
            lines.append(f'        "platform": "{r["platform"]}",')
            lines.append(f'        "tags": {r["tags"]},')
            lines.append(f'        "metadata": {{')
            lines.append(f'            "provider": "{r["metadata"]["provider"]}",')
            lines.append(f'            "provider_name": "{r["metadata"]["provider_name"]}",')
            if r["metadata"].get("company"):
                lines.append(f'            "company": "{r["metadata"]["company"]}",')
            if r["metadata"].get("country"):
                lines.append(f'            "country": "{r["metadata"]["country"]}",')
            if r["metadata"].get("console_url"):
                lines.append(f'            "console_url": "{r["metadata"]["console_url"]}",')
                lines.append(f'            "docs_url": "{r["metadata"]["docs_url"]}",')
                lines.append(f'            "free_tier": "{r["metadata"]["free_tier"]}",')
                lines.append(f'            "env_key": "{r["metadata"]["env_key"]}",')
            if r["metadata"].get("stars") is not None:
                lines.append(f'            "stars": {r["metadata"]["stars"]},')
            if r["metadata"].get("updated_at"):
                lines.append(f'            "updated_at": "{r["metadata"]["updated_at"]}",')
            lines.append(f'        }},')
            lines.append(f'        "is_active": {r["is_active"]},')
            lines.append("    },")
        
        lines.append("]")
        lines.append("")
        
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"\n[INFO] 已保存到 {path}")


def print_provider_info():
    """打印 provider 注册信息"""
    print("\n" + "=" * 60)
    print("免费 LLM Provider 注册信息")
    print("=" * 60)
    for p in LLM_PROVIDER_REGISTRY:
        print(f"\n【{p['name']}】")
        print(f"  获取 Key: {p['console_url']}")
        print(f"  文档: {p['docs_url']}")
        print(f"  免费额度: {p['free_tier']}")
        print(f"  环境变量: {p['env_key']}")
        print(f"  模型: {', '.join(p['models'][:3])}")


def print_official_repos():
    """打印官方仓库列表"""
    print("\n" + "=" * 60)
    print("Provider 官方 GitHub 仓库")
    print("=" * 60)
    for provider, repos in PROVIDER_OFFICIAL_REPOS.items():
        print(f"\n【{provider}】")
        for repo in repos:
            print(f"  https://github.com/{repo['repo']}")
            print(f"    {repo['desc']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--info":
            print_provider_info()
        elif sys.argv[1] == "--repos":
            print_official_repos()
        elif sys.argv[1] == "--all":
            print_provider_info()
            print_official_repos()
        else:
            print("用法:")
            print("  --info   显示免费 provider 注册信息")
            print("  --repos  显示官方 GitHub 仓库")
            print("  --all    显示全部信息")
            print("  (无参数) 运行资源发现")
    else:
        # 运行资源发现
        script = DiscoverLLMProvidersScript(verbose=True)
        result = script.run()
        print(result)
