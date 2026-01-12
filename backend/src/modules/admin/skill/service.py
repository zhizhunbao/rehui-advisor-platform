"""Skills 服务 - 使用 Supabase API"""
import re
import requests

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin

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
        self.client = get_supabase_admin()
        self.table = "skills"
        self.category_table = "skill_categories"

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
        query = self.client.table(self.table).select("*", count="exact")

        # 筛选条件
        if category:
            query = query.eq("category", category)
        if source:
            query = query.eq("source", source)
        if search:
            query = query.or_(f"name.ilike.%{search}%,description.ilike.%{search}%")

        # 排序和分页：启用的在前，再按更新时间降序
        query = query.order("is_active", desc=True).order("updated_at", desc=True).range((page - 1) * limit, page * limit - 1)

        response = query.execute()
        return response.data, response.count or 0

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def find_by_name(self, name: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("name", name)
            .maybe_single()
            .execute()
        )
        return response.data

    def get_categories(self) -> list[dict]:
        """获取所有分类及数量"""
        response = self.client.table(self.table).select("category").execute()
        
        # 统计每个分类的数量
        category_counts: dict[str, int] = {}
        for item in response.data:
            cat = item.get("category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        return [
            {"category": cat, "count": count}
            for cat, count in sorted(category_counts.items(), key=lambda x: -x[1])
        ]

    def get_sources(self) -> list[dict]:
        """获取所有来源及数量"""
        response = self.client.table(self.table).select("source").execute()
        
        source_counts: dict[str, int] = {}
        for item in response.data:
            src = item.get("source", "unknown")
            source_counts[src] = source_counts.get(src, 0) + 1
        
        return [
            {"source": src, "count": count}
            for src, count in sorted(source_counts.items(), key=lambda x: -x[1])
        ]

    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Skill {id} not found")
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        return response.data[0]

    def toggle_active(self, id: str) -> dict:
        """切换启用/禁用状态"""
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Skill {id} not found")

        new_status = not existing.get("is_active", True)
        response = (
            self.client.table(self.table)
            .update({"is_active": new_status})
            .eq("id", id)
            .execute()
        )
        return response.data[0]

    def get_stats(self) -> dict:
        """获取统计信息"""
        response = (
            self.client.table(self.table)
            .select("category, source, is_active", count="exact")
            .execute()
        )
        
        total = response.count or 0
        active = sum(1 for item in response.data if item.get("is_active", True))
        
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

        # 获取官方 skills 目录
        url = f"{GITHUB_API}/repos/{OFFICIAL_REPO}/contents/{OFFICIAL_SKILLS_PATH}"
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=30)

        if response.status_code != 200:
            raise AppError(AppErrorCode.EXTERNAL_SERVICE_ERROR, f"GitHub API error: {response.status_code}")

        folders = [item for item in response.json() if item["type"] == "dir"]

        for folder in folders:
            skill_name = folder["name"]
            try:
                # 获取 SKILL.md 内容
                content = self._fetch_skill_content(OFFICIAL_REPO, folder["path"])
                if not content:
                    continue

                parsed = self._parse_skill_md(content)
                if not parsed["name"]:
                    parsed["name"] = skill_name

                # 更新或创建
                existing = self.find_by_name(skill_name)
                data = {
                    "description": parsed["description"],
                    "content": parsed["template"],
                    "category": OFFICIAL_CATEGORIES.get(skill_name, "tool"),
                    "source": "official",
                    "repo": OFFICIAL_REPO,
                }

                if existing:
                    self.client.table(self.table).update(data).eq("name", skill_name).execute()
                else:
                    data["name"] = skill_name
                    data["is_active"] = True
                    self.client.table(self.table).insert(data).execute()

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

        # 表格格式
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

        # Frontmatter 格式
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

        # 清理内容
        body = re.sub(r'\|[^\n]+\|(\n\|[^\n]+\|)*', '', content)
        body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', body, flags=re.DOTALL)

        return {"name": name, "description": description, "template": body.strip()}
