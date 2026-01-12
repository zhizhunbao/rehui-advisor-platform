"""Prompt 服务 - 使用 Supabase API"""
import csv
import io
import re
import requests

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin

RAW_GITHUB = "https://raw.githubusercontent.com"

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
        self.client = get_supabase_admin()
        self.table = "prompt_templates"
        self.category_table = "prompt_categories"

    # ========== 分类管理 ==========
    def get_category_labels(self, type: str = "category") -> list[dict]:
        """获取分类/来源标签列表"""
        response = (
            self.client.table(self.category_table)
            .select("*")
            .eq("type", type)
            .eq("is_active", True)
            .order("sort_order")
            .execute()
        )
        return response.data or []

    def get_all_category_labels(self) -> dict:
        """获取所有标签（分类+来源）"""
        response = (
            self.client.table(self.category_table)
            .select("*")
            .eq("is_active", True)
            .order("sort_order")
            .execute()
        )
        result = {"categories": [], "sources": []}
        for item in response.data or []:
            if item["type"] == "category":
                result["categories"].append(item)
            else:
                result["sources"].append(item)
        return result

    def create_category_label(self, data: dict) -> dict:
        """创建分类/来源标签"""
        existing = (
            self.client.table(self.category_table)
            .select("id")
            .eq("type", data.get("type"))
            .eq("code", data.get("code"))
            .maybe_single()
            .execute()
        )
        if existing.data:
            raise AppError(AppErrorCode.DUPLICATE, f"Label {data.get('code')} already exists")
        response = self.client.table(self.category_table).insert(data).execute()
        return response.data[0]

    def update_category_label(self, id: str, data: dict) -> dict:
        """更新分类/来源标签"""
        response = self.client.table(self.category_table).update(data).eq("id", id).execute()
        if not response.data:
            raise AppError(AppErrorCode.NOT_FOUND, f"Label {id} not found")
        return response.data[0]

    def delete_category_label(self, id: str) -> None:
        """删除分类/来源标签"""
        self.client.table(self.category_table).delete().eq("id", id).execute()

    # ========== Prompts 管理 ==========
    def find_all(
        self, page: int = 1, limit: int = 20,
        category: str | None = None, source: str | None = None, search: str | None = None,
    ) -> tuple[list[dict], int]:
        query = self.client.table(self.table).select("*", count="exact")
        if category:
            query = query.eq("category", category)
        if source:
            query = query.eq("source", source)
        if search:
            query = query.or_(f"name.ilike.%{search}%,description.ilike.%{search}%")
        # 排序：启用的在前，再按更新时间降序
        query = query.order("is_active", desc=True).order("updated_at", desc=True).range((page - 1) * limit, page * limit - 1)
        response = query.execute()
        return response.data, response.count or 0

    def find_by_id(self, id: str) -> dict | None:
        response = self.client.table(self.table).select("*").eq("id", id).maybe_single().execute()
        return response.data

    def get_categories(self) -> list[dict]:
        response = self.client.table(self.table).select("category").execute()
        counts: dict[str, int] = {}
        for item in response.data:
            cat = item.get("category") or "general"
            counts[cat] = counts.get(cat, 0) + 1
        return [{"category": c, "count": n} for c, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_sources(self) -> list[dict]:
        response = self.client.table(self.table).select("source").execute()
        counts: dict[str, int] = {}
        for item in response.data:
            src = item.get("source") or ""
            counts[src] = counts.get(src, 0) + 1
        return [{"source": s, "count": n} for s, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_stats(self) -> dict:
        response = self.client.table(self.table).select("category, source, is_active", count="exact").execute()
        total = response.count or 0
        active = sum(1 for item in response.data if item.get("is_active", True))
        return {
            "total": total, "active": active, "inactive": total - active,
            "categories": self.get_categories(), "sources": self.get_sources(),
        }

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt {id} not found")
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        return response.data[0]

    def toggle_active(self, id: str) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Prompt {id} not found")
        new_status = not existing.get("is_active", True)
        response = self.client.table(self.table).update({"is_active": new_status}).eq("id", id).execute()
        return response.data[0]

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
        existing = self.client.table(self.table).select("id").eq("name", name).eq("source", source).execute()
        data = {"description": desc, "template": content, "category": category, "source": source, "repo": repo}
        if existing.data:
            self.client.table(self.table).update(data).eq("id", existing.data[0]["id"]).execute()
        else:
            data["name"] = name
            data["is_active"] = True
            self.client.table(self.table).insert(data).execute()
        return 1
