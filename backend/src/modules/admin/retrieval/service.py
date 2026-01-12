"""Retrieval Engine Service - 知识检索引擎管理"""
from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin


# 支持的引擎类型
ENGINE_TYPES = {
    "keyword_match": {
        "name": "关键词匹配",
        "description": "基于关键词的简单匹配，速度快、零成本",
        "config_schema": {
            "match_mode": ["exact", "fuzzy", "prefix"],
            "max_results": "int",
        },
    },
    "structured_query": {
        "name": "结构化查询",
        "description": "基于分类、标签、元数据的精准查询",
        "config_schema": {
            "use_category": "bool",
            "use_tags": "bool",
            "use_metadata": "bool",
        },
    },
    "rag_vector": {
        "name": "RAG 向量检索",
        "description": "传统 RAG，基于向量相似度检索",
        "config_schema": {
            "embedding_model": "str",
            "top_k": "int",
            "similarity_threshold": "float",
            "chunk_size": "int",
            "chunk_overlap": "int",
        },
    },
    "page_index": {
        "name": "PageIndex 树形推理",
        "description": "基于文档层级结构的推理式检索，适合长文档",
        "config_schema": {
            "tree_depth": "int",
            "reasoning_model": "str",
            "index_storage": "str",
        },
    },
    "agent_tools": {
        "name": "Agent 工具调用",
        "description": "LLM 自主决定调用哪些工具获取信息",
        "config_schema": {
            "available_tools": "list",
            "max_tool_calls": "int",
            "agent_model": "str",
        },
    },
    "realtime_search": {
        "name": "实时网络搜索",
        "description": "实时搜索互联网获取最新信息",
        "config_schema": {
            "search_provider": ["google", "bing", "serper", "tavily"],
            "max_results": "int",
            "include_snippets": "bool",
        },
    },
    "hybrid": {
        "name": "混合引擎",
        "description": "组合多种引擎，取长补短",
        "config_schema": {
            "engines": "list",
            "merge_strategy": ["union", "intersection", "weighted"],
            "weights": "dict",
        },
    },
}


