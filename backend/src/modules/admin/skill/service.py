"""Skills 服务 - 使用 Document Store"""
import re
import requests

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode

# Document types
DOC_TYPE_SKILL = "admin_skill"
DOC_TYPE_SKILL_LABEL = "admin_skill_label"

# GitHub API
GITHUB_API = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com"
OFFICIAL_REPO = "anthropics/skills"
OFFICIAL_SKILLS_PATH = "skills"

# 分类映射（用于同步时自动分类）
OFFICIAL_CATEGORIES = {
    "docx": "document", "pdf": "document", "pptx": "document", "xlsx": "document",
    "algorithmic-art": "design", "brand-guidelines": "design", "canvas-design": "design",
    "frontend-design": "design", "theme-factory": "design", "web-artifacts-builder": "design",
    "mcp-builder": "development", "webapp-testing": "security",
    "doc-coauthoring": "communication", "internal-comms": "communication",
    "slack-gif-creator": "media", "skill-creator": "tool",
}


class SkillService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    # ========== 分类管理 ==========
    def get_category_labels(self, type: str = "category") -> list[dict]:
        """获取分类/来源标签列表"""
        docs = self.store.find(DOC_TYPE_SKILL_LABEL, status="active")
        labels = [
            self._label_to_response(doc)
            for doc in docs
            if doc["data"].get("type") == type and doc["data"].get("is_active", True)
        ]
        labels.sort(key=lambda x: x.get("sort_order", 0))
        return labels

    def get_all_category_labels(self) -> dict:
        """获取所有标签（分类+来源）"""
        docs = self.store.find(DOC_TYPE_SKILL_LABEL, status="active")
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
        # 检查是否重复
        docs = self.store.find(DOC_TYPE_SKILL_LABEL, status="active")
        for doc in docs:
            if doc["data"].get("type") == data.get("type") and doc["data"].get("code") == data.get("code"):
                raise AppError(AppErrorCode.DUPLICATE, f"Label {data.get('code')} already exists")
        
        doc = self.store.create(DOC_TYPE_SKILL_LABEL, data)
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

    # ========== Skills 管理 ==========
    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        category: str | None = None,
        source: str | None = None,
        search: str | None = None,
    ) -> tuple[list[dict], int]:
        """获取 Skills 列表，支持分页、筛选、搜索"""
        docs = self.store.find(DOC_TYPE_SKILL, status="active", limit=1000)
        
        # 过滤
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
        
        # 排序：启用的在前，再按更新时间降序
        filtered.sort(key=lambda x: (
            not x["data"].get("is_active", True),
            x.get("updated_at") or ""
        ), reverse=True)
        
        # 分页
        total = len(filtered)
        start = (page - 1) * limit
        end = start + limit
        paged = filtered[start:end]
        
        return [self._skill_to_response(doc) for doc in paged], total

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_SKILL or doc["status"] == "deleted":
            return None
        return self._skill_to_response(doc)

    def find_by_name(self, name: str) -> dict | None:
        docs = self.store.find(DOC_TYPE_SKILL, status="active")
        for doc in docs:
            if doc["data"].get("name") == name:
                return self._skill_to_response(doc)
        return None

    def get_categories(self) -> list[dict]:
        """获取所有分类及数量"""
        docs = self.store.find(DOC_TYPE_SKILL, status="active")
        category_counts: dict[str, int] = {}
        for doc in docs:
            cat = doc["data"].get("category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1
        return [
            {"category": cat, "count": count}
            for cat, count in sorted(category_counts.items(), key=lambda x: -x[1])
        ]

    def get_sources(self) -> list[dict]:
        """获取所有来源及数量"""
        docs = self.store.find(DOC_TYPE_SKILL, status="active")
        source_counts: dict[str, int] = {}
        for doc in docs:
            src = doc["data"].get("source", "unknown")
            source_counts[src] = source_counts.get(src, 0) + 1
        return [
            {"source": src, "count": count}
            for src, count in sorted(source_counts.items(), key=lambda x: -x[1])
        ]

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Skill {id} not found")
        doc = self.store.update(id, data_updates=data)
        return self._skill_to_response(doc)

    def toggle_active(self, id: str) -> dict:
        """切换启用/禁用状态"""
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE_SKILL:
            raise AppError(AppErrorCode.NOT_FOUND, f"Skill {id} not found")
        
        new_status = not doc["data"].get("is_active", True)
        updated = self.store.update(id, data_updates={"is_active": new_status})
        return self._skill_to_response(updated)

    def get_stats(self) -> dict:
        """获取统计信息"""
        docs = self.store.find(DOC_TYPE_SKILL, status="active")
        total = len(docs)
        active = sum(1 for doc in docs if doc["data"].get("is_active", True))
        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "categories": self.get_categories(),
            "sources": self.get_sources(),
        }

    # ========== 同步功能 ==========
    def sync_from_github(self) -> dict:
        """从 GitHub 同步官方 Skills"""
        synced = 0
        errors = []

        url = f"{GITHUB_API}/repos/{OFFICIAL_REPO}/contents/{OFFICIAL_SKILLS_PATH}"
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=30)

        if response.status_code != 200:
            raise AppError(AppErrorCode.EXTERNAL_SERVICE_ERROR, f"GitHub API error: {response.status_code}")

        folders = [item for item in response.json() if item["type"] == "dir"]

        for folder in folders:
            skill_name = folder["name"]
            try:
                content = self._fetch_skill_content(OFFICIAL_REPO, folder["path"])
                if not content:
                    continue

                parsed = self._parse_skill_md(content)
                if not parsed["name"]:
                    parsed["name"] = skill_name

                existing = self.find_by_name(skill_name)
                data = {
                    "name": skill_name,
                    "description": parsed["description"],
                    "content": parsed["template"],
                    "category": OFFICIAL_CATEGORIES.get(skill_name, "tool"),
                    "source": "official",
                    "repo": OFFICIAL_REPO,
                    "is_active": True,
                }

                if existing:
                    self.store.update(existing["id"], data_updates=data)
                else:
                    self.store.create(DOC_TYPE_SKILL, data)

                synced += 1
            except Exception as e:
                errors.append({"skill": skill_name, "error": str(e)})

        return {"synced": synced, "errors": errors, "total_checked": len(folders)}

    def _fetch_skill_content(self, repo: str, skill_path: str) -> str | None:
        """获取 SKILL.md 内容"""
        for branch in ["main", "master"]:
            url = f"{RAW_GITHUB}/{repo}/{branch}/{skill_path}/SKILL.md"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
        return None

    def _parse_skill_md(self, content: str) -> dict:
        """解析 SKILL.md"""
        name = ""
        description = ""

        table_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        matches = re.findall(table_pattern, content)
        if len(matches) >= 2:
            for match in matches:
                col1, col2, _ = [m.strip() for m in match]
                if col1.lower() == "name" or col1.startswith("-"):
                    continue
                name = col1
                description = col2
                break

        if not name:
            fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                name_match = re.search(r'name:\s*["\']?([^"\'\n]+)', fm)
                desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)', fm)
                if name_match:
                    name = name_match.group(1).strip()
                if desc_match:
                    description = desc_match.group(1).strip()

        body = re.sub(r'\|[^\n]+\|(\n\|[^\n]+\|)*', '', content)
        body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', body, flags=re.DOTALL)

        return {"name": name, "description": description, "template": body.strip()}

    def _skill_to_response(self, doc: dict) -> dict:
        """转换 skill 为响应格式"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "name": data.get("name"),
            "description": data.get("description"),
            "content": data.get("content"),
            "category": data.get("category"),
            "source": data.get("source"),
            "repo": data.get("repo"),
            "is_active": data.get("is_active", True),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }

    def _label_to_response(self, doc: dict) -> dict:
        """转换 label 为响应格式"""
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
