"""Prompt 服务 - 使用 Document Store"""
import csv
import io
import re
import requests

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.enum import RAW_GITHUB
from src.common.helper import paginate

# Document types
DOC_TYPE_PROMPT = "admin_prompt"
DOC_TYPE_PROMPT_LABEL = "admin_prompt_label"

CATEGORY_MAP = {
    "act as": "roleplay", "pretend": "roleplay", "simulate": "roleplay",
    "write": "writing", "essay": "writing", "story": "writing", "article": "writing",
    "code": "coding", "programming": "coding", "developer": "coding", "python": "coding",
    "business": "business", "marketing": "business", "sales": "business",
    "teach": "education", "learn": "education", "tutor": "education",
    "creative": "creative", "brainstorm": "creative", "design": "creative",
    "analyze": "analysis", "research": "analysis", "data": "analysis",
    "translate": "translation", "language": "translation",
    "assistant": "assistant", "helper": "assistant",
}


class PromptService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    # ========== 分类管理 ==========
    def get_category_labels(self, type: str = "category") -> list[dict]:
        """获取分类/来源标签列表"""
        docs = self.store.find(DOC_TYPE_PROMPT_LABEL, status="active")
        labels = [
            self._label_to_response(doc)
            for doc in docs
            if doc["data"].get("type") == type and doc["data"].get("is_active", True)
        ]
        labels.sort(key=lambda x: x.get("sort_order", 0))
        return labels

    def get_all_category_labels(self) -> dict:
        """获取所有标签（分类+来源）"""
        docs = self.store.find(DOC_TYPE_PROMPT_LABEL, status="active")
        result = {"categories": [], "sources": []}
        for doc in docs:
            data = doc["data"]
            if not data.get("is_active", True):
                continue
            item = self._label_to_response(doc)
            if data.get("type") == "category":
                result["categories"].append(item)
            else:
                result["sources"].append(item)
        result["categories"].sort(key=lambda x: x.get("sort_order", 0))
        result["sources"].sort(key=lambda x: x.get("sort_order", 0))
        return result

    def create_category_label(self, data: dict) -> dict:
        """创建分类/来源标签"""
        docs = self.store.find(DOC_TYPE_PROMPT_LABEL, status="active")
        for doc in docs:
            if doc["data"].get("type") == data.get("type") and doc["data"].get("code") == data.get("code"):
                raise AppError(AppErrorCode.DUPLICATE, f"Label {data.get('code')} already exists")
        doc = self.store.create(DOC_TYPE_PROMPT_LABEL, data)
        return self._label_to_response(doc)

    def update_category_label(self, id: str, data: dict) -> dict:
        """更新分类/来源标签"""
        doc = self.store.update(id, data_updates=data)
        if not doc:
            raise AppError(AppErrorCode.NOT_FOUND, f"Label {id} not found")
        return self._label_to_response(doc)

    def delete_category_label(self, id: str) -> None:
        """删除分类/来源标签"""
        self.store.delete(id)

    # ========== Prompts 管理 ==========
    def find_all(
        self, page: int = 1, limit: int = 20,
        category: str | None = None, source: str | None = None, search: str | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE_PROMPT, status="active", limit=1000)
        
        filtered = []
        for doc in docs:
            data = doc["data"]
            if category and data.get("category") != category:
                continue
            if source and data.get("source") != source:
                continue
            if search:
                search_lower = search.lower()
                name = (data.get("name") or "").lower()
                desc = (data.get("description") or "").lower()
                if search_lower not in name and search_lower not in desc:
                    continue
            filtered.append(doc)
        
        filtered.sort(key=lambda x: (
            not x["data"].get("is_active", True),
            x.get("updated_at") or ""
        ), reverse=True)
        
        paged, total = paginate(filtered, page, limit)
        
        return [self._prompt_to_response(doc) for doc in paged], total

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_PROMPT or doc["status"] == "deleted":
            return None
        return self._prompt_to_response(doc)

    def find_by_name_and_source(self, name: str, source: str) -> dict | None:
        docs = self.store.find(DOC_TYPE_PROMPT, status="active")
        for doc in docs:
            if doc["data"].get("name") == name and doc["data"].get("source") == source:
                return self._prompt_to_response(doc)
        return None

    def get_categories(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE_PROMPT, status="active")
        counts: dict[str, int] = {}
        for doc in docs:
            cat = doc["data"].get("category") or "general"
            counts[cat] = counts.get(cat, 0) + 1
        return [{"category": c, "count": n} for c, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_sources(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE_PROMPT, status="active")
        counts: dict[str, int] = {}
        for doc in docs:
            src = doc["data"].get("source") or ""
            counts[src] = counts.get(src, 0) + 1
        return [{"source": s, "count": n} for s, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_stats(self) -> dict:
        docs = self.store.find(DOC_TYPE_PROMPT, status="active")
        total = len(docs)
        active = sum(1 for doc in docs if doc["data"].get("is_active", True))
        return {
            "total": total, "active": active, "inactive": total - active,
            "categories": self.get_categories(), "sources": self.get_sources(),
        }

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt {id} not found")
        doc = self.store.update(id, data_updates=data)
        return self._prompt_to_response(doc)

    def toggle_active(self, id: str) -> dict:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_PROMPT:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt {id} not found")
        new_status = not doc["data"].get("is_active", True)
        updated = self.store.update(id, data_updates={"is_active": new_status})
        return self._prompt_to_response(updated)

    def _categorize(self, title: str, content: str) -> str:
        text = (title + " " + content).lower()
        for keyword, category in CATEGORY_MAP.items():
            if keyword in text:
                return category
        return "general"

    def sync_from_github(self) -> dict:
        """从 GitHub 同步 Prompts"""
        synced = 0
        errors = []

        # 1. awesome-chatgpt-prompts (CSV)
        try:
            url = f"{RAW_GITHUB}/f/awesome-chatgpt-prompts/main/prompts.csv"
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                reader = csv.DictReader(io.StringIO(resp.text))
                for row in reader:
                    title = row.get("act", "").strip()
                    content = row.get("prompt", "").strip()
                    if not title or not content:
                        continue
                    synced += self._upsert_prompt(title, f"Act as {title}", content,
                        self._categorize(title, content), "awesome-chatgpt-prompts", "f/awesome-chatgpt-prompts")
        except Exception as e:
            errors.append({"source": "awesome-chatgpt-prompts", "error": str(e)})

        # 2. awesome-ai-system-prompts
        try:
            api_url = "https://api.github.com/repos/dontriskit/awesome-ai-system-prompts/contents"
            resp = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=30)
            if resp.status_code == 200:
                for item in resp.json():
                    if item["type"] != "dir" or item["name"] in ["LICENSE", "README.md"]:
                        continue
                    folder = item["name"]
                    folder_resp = requests.get(
                        f"https://api.github.com/repos/dontriskit/awesome-ai-system-prompts/contents/{folder}",
                        headers={"Accept": "application/vnd.github.v3+json"}, timeout=10)
                    if folder_resp.status_code != 200:
                        continue
                    for f in folder_resp.json():
                        if not f["name"].endswith(".md"):
                            continue
                        file_resp = requests.get(f["download_url"], timeout=10)
                        if file_resp.status_code != 200:
                            continue
                        content = re.sub(r'^---\n.*?\n---\n', '', file_resp.text, flags=re.DOTALL).strip()
                        if len(content) < 100:
                            continue
                        title = f"{folder} - {f['name'].replace('.md', '').replace('-', ' ').title()}"
                        synced += self._upsert_prompt(title[:100], f"System prompt for {folder}",
                            content[:8000], "system", "awesome-system-prompts", "dontriskit/awesome-ai-system-prompts")
        except Exception as e:
            errors.append({"source": "awesome-system-prompts", "error": str(e)})

        return {"synced": synced, "errors": errors}

    def _upsert_prompt(self, name: str, desc: str, content: str, category: str, source: str, repo: str) -> int:
        existing = self.find_by_name_and_source(name, source)
        data = {
            "name": name,
            "description": desc,
            "template": content,
            "category": category,
            "source": source,
            "repo": repo,
            "is_active": True,
        }
        if existing:
            self.store.update(existing["id"], data_updates=data)
        else:
            self.store.create(DOC_TYPE_PROMPT, data)
        return 1

    def _prompt_to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "name": data.get("name"),
            "description": data.get("description"),
            "template": data.get("template"),
            "template_en": data.get("template_en"),
            "category": data.get("category"),
            "source": data.get("source"),
            "repo": data.get("repo"),
            "is_active": data.get("is_active", True),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }

    def _label_to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "type": data.get("type"),
            "code": data.get("code"),
            "name": data.get("name"),
            "name_en": data.get("name_en"),
            "color": data.get("color"),
            "icon": data.get("icon"),
            "sort_order": data.get("sort_order", 0),
            "is_active": data.get("is_active", True),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