class RetrievalEngineService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "retrieval_engines"
        self.domain_table = "retrieval_domain_configs"

    # ========== 引擎管理 ==========
    def find_all_engines(
        self,
        page: int = 1,
        limit: int = 20,
        type: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.table).select("*", count="exact")

        if type:
            query = query.eq("type", type)
        if is_active is not None:
            query = query.eq("is_active", is_active)

        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def find_engine_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def find_engine_by_name(self, name: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("name", name)
            .maybe_single()
            .execute()
        )
        return response.data

    def get_default_engine(self) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("is_default", True)
            .eq("is_active", True)
            .maybe_single()
            .execute()
        )
        return response.data

    def get_active_engines(self) -> list[dict]:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("is_active", True)
            .order("display_name")
            .execute()
        )
        return response.data

    def get_engine_types(self) -> list[dict]:
        return [
            {"type": k, "name": v["name"], "description": v["description"]}
            for k, v in ENGINE_TYPES.items()
        ]

    def get_engine_type_schema(self, type: str) -> dict:
        if type not in ENGINE_TYPES:
            raise AppError(AppErrorCode.NOT_FOUND, f"Unknown engine type: {type}")
        return ENGINE_TYPES[type]

    def create_engine(self, data: dict) -> dict:
        engine_type = data.get("type")
        if engine_type not in ENGINE_TYPES:
            raise AppError(
                AppErrorCode.VALIDATION_ERROR, f"Invalid engine type: {engine_type}"
            )

        existing = self.find_engine_by_name(data.get("name", ""))
        if existing:
            raise AppError(
                AppErrorCode.DUPLICATE, f"Engine name already exists: {data['name']}"
            )

        insert_data = {
            "name": data["name"],
            "display_name": data["display_name"],
            "type": engine_type,
            "description": data.get("description", ""),
            "config": data.get("config", {}),
            "is_active": data.get("is_active", True),
            "is_default": False,
        }

        response = self.client.table(self.table).insert(insert_data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create engine")
        return response.data[0]

    def update_engine(self, id: str, data: dict) -> dict:
        existing = self.find_engine_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        response = (
            self.client.table(self.table).update(update_data).eq("id", id).execute()
        )
        return response.data[0]

    def delete_engine(self, id: str) -> None:
        existing = self.find_engine_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {id} not found")

        if existing.get("is_default"):
            raise AppError(
                AppErrorCode.VALIDATION_ERROR, "Cannot delete default engine"
            )

        self.client.table(self.table).delete().eq("id", id).execute()

    def set_default_engine(self, engine_id: str) -> dict:
        engine = self.find_engine_by_id(engine_id)
        if not engine:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {engine_id} not found")

        if not engine.get("is_active"):
            raise AppError(
                AppErrorCode.VALIDATION_ERROR, "Cannot set inactive engine as default"
            )

        # 清除旧默认
        self.client.table(self.table).update({"is_default": False}).eq(
            "is_default", True
        ).execute()

        # 设置新默认
        response = (
            self.client.table(self.table)
            .update({"is_default": True})
            .eq("id", engine_id)
            .execute()
        )
        return response.data[0]

    # ========== 领域配置 ==========
    def get_domain_configs(self) -> list[dict]:
        response = (
            self.client.table(self.domain_table)
            .select("*, retrieval_engines(*)")
            .order("domain")
            .execute()
        )
        return response.data

    def get_domain_engine(self, domain: str) -> dict | None:
        response = (
            self.client.table(self.domain_table)
            .select("*, retrieval_engines(*)")
            .eq("domain", domain)
            .maybe_single()
            .execute()
        )
        if response.data:
            return response.data.get("retrieval_engines")
        return self.get_default_engine()

    def set_domain_engine(self, domain: str, engine_id: str) -> dict:
        engine = self.find_engine_by_id(engine_id)
        if not engine:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {engine_id} not found")

        # Upsert 领域配置
        response = (
            self.client.table(self.domain_table)
            .upsert({"domain": domain, "engine_id": engine_id}, on_conflict="domain")
            .execute()
        )
        return response.data[0]

    def delete_domain_config(self, domain: str) -> None:
        self.client.table(self.domain_table).delete().eq("domain", domain).execute()

    # ========== 统计 ==========
    def get_stats(self) -> dict:
        response = self.client.table(self.table).select("type, is_active").execute()

        total = len(response.data)
        active = sum(1 for e in response.data if e.get("is_active"))
        by_type: dict[str, int] = {}

        for item in response.data:
            t = item.get("type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1

        domain_response = self.client.table(self.domain_table).select("domain").execute()

        return {
            "total": total,
            "active": active,
            "by_type": [{"type": k, "count": v} for k, v in by_type.items()],
            "domain_configs": len(domain_response.data),
        }

    # ========== 引擎调用（占位，后续实现具体逻辑） ==========
    def retrieve(self, query: str, domain: str | None = None, engine_id: str | None = None) -> dict:
        """执行检索"""
        # 确定使用哪个引擎
        if engine_id:
            engine = self.find_engine_by_id(engine_id)
        elif domain:
            engine = self.get_domain_engine(domain)
        else:
            engine = self.get_default_engine()

        if not engine:
            raise AppError(AppErrorCode.NOT_FOUND, "No retrieval engine available")

        # 根据引擎类型调用对应实现
        engine_type = engine.get("type")
        config = engine.get("config", {})

        # TODO: 实现各引擎的具体检索逻辑
        result = {
            "engine": engine["name"],
            "engine_type": engine_type,
            "query": query,
            "results": [],
            "metadata": {"config": config},
        }

        return result

    def compare_engines(self, query: str, engine_ids: list[str], context: dict) -> list[dict]:
        """对比多个引擎的检索结果"""
        results = []
        for engine_id in engine_ids:
            try:
                result = self.retrieve(query, engine_id=engine_id)
                results.append({"engine_id": engine_id, "success": True, "result": result})
            except Exception as e:
                results.append({"engine_id": engine_id, "success": False, "error": str(e)})
        return results
