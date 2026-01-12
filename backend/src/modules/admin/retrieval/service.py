"""Retrieval Engine Service - 知识检索引擎管理 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode


DOC_TYPE_ENGINE = "admin_retrieval_engine"
DOC_TYPE_DOMAIN_CONFIG = "admin_retrieval_domain_config"


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
        self.store = DocumentStore()

    # ========== 引擎管理 ==========
    def find_all_engines(
        self,
        page: int = 1,
        limit: int = 20,
        type: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_ENGINE, status="active")
        
        # 过滤
        engines = []
        for doc in docs:
            data = doc["data"]
            if type and data.get("type") != type:
                continue
            if is_active is not None and data.get("is_active") != is_active:
                continue
            engines.append(self._engine_to_response(doc))
        
        # 排序
        engines.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 分页
        total = len(engines)
        start = (page - 1) * limit
        end = start + limit
        
        return engines[start:end], total

    def find_engine_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_ENGINE or doc["status"] == "deleted":
            return None
        return self._engine_to_response(doc)

    def find_engine_by_name(self, name: str) -> dict | None:
        docs = self.store.find(DOC_TYPE_ENGINE, status="active")
        for doc in docs:
            if doc["data"].get("name") == name:
                return self._engine_to_response(doc)
        return None

    def get_default_engine(self) -> dict | None:
        docs = self.store.find(DOC_TYPE_ENGINE, status="active")
        for doc in docs:
            data = doc["data"]
            if data.get("is_default") and data.get("is_active"):
                return self._engine_to_response(doc)
        return None

    def get_active_engines(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE_ENGINE, status="active")
        engines = []
        for doc in docs:
            if doc["data"].get("is_active"):
                engines.append(self._engine_to_response(doc))
        engines.sort(key=lambda x: x.get("display_name", ""))
        return engines

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

        doc = self.store.create(DOC_TYPE_ENGINE, {
            "name": data["name"],
            "display_name": data["display_name"],
            "type": engine_type,
            "description": data.get("description", ""),
            "config": data.get("config", {}),
            "is_active": data.get("is_active", True),
            "is_default": False,
        })
        
        return self._engine_to_response(doc)

    def update_engine(self, id: str, data: dict) -> dict:
        existing = self.find_engine_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {id} not found")

        update_data = {k: v for k, v in data.items() if v is not None}
        doc = self.store.update(id, data_updates=update_data)
        return self._engine_to_response(doc)

    def delete_engine(self, id: str) -> None:
        existing = self.find_engine_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {id} not found")

        if existing.get("is_default"):
            raise AppError(
                AppErrorCode.VALIDATION_ERROR, "Cannot delete default engine"
            )

        self.store.delete(id)

    def set_default_engine(self, engine_id: str) -> dict:
        engine = self.find_engine_by_id(engine_id)
        if not engine:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {engine_id} not found")

        if not engine.get("is_active"):
            raise AppError(
                AppErrorCode.VALIDATION_ERROR, "Cannot set inactive engine as default"
            )

        # 清除旧默认
        docs = self.store.find(DOC_TYPE_ENGINE, status="active")
        for doc in docs:
            if doc["data"].get("is_default"):
                self.store.update(doc["id"], data_updates={"is_default": False})

        # 设置新默认
        doc = self.store.update(engine_id, data_updates={"is_default": True})
        return self._engine_to_response(doc)


    # ========== 领域配置 ==========
    def get_domain_configs(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE_DOMAIN_CONFIG, status="active")
        configs = []
        for doc in docs:
            config = self._domain_config_to_response(doc)
            # 获取关联的引擎信息
            engine_id = doc["data"].get("engine_id")
            if engine_id:
                engine = self.find_engine_by_id(engine_id)
                config["engine"] = engine
            configs.append(config)
        configs.sort(key=lambda x: x.get("domain", ""))
        return configs

    def get_domain_engine(self, domain: str) -> dict | None:
        docs = self.store.find(DOC_TYPE_DOMAIN_CONFIG, status="active")
        for doc in docs:
            if doc["data"].get("domain") == domain:
                engine_id = doc["data"].get("engine_id")
                if engine_id:
                    return self.find_engine_by_id(engine_id)
        return self.get_default_engine()

    def set_domain_engine(self, domain: str, engine_id: str) -> dict:
        engine = self.find_engine_by_id(engine_id)
        if not engine:
            raise AppError(AppErrorCode.NOT_FOUND, f"Engine {engine_id} not found")

        # 查找现有配置
        docs = self.store.find(DOC_TYPE_DOMAIN_CONFIG, status="active")
        existing_doc = None
        for doc in docs:
            if doc["data"].get("domain") == domain:
                existing_doc = doc
                break

        if existing_doc:
            # 更新
            doc = self.store.update(existing_doc["id"], data_updates={"engine_id": engine_id})
        else:
            # 创建
            doc = self.store.create(DOC_TYPE_DOMAIN_CONFIG, {
                "domain": domain,
                "engine_id": engine_id,
            })
        
        return self._domain_config_to_response(doc)

    def delete_domain_config(self, domain: str) -> None:
        docs = self.store.find(DOC_TYPE_DOMAIN_CONFIG, status="active")
        for doc in docs:
            if doc["data"].get("domain") == domain:
                self.store.delete(doc["id"])
                return

    # ========== 统计 ==========
    def get_stats(self) -> dict:
        engine_docs = self.store.find(DOC_TYPE_ENGINE, status="active")
        domain_docs = self.store.find(DOC_TYPE_DOMAIN_CONFIG, status="active")

        total = len(engine_docs)
        active = sum(1 for e in engine_docs if e["data"].get("is_active"))
        by_type: dict[str, int] = {}

        for doc in engine_docs:
            t = doc["data"].get("type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1

        return {
            "total": total,
            "active": active,
            "by_type": [{"type": k, "count": v} for k, v in by_type.items()],
            "domain_configs": len(domain_docs),
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

    def _engine_to_response(self, doc: dict) -> dict:
        """转换 engine 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "name": data.get("name"),
            "display_name": data.get("display_name"),
            "type": data.get("type"),
            "description": data.get("description"),
            "config": data.get("config", {}),
            "is_active": data.get("is_active", True),
            "is_default": data.get("is_default", False),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }

    def _domain_config_to_response(self, doc: dict) -> dict:
        """转换 domain config 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "domain": data.get("domain"),
            "engine_id": data.get("engine_id"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
