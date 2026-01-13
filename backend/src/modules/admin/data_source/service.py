"""Data Source 服务 - 使用 Document Store"""
import re
from datetime import datetime, timezone, timedelta
import requests

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.enum import GITHUB_API, RAW_GITHUB
from src.common.helper import paginate

DOC_TYPE = "admin_data_source"


class DataSourceService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    # ========== 查询 ==========
    def find_all(
        self,
        page: int = 1,
        limit: int = 20,
        type: str | None = None,
        category_id: str | None = None,
        domain_id: str | None = None,
        status: str | None = None,
        language: str | None = None,
        search: str | None = None,
        domain_code: str | None = None,
    ) -> tuple[list[dict], int]:
        docs = self.store.find(DOC_TYPE, status="active", limit=1000)
        
        # 如果提供了 domain_code，先查询对应的 domain_id
        if domain_code and not domain_id:
            from src.modules.admin.domain.service import DomainService
            domain_service = DomainService()
            domain = domain_service.find_by_code(domain_code)
            if domain:
                domain_id = domain["id"]
        
        filtered = []
        for doc in docs:
            data = doc["data"]
            if type and data.get("type") != type:
                continue
            if category_id and data.get("category_id") != category_id:
                continue
            if domain_id and data.get("domain_id") != domain_id:
                continue
            if status and data.get("status") != status:
                continue
            if language and data.get("language") != language:
                continue
            if search:
                search_lower = search.lower()
                name = (data.get("name") or "").lower()
                desc = (data.get("description") or "").lower()
                url = (data.get("url") or "").lower()
                if search_lower not in name and search_lower not in desc and search_lower not in url:
                    continue
            filtered.append(doc)
        
        filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        paged, total = paginate(filtered, page, limit)
        
        return [self._to_response(doc) for doc in paged], total

    def find_by_id(self, id: str) -> dict | None:
        doc = self.store.get(id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def find_by_url(self, url: str) -> dict | None:
        docs = self.store.find(DOC_TYPE, status="active")
        for doc in docs:
            if doc["data"].get("url") == url:
                return self._to_response(doc)
        return None

    def find_by_category(self, category: str) -> list[dict]:
        docs = self.store.find(DOC_TYPE, status="active")
        return [
            self._to_response(doc)
            for doc in docs
            if doc["data"].get("category") == category
        ]

    # ========== 统计 ==========
    def get_stats(self) -> dict:
        docs = self.store.find(DOC_TYPE, status="active")
        total = len(docs)
        by_type: dict[str, int] = {}
        by_status: dict[str, int] = {}
        by_category: dict[str, int] = {}
        
        for doc in docs:
            data = doc["data"]
            t = data.get("type") or "unknown"
            by_type[t] = by_type.get(t, 0) + 1
            
            s = data.get("status", "active")
            by_status[s] = by_status.get(s, 0) + 1
            
            cat = data.get("category") or "uncategorized"
            by_category[cat] = by_category.get(cat, 0) + 1
        
        return {
            "total": total,
            "by_type": by_type,
            "by_status": by_status,
            "by_category": [{"category": k, "count": v} for k, v in sorted(by_category.items(), key=lambda x: -x[1])],
        }

    def get_types(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE, status="active")
        counts: dict[str, int] = {}
        for doc in docs:
            t = doc["data"].get("type") or "unknown"
            counts[t] = counts.get(t, 0) + 1
        return [{"type": t, "count": n} for t, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_statuses(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE, status="active")
        counts: dict[str, int] = {}
        for doc in docs:
            s = doc["data"].get("status") or "active"
            counts[s] = counts.get(s, 0) + 1
        return [{"status": s, "count": n} for s, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_languages(self) -> list[dict]:
        docs = self.store.find(DOC_TYPE, status="active")
        counts: dict[str, int] = {}
        for doc in docs:
            lang = doc["data"].get("language")
            if lang:
                counts[lang] = counts.get(lang, 0) + 1
        return [{"language": l, "count": n} for l, n in sorted(counts.items(), key=lambda x: -x[1])]

    # ========== 创建 ==========
    def create(self, data: dict) -> dict:
        url = data.get("url", "").strip()
        if not url:
            raise AppError(AppErrorCode.VALIDATION_ERROR, "URL is required")
        
        existing = self.find_by_url(url)
        if existing:
            raise AppError(AppErrorCode.DUPLICATE, f"URL already exists: {url}")
        
        source_type = data.get("type", "website")
        
        insert_data = {
            "url": url,
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "type": source_type,
            "category_id": data.get("category_id"),
            "domain_id": data.get("domain_id"),
            "category": data.get("category"),
            "tags": data.get("tags"),
            "status": "active",
            "config": data.get("config", {}),
            "notes": data.get("notes"),
        }
        
        if source_type == "github":
            parsed = self._parse_github_url(url)
            metadata = self._fetch_github_metadata(parsed)
            insert_data.update({
                "owner": parsed.get("owner"),
                "repo": parsed.get("repo"),
                "path": parsed.get("path"),
                "branch": parsed.get("branch", "main"),
                "stars": metadata.get("stars"),
                "forks": metadata.get("forks"),
                "language": metadata.get("language"),
                "topics": metadata.get("topics"),
                "last_updated_at": metadata.get("updated_at"),
            })
            if not insert_data["name"]:
                insert_data["name"] = parsed.get("name") or metadata.get("name", "")
            if not insert_data["description"]:
                insert_data["description"] = metadata.get("description", "")
        
        doc = self.store.create(DOC_TYPE, insert_data)
        return self._to_response(doc)

    def batch_add(self, urls: list[str], source_type: str, category_id: str) -> dict:
        added = 0
        skipped = 0
        errors = []
        
        for url in urls:
            url = url.strip()
            if not url:
                continue
            try:
                existing = self.find_by_url(url)
                if existing:
                    skipped += 1
                    continue
                self.create({"url": url, "type": source_type, "category_id": category_id})
                added += 1
            except Exception as e:
                errors.append({"url": url, "error": str(e)})
        
        return {"added": added, "skipped": skipped, "errors": errors}

    # ========== 更新 ==========
    def update(self, id: str, data: dict) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Data source {id} not found")
        doc = self.store.update(id, data_updates=data)
        return self._to_response(doc)

    def refresh(self, id: str) -> dict:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Data source {id} not found")
        
        if existing.get("type") != "github":
            return existing
        
        parsed = self._parse_github_url(existing["url"])
        
        try:
            metadata = self._fetch_github_metadata(parsed)
            update_data = {
                "stars": metadata.get("stars"),
                "forks": metadata.get("forks"),
                "language": metadata.get("language"),
                "topics": metadata.get("topics"),
                "last_checked_at": datetime.now(timezone.utc).isoformat(),
                "last_updated_at": metadata.get("updated_at"),
                "status": "active",
            }
            if metadata.get("description"):
                update_data["description"] = metadata["description"]
        except Exception as e:
            update_data = {
                "last_checked_at": datetime.now(timezone.utc).isoformat(),
                "status": "invalid" if "404" in str(e) else "active",
            }
        
        doc = self.store.update(id, data_updates=update_data)
        return self._to_response(doc)

    # ========== 删除 ==========
    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Data source {id} not found")
        self.store.delete(id)

    # ========== 私有方法 ==========
    def _parse_github_url(self, url: str) -> dict:
        result = {"owner": None, "repo": None, "path": None, "branch": "main", "name": None}
        match = re.match(r'https?://github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?(?:/(.+))?', url)
        if match:
            result["owner"] = match.group(1)
            result["repo"] = match.group(2).replace(".git", "")
            if match.group(3):
                result["branch"] = match.group(3)
            if match.group(4):
                result["path"] = match.group(4)
                result["name"] = match.group(4).split("/")[-1]
            else:
                result["name"] = result["repo"]
        return result

    def _fetch_github_metadata(self, parsed: dict) -> dict:
        metadata = {}
        if not parsed.get("owner") or not parsed.get("repo"):
            return metadata
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        api_url = f"{GITHUB_API}/repos/{parsed['owner']}/{parsed['repo']}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                metadata["name"] = data.get("name")
                metadata["description"] = data.get("description")
                metadata["stars"] = data.get("stargazers_count")
                metadata["forks"] = data.get("forks_count")
                metadata["language"] = data.get("language")
                metadata["topics"] = data.get("topics", [])
                metadata["updated_at"] = data.get("updated_at")
        except Exception:
            pass
        return metadata


    # ========== GitHub 探索 ==========
    def discover_github(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 30) -> list[dict]:
        """搜索 GitHub 仓库"""
        from src.common.config import get_settings
        settings = get_settings()
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        github_token = getattr(settings, 'github_token', None)
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        params = {"q": query, "sort": sort, "order": order, "per_page": min(per_page, 100)}
        
        try:
            response = requests.get(f"{GITHUB_API}/search/repositories", headers=headers, params=params, timeout=15)
            
            if response.status_code == 403:
                raise AppError(AppErrorCode.INTERNAL_ERROR, "GitHub API rate limit exceeded")
            if response.status_code != 200:
                raise AppError(AppErrorCode.INTERNAL_ERROR, f"GitHub API error: {response.status_code}")
            
            data = response.json()
            results = []
            
            existing_urls = set()
            for item in data.get("items", []):
                url = item.get("html_url")
                if url:
                    existing = self.find_by_url(url)
                    if existing:
                        existing_urls.add(url)
            
            for item in data.get("items", []):
                url = item.get("html_url", "")
                results.append({
                    "url": url,
                    "name": item.get("name", ""),
                    "full_name": item.get("full_name", ""),
                    "description": item.get("description") or "",
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "language": item.get("language") or "",
                    "topics": item.get("topics", []),
                    "updated_at": item.get("updated_at", ""),
                    "owner": item.get("owner", {}).get("login", ""),
                    "repo": item.get("name", ""),
                    "already_exists": url in existing_urls,
                })
            return results
        except requests.RequestException as e:
            raise AppError(AppErrorCode.INTERNAL_ERROR, f"GitHub API request failed: {str(e)}")

    def batch_import(self, items: list[dict], category_id: str, domain_id: str | None) -> dict:
        """批量导入探索结果"""
        added = 0
        skipped = 0
        errors = []
        
        for item in items:
            url = item.get("url", "").strip()
            if not url:
                continue
            try:
                existing = self.find_by_url(url)
                if existing:
                    skipped += 1
                    continue
                self.create({
                    "url": url,
                    "name": item.get("name", ""),
                    "description": item.get("description", ""),
                    "type": "github",
                    "category_id": category_id,
                    "domain_id": domain_id,
                    "tags": item.get("topics", []),
                })
                added += 1
            except Exception as e:
                errors.append({"url": url, "error": str(e)})
        
        return {"added": added, "skipped": skipped, "errors": errors}

    def _to_response(self, doc: dict) -> dict:
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "url": data.get("url"),
            "name": data.get("name"),
            "description": data.get("description"),
            "type": data.get("type"),
            "category_id": data.get("category_id"),
            "domain_id": data.get("domain_id"),
            "category": data.get("category"),
            "tags": data.get("tags"),
            "status": data.get("status", "active"),
            "config": data.get("config", {}),
            "notes": data.get("notes"),
            "owner": data.get("owner"),
            "repo": data.get("repo"),
            "path": data.get("path"),
            "branch": data.get("branch"),
            "stars": data.get("stars"),
            "forks": data.get("forks"),
            "language": data.get("language"),
            "topics": data.get("topics"),
            "last_updated_at": data.get("last_updated_at"),
            "last_checked_at": data.get("last_checked_at"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
