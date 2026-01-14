# AI 相关 GitHub 数据源
from typing import Any, Dict, List

# llm_models - 大语言模型
LLM_MODELS_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/Hannibal046/Awesome-LLM", "name": "Awesome LLM", "description": "大语言模型资源汇总", "source_type": "github", "domain_code": "llm_models", "tags": ["llm", "ai", "awesome", "resources"]},
    {"url": "https://github.com/steven2358/awesome-generative-ai", "name": "Awesome Generative AI", "description": "生成式AI资源精选", "source_type": "github", "domain_code": "llm_models", "tags": ["generative-ai", "ai", "awesome"]},
    {"url": "https://github.com/ollama/ollama", "name": "Ollama", "description": "本地运行大语言模型", "source_type": "github", "domain_code": "llm_models", "tags": ["ollama", "local", "llm", "inference"]},
    {"url": "https://github.com/vllm-project/vllm", "name": "vLLM", "description": "高性能 LLM 推理引擎", "source_type": "github", "domain_code": "llm_models", "tags": ["vllm", "inference", "performance"]},
]

# agents - AI Agent 框架
AGENTS_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/e2b-dev/awesome-ai-agents", "name": "Awesome AI Agents", "description": "AI Agent 资源汇总", "source_type": "github", "domain_code": "agents", "tags": ["ai-agent", "awesome", "automation"]},
    {"url": "https://github.com/langchain-ai/langchain", "name": "LangChain", "description": "构建 LLM 应用的框架", "source_type": "github", "domain_code": "agents", "tags": ["langchain", "llm", "framework", "agent"]},
    {"url": "https://github.com/microsoft/autogen", "name": "AutoGen", "description": "微软开源的多智能体对话框架", "source_type": "github", "domain_code": "agents", "tags": ["autogen", "microsoft", "multi-agent"]},
    {"url": "https://github.com/crewAIInc/crewAI", "name": "CrewAI", "description": "角色扮演式多智能体协作框架", "source_type": "github", "domain_code": "agents", "tags": ["crewai", "agent", "multi-agent"]},
    {"url": "https://github.com/langchain-ai/langgraph", "name": "LangGraph", "description": "有状态多Agent编排框架", "source_type": "github", "domain_code": "agents", "tags": ["agent", "langchain", "graph", "workflow"]},
    {"url": "https://github.com/camel-ai/camel", "name": "CAMEL (OWL)", "description": "首个LLM多智能体框架", "source_type": "github", "domain_code": "agents", "tags": ["agent", "multi-agent", "camel", "owl"]},
    {"url": "https://github.com/langgenius/dify", "name": "Dify", "description": "开源LLM应用开发平台", "source_type": "github", "domain_code": "agents", "tags": ["agent", "workflow", "llm-platform"]},
    {"url": "https://github.com/huggingface/smolagents", "name": "Smolagents", "description": "Hugging Face 轻量级Agent框架", "source_type": "github", "domain_code": "agents", "tags": ["agent", "huggingface", "lightweight"]},
    {"url": "https://github.com/mannaandpoem/OpenManus", "name": "OpenManus", "description": "开源通用Agent框架", "source_type": "github", "domain_code": "agents", "tags": ["agent", "manus", "general-purpose"]},
    {"url": "https://github.com/jd-opensource/joyagent-jdgenie", "name": "JoyAgent-JDGenie", "description": "京东开源的端到端多智能体产品", "source_type": "github", "domain_code": "agents", "tags": ["agent", "multi-agent", "jd"]},
]

# prompts - 提示词工程
PROMPTS_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/anthropics/anthropic-cookbook", "name": "Anthropic Cookbook", "description": "Anthropic API 使用示例和最佳实践", "source_type": "github", "domain_code": "prompts", "tags": ["claude", "anthropic", "cookbook"]},
    {"url": "https://github.com/f/awesome-chatgpt-prompts", "name": "Awesome ChatGPT Prompts", "description": "ChatGPT 提示词精选集合", "source_type": "github", "domain_code": "prompts", "tags": ["chatgpt", "prompts", "awesome"]},
    {"url": "https://github.com/dair-ai/Prompt-Engineering-Guide", "name": "Prompt Engineering Guide", "description": "提示工程指南和最佳实践", "source_type": "github", "domain_code": "prompts", "tags": ["prompt-engineering", "guide"]},
]

# skills - Claude Skills
SKILLS_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/anthropics/skills", "name": "Anthropic Skills", "description": "Anthropic 官方 Claude Skills 仓库", "source_type": "github", "domain_code": "skills", "tags": ["claude", "skills", "anthropic"]},
]

# retrieval - 检索引擎
RETRIEVAL_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/run-llama/llama_index", "name": "LlamaIndex", "description": "LLM 数据框架，支持多种数据源的索引和检索", "source_type": "github", "domain_code": "retrieval", "tags": ["llamaindex", "rag", "index"]},
    {"url": "https://github.com/chroma-core/chroma", "name": "Chroma", "description": "开源向量数据库，专为 AI 应用设计", "source_type": "github", "domain_code": "retrieval", "tags": ["chroma", "vector-db", "embedding"]},
    {"url": "https://github.com/qdrant/qdrant", "name": "Qdrant", "description": "高性能向量搜索引擎", "source_type": "github", "domain_code": "retrieval", "tags": ["qdrant", "vector-db", "search"]},
    {"url": "https://github.com/weaviate/weaviate", "name": "Weaviate", "description": "开源向量数据库，支持语义搜索", "source_type": "github", "domain_code": "retrieval", "tags": ["weaviate", "vector-db"]},
    {"url": "https://github.com/milvus-io/milvus", "name": "Milvus", "description": "云原生向量数据库", "source_type": "github", "domain_code": "retrieval", "tags": ["milvus", "vector-db", "cloud-native"]},
    {"url": "https://github.com/pgvector/pgvector", "name": "pgvector", "description": "PostgreSQL 向量扩展", "source_type": "github", "domain_code": "retrieval", "tags": ["pgvector", "postgresql", "vector"]},
]

# 汇总导出
AI_GITHUB_SOURCES: List[Dict[str, Any]] = []
AI_GITHUB_SOURCES.extend(LLM_MODELS_SOURCES)
AI_GITHUB_SOURCES.extend(AGENTS_SOURCES)
AI_GITHUB_SOURCES.extend(PROMPTS_SOURCES)
AI_GITHUB_SOURCES.extend(SKILLS_SOURCES)
AI_GITHUB_SOURCES.extend(RETRIEVAL_SOURCES)
