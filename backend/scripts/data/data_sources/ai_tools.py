# AI 工具相关数据源 - 按类型分类
from typing import Any, Dict, List

# Prompts - 提示词资源
PROMPTS_SOURCES: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/anthropics/anthropic-cookbook",
        "name": "Anthropic Cookbook",
        "description": "Anthropic API 使用示例和最佳实践",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["claude", "anthropic", "cookbook", "api", "prompts"],
    },
    {
        "url": "https://github.com/f/awesome-chatgpt-prompts",
        "name": "Awesome ChatGPT Prompts",
        "description": "ChatGPT 提示词精选集合",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["chatgpt", "prompts", "awesome"],
    },
    {
        "url": "https://github.com/dair-ai/Prompt-Engineering-Guide",
        "name": "Prompt Engineering Guide",
        "description": "提示工程指南和最佳实践",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["prompt-engineering", "guide", "tutorial"],
    },
]

# Skills - Claude Skills 资源
SKILLS_SOURCES: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/anthropics/skills",
        "name": "Anthropic Skills",
        "description": "Anthropic 官方 Claude Skills 仓库",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["claude", "skills", "anthropic", "official"],
    },
]

# Agents - AI Agent 框架和资源
AGENTS_SOURCES: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/e2b-dev/awesome-ai-agents",
        "name": "Awesome AI Agents",
        "description": "AI Agent 资源汇总",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["ai-agent", "awesome", "automation"],
    },
    {
        "url": "https://github.com/langchain-ai/langchain",
        "name": "LangChain",
        "description": "构建 LLM 应用的框架",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["langchain", "llm", "framework", "agent"],
    },
    {
        "url": "https://github.com/microsoft/autogen",
        "name": "AutoGen",
        "description": "微软多智能体对话框架",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["autogen", "microsoft", "multi-agent"],
    },
    {
        "url": "https://github.com/crewAIInc/crewAI",
        "name": "CrewAI",
        "description": "AI Agent 协作框架",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["crewai", "agent", "collaboration"],
    },
]

# Engines - LLM 模型和引擎资源
ENGINES_SOURCES: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/Hannibal046/Awesome-LLM",
        "name": "Awesome LLM",
        "description": "大语言模型资源汇总",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["llm", "ai", "awesome", "resources"],
    },
    {
        "url": "https://github.com/steven2358/awesome-generative-ai",
        "name": "Awesome Generative AI",
        "description": "生成式AI资源精选",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["generative-ai", "ai", "awesome"],
    },
    {
        "url": "https://github.com/ollama/ollama",
        "name": "Ollama",
        "description": "本地运行大语言模型",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["ollama", "local", "llm", "inference"],
    },
    {
        "url": "https://github.com/vllm-project/vllm",
        "name": "vLLM",
        "description": "高性能 LLM 推理引擎",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["vllm", "inference", "performance"],
    },
]

# 合并所有数据源
AI_TOOLS_SOURCES: List[Dict[str, Any]] = (
    PROMPTS_SOURCES + SKILLS_SOURCES + AGENTS_SOURCES + ENGINES_SOURCES
)
