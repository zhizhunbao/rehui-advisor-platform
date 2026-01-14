# 检索引擎数据定义
from typing import Any, Dict, List

RETRIEVAL_ENGINES: List[Dict[str, Any]] = [
    {
        "name": "keyword_match",
        "display_name": "关键词匹配",
        "type": "keyword_match",
        "description": "基于关键词的简单匹配，速度快、零成本，适合简单查询场景",
        "config": {
            "match_mode": "fuzzy",
            "max_results": 10,
            "min_score": 0.3,
        },
        "is_active": True,
        "is_default": False,
    },
    {
        "name": "structured_query",
        "display_name": "结构化查询",
        "type": "structured_query",
        "description": "基于分类、标签、元数据的精准查询，适合数据源分类明确的场景",
        "config": {
            "use_category": True,
            "use_tags": True,
            "use_metadata": True,
            "max_results": 20,
        },
        "is_active": True,
        "is_default": True,
    },
    {
        "name": "rag_vector",
        "display_name": "RAG 向量检索",
        "type": "rag_vector",
        "description": "传统 RAG，基于向量相似度检索，适合通用语义搜索",
        "config": {
            "embedding_model": "text-embedding-3-small",
            "top_k": 5,
            "similarity_threshold": 0.7,
            "chunk_size": 1000,
            "chunk_overlap": 200,
        },
        "is_active": True,
        "is_default": False,
    },
    {
        "name": "page_index",
        "display_name": "PageIndex 树形推理",
        "type": "page_index",
        "description": "基于文档层级结构的推理式检索，适合长文档和专业文档，准确率高",
        "config": {
            "tree_depth": 3,
            "reasoning_model": "gpt-4o-mini",
            "index_storage": "supabase",
            "enable_caching": True,
        },
        "is_active": True,
        "is_default": False,
    },
    {
        "name": "agent_tools",
        "display_name": "Agent 工具调用",
        "type": "agent_tools",
        "description": "LLM 自主决定调用哪些工具获取信息，适合动态数据获取场景",
        "config": {
            "available_tools": [
                "search_data_sources",
                "fetch_github_readme",
                "web_search",
                "query_database",
            ],
            "max_tool_calls": 5,
            "agent_model": "gpt-4o-mini",
        },
        "is_active": True,
        "is_default": False,
    },
    {
        "name": "realtime_search",
        "display_name": "实时网络搜索",
        "type": "realtime_search",
        "description": "实时搜索互联网获取最新信息，适合需要最新数据的场景",
        "config": {
            "search_provider": "serper",
            "max_results": 10,
            "include_snippets": True,
            "search_depth": "basic",
        },
        "is_active": True,
        "is_default": False,
    },
    {
        "name": "hybrid_default",
        "display_name": "混合引擎 (默认)",
        "type": "hybrid",
        "description": "组合结构化查询 + PageIndex，兼顾速度和准确性",
        "config": {
            "engines": ["structured_query", "page_index"],
            "merge_strategy": "weighted",
            "weights": {
                "structured_query": 0.4,
                "page_index": 0.6,
            },
            "fallback_engine": "keyword_match",
        },
        "is_active": True,
        "is_default": False,
    },
]

# 领域默认配置
DOMAIN_ENGINE_CONFIGS: List[Dict[str, str]] = [
    {"domain": "job", "engine_name": "page_index"},
    {"domain": "education", "engine_name": "page_index"},
    {"domain": "investment", "engine_name": "hybrid_default"},
    {"domain": "insurance", "engine_name": "structured_query"},
    {"domain": "house", "engine_name": "realtime_search"},
    {"domain": "car", "engine_name": "structured_query"},
    {"domain": "hotel", "engine_name": "realtime_search"},
    {"domain": "flight", "engine_name": "realtime_search"},
]
