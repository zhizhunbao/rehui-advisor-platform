"""领域配置服务 - 使用 Document Store"""
from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode


DOC_TYPE_PRODUCT_LINE = "product_line"
DOC_TYPE_DOMAIN = "domain"
DOC_TYPE_CATEGORY = "domain_category"
DOC_TYPE_QUESTION = "domain_question"


class ProductLineService:
    """产品线服务"""
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE_PRODUCT_LINE, status="active")
        items = [self._to_response(doc) for doc in docs]
        items.sort(key=lambda x: x.get("sort_order", 0))
        return items

    def find_active(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE_PRODUCT_LINE, status="active")
        items = [
            self._to_response(doc) for doc in docs 
            if doc["data"].get("is_active", True)
        ]
        items.sort(key=lambda x: x.get("sort_order", 0))
        return items

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_PRODUCT_LINE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def find_by_code(self, code: str) -> dict | None:
        docs = self.store.find(DOC_TYPE_PRODUCT_LINE, status="active")
        for doc in docs:
            if doc["data"].get("code") == code:
                return self._to_response(doc)
        return None

    def _to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "code": data.get("code"),
            "name": data.get("name"),
            "name_en": data.get("name_en"),
            "description": data.get("description"),
            "description_en": data.get("description_en"),
            "icon": data.get("icon"),
            "color": data.get("color"),
            "sort_order": data.get("sort_order", 0),
            "is_active": data.get("is_active", True),
        }


class DomainCategoryService:
    """领域分类服务"""
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(self, product_line_id: str | None = None) -> list[dict]:
        docs = self.store.find(DOC_TYPE_CATEGORY, status="active")
        categories = []
        for doc in docs:
            if product_line_id and doc["data"].get("product_line_id") != product_line_id:
                continue
            categories.append(self._to_response(doc))
        categories.sort(key=lambda x: x.get("sort_order", 0))
        return categories

    def find_active(self, product_line_id: str | None = None) -> list[dict]:
        docs = self.store.find(DOC_TYPE_CATEGORY, status="active")
        categories = []
        for doc in docs:
            if not doc["data"].get("is_active", True):
                continue
            if product_line_id and doc["data"].get("product_line_id") != product_line_id:
                continue
            categories.append(self._to_response(doc))
        categories.sort(key=lambda x: x.get("sort_order", 0))
        return categories

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_CATEGORY or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def create(self, data: dict) -> dict:
        doc = self.store.create(DOC_TYPE_CATEGORY, {
            "code": data.get("code"),
            "name": data.get("name"),
            "name_en": data.get("name_en"),
            "description": data.get("description"),
            "description_en": data.get("description_en"),
            "icon": data.get("icon"),
            "color": data.get("color"),
            "sort_order": data.get("sort_order", 0),
            "is_active": True,
        })
        return self._to_response(doc)

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain category {id} not found")
        
        update_data = {k: v for k, v in data.items() if v is not None}
        doc = self.store.update(id, data_updates=update_data)
        return self._to_response(doc)

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain category {id} not found")
        self.store.delete(id)

    def _to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "code": data.get("code"),
            "name": data.get("name"),
            "name_en": data.get("name_en"),
            "description": data.get("description"),
            "description_en": data.get("description_en"),
            "icon": data.get("icon"),
            "color": data.get("color"),
            "product_line_id": data.get("product_line_id"),
            "sort_order": data.get("sort_order", 0),
            "is_active": data.get("is_active", True),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }


class DomainService:
    """领域服务"""
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(self, category_id: str | None = None, is_active: bool | None = None) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_DOMAIN, status="active")
        
        domains = []
        for doc in docs:
            data = doc["data"]
            if category_id and data.get("category_id") != category_id:
                continue
            if is_active is not None and data.get("is_active", True) != is_active:
                continue
            domains.append(self._to_response(doc))
        
        domains.sort(key=lambda x: x.get("sort_order", 0))
        return domains, len(domains)

    def find_active(self) -> list[dict]:
        domains, _ = self.find_all(is_active=True)
        return domains

    def find_grouped_by_category(self, lang: str = "zh", product_line_id: str | None = None) -> list[dict]:
        """按分类分组返回 domains"""
        category_service = DomainCategoryService()
        categories = category_service.find_active(product_line_id)
        
        domains, _ = self.find_all(is_active=True)
        
        # 按 category_id 分组
        domain_map: dict[str, list[dict]] = {}
        for domain in domains:
            cat_id = domain.get("category_id") or "uncategorized"
            if cat_id not in domain_map:
                domain_map[cat_id] = []
            domain_map[cat_id].append(domain)
        
        # 构建结果
        result = []
        for cat in categories:
            cat_domains = domain_map.get(cat["id"], [])
            if not cat_domains:
                continue
            result.append({
                "id": cat["id"],
                "code": cat.get("code"),
                "name": cat.get("name") if lang == "zh" else cat.get("name_en"),
                "icon": cat.get("icon"),
                "color": cat.get("color"),
                "domains": cat_domains,
            })
        
        return result

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_DOMAIN or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def find_by_code(self, code: str) -> dict | None:
        docs = self.store.find(DOC_TYPE_DOMAIN, status="active")
        for doc in docs:
            if doc["data"].get("code") == code:
                return self._to_response(doc)
        return None

    def create(self, data: dict) -> dict:
        if data.get("code"):
            existing = self.find_by_code(data["code"])
            if existing:
                raise AppError(AppErrorCode.DUPLICATE, f"Domain code '{data['code']}' already exists")
        
        doc = self.store.create(DOC_TYPE_DOMAIN, data)
        return self._to_response(doc)

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain {id} not found")
        
        update_data = {k: v for k, v in data.items() if v is not None}
        doc = self.store.update(id, data_updates=update_data)
        return self._to_response(doc)

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain {id} not found")
        self.store.delete(id)

    def _to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "code": data.get("code"),
            "name": data.get("name"),
            "name_en": data.get("name_en"),
            "description": data.get("description"),
            "description_en": data.get("description_en"),
            "icon": data.get("icon"),
            "color": data.get("color"),
            "prompt": data.get("prompt"),
            "prompt_en": data.get("prompt_en"),
            "category_id": data.get("category_id"),
            "route": data.get("route"),
            "sort_order": data.get("sort_order", 0),
            "is_active": data.get("is_active", True),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }


class QuestionService:
    """问题服务"""
    def __init__(self) -> None:
        self.store = DocumentStore()

    def find_all(self, domain_id: str | None = None) -> list[dict]:
        docs = self.store.find(DOC_TYPE_QUESTION, status="active")
        
        questions = []
        for doc in docs:
            if domain_id and doc["data"].get("domain_id") != domain_id:
                continue
            questions.append(self._to_response(doc))
        
        questions.sort(key=lambda x: x.get("sort_order", 0))
        return questions

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_QUESTION or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def create(self, data: dict) -> dict:
        doc = self.store.create(DOC_TYPE_QUESTION, {
            "domain_id": data.get("domain_id"),
            "text": data.get("text"),
            "text_en": data.get("text_en"),
            "type": data.get("type"),
            "options": data.get("options"),
            "sort_order": data.get("sort_order", 0),
            "is_active": True,
        })
        return self._to_response(doc)

    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Question {id} not found")
        self.store.delete(id)

    def _to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "domain_id": data.get("domain_id"),
            "text": data.get("text"),
            "text_en": data.get("text_en"),
            "type": data.get("type"),
            "options": data.get("options") or [],
            "sort_order": data.get("sort_order", 0),
            "is_active": data.get("is_active", True),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
