# Agent 框架种子数据
from typing import Any, Dict, List

AGENT_FRAMEWORKS: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/jd-opensource/joyagent-jdgenie",
        "name": "JoyAgent-JDGenie",
        "description": "京东开源的端到端多智能体产品，支持报告生成、代码、PPT等多种Agent",
        "tags": ["agent", "multi-agent", "jd", "gaia", "report", "ppt"],
    },
    {
        "url": "https://github.com/microsoft/autogen",
        "name": "AutoGen",
        "description": "微软开源的多智能体对话框架，支持多Agent协作完成复杂任务",
        "tags": ["agent", "multi-agent", "microsoft", "conversation"],
    },
    {
        "url": "https://github.com/crewAIInc/crewAI",
        "name": "CrewAI",
        "description": "角色扮演式多智能体协作框架，让AI Agent像团队一样协作",
        "tags": ["agent", "multi-agent", "crew", "role-playing"],
    },
    {
        "url": "https://github.com/langchain-ai/langgraph",
        "name": "LangGraph",
        "description": "LangChain 团队的有状态多Agent编排框架，支持循环和条件逻辑",
        "tags": ["agent", "langchain", "graph", "workflow"],
    },
    {
        "url": "https://github.com/camel-ai/camel",
        "name": "CAMEL (OWL)",
        "description": "首个LLM多智能体框架，支持角色扮演和任务协作",
        "tags": ["agent", "multi-agent", "camel", "owl", "role-playing"],
    },
    {
        "url": "https://github.com/langgenius/dify",
        "name": "Dify",
        "description": "开源LLM应用开发平台，支持Agent和Workflow可视化编排",
        "tags": ["agent", "workflow", "llm-platform", "low-code"],
    },
    {
        "url": "https://github.com/huggingface/smolagents",
        "name": "Smolagents",
        "description": "Hugging Face 的轻量级Agent框架，简洁易用",
        "tags": ["agent", "huggingface", "lightweight"],
    },
    {
        "url": "https://github.com/mannaandpoem/OpenManus",
        "name": "OpenManus",
        "description": "开源通用Agent框架，xManus的开源实现",
        "tags": ["agent", "manus", "general-purpose"],
    },
]
