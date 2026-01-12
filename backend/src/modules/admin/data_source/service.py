"""Data Source 服务 - 使用 Supabase API"""
import re
from datetime import datetime, timezone
import requests

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin

GITHUB_API = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com"


class DataSourceService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "data_sources"

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
        # 如果提供了 domain_code，先查询对应的 domain_id
        if domain_code and not domain_id:
            domain_response = (
                self.client.table("domains")
                .select("id")
                .eq("code", domain_code)
                .execute()
            )
            if domain_response.data and len(domain_response.data) > 0:
                domain_id = domain_response.data[0]["id"]
        
        # 使用 join 查询关联的分类和领域信息
        query = self.client.table(self.table).select(
            "*, domain_categories(id, code, name), domains(id, code, name)",
            count="exact"
        )
        
        if type:
            query = query.eq("type", type)
        if category_id:
            query = query.eq("category_id", category_id)
        if domain_id:
            query = query.eq("domain_id", domain_id)
        if status:
            query = query.eq("status", status)
        if language:
            query = query.eq("language", language)
        if search:
            query = query.or_(f"name.ilike.%{search}%,description.ilike.%{search}%,url.ilike.%{search}%")
        
        query = query.order("created_at", desc=True)
        query = query.range((page - 1) * limit, page * limit - 1)
        
        response = query.execute()
        return response.data, response.count or 0

    def find_by_id(self, id: str) -> dict | None:
        response = (
            self.client.table(self.table)
            .select("*, domain_categories(id, code, name), domains(id, code, name)")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        return response.data

    def find_by_url(self, url: str) -> dict | None:
        try:
            response = self.client.table(self.table).select("*").eq("url", url).maybe_single().execute()
            return response.data
        except Exception:
            return None

    def find_by_category(self, category: str) -> list[dict]:
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("category", category)
            .eq("status", "active")
            .execute()
        )
        return response.data

    # ========== 统计 ==========
    def get_stats(self) -> dict:
        response = self.client.table(self.table).select(
            "type, category_id, status, domain_categories(code, name)"
        ).execute()
        
        total = len(response.data)
        by_type: dict[str, int] = {}
        by_status: dict[str, int] = {}
        by_category: dict[str, int] = {}
        
        for item in response.data:
            t = item.get("type") or "unknown"
            by_type[t] = by_type.get(t, 0) + 1
            
            status = item.get("status", "active")
            by_status[status] = by_status.get(status, 0) + 1
            
            # 使用关联的分类
            cat_info = item.get("domain_categories")
            if cat_info:
                cat = cat_info.get("code") or "uncategorized"
            else:
                cat = "uncategorized"
            by_category[cat] = by_category.get(cat, 0) + 1
        
        return {
            "total": total,
            "by_type": by_type,
            "by_status": by_status,
            "by_category": [{"category": k, "count": v} for k, v in sorted(by_category.items(), key=lambda x: -x[1])],
        }

    def get_categories(self) -> list[dict]:
        """获取所有可用的分类（从 domain_categories 表）"""
        # 获取所有领域分类
        categories_response = (
            self.client.table("domain_categories")
            .select("id, code, name, name_en, sort_order")
            .order("sort_order")
            .execute()
        )
        
        # 获取每个分类的数据源数量
        data_sources_response = self.client.table(self.table).select("category_id").execute()
        
        # 统计数量
        counts_by_id: dict[str, int] = {}
        for item in data_sources_response.data:
            cat_id = item.get("category_id")
            if cat_id:
                counts_by_id[cat_id] = counts_by_id.get(cat_id, 0) + 1
        
        result = []
        for cat in categories_response.data:
            count = counts_by_id.get(cat["id"], 0)
            result.append({
                "id": cat["id"],
                "code": cat["code"],
                "name": cat["name"],
                "nameEn": cat.get("name_en"),
                "count": count,
            })
        
        return result

    def get_domains_by_category(self, category_id: str | None = None) -> list[dict]:
        """获取领域列表，可选按分类筛选"""
        query = (
            self.client.table("domains")
            .select("id, code, name, name_en, category_id")
            .eq("is_active", True)
            .order("sort_order")
        )
        
        if category_id:
            query = query.eq("category_id", category_id)
        
        response = query.execute()
        
        # 获取每个领域的数据源数量
        ds_query = self.client.table(self.table).select("domain_id")
        if category_id:
            ds_query = ds_query.eq("category_id", category_id)
        data_sources_response = ds_query.execute()
        
        counts: dict[str, int] = {}
        for item in data_sources_response.data:
            domain_id = item.get("domain_id")
            if domain_id:
                counts[domain_id] = counts.get(domain_id, 0) + 1
        
        result = []
        for domain in response.data:
            result.append({
                "id": domain["id"],
                "code": domain["code"],
                "name": domain["name"],
                "nameEn": domain.get("name_en"),
                "count": counts.get(domain["id"], 0),
            })
        
        return result

    def get_types(self) -> list[dict]:
        response = self.client.table(self.table).select("type").execute()
        counts: dict[str, int] = {}
        for item in response.data:
            t = item.get("type") or "unknown"
            counts[t] = counts.get(t, 0) + 1
        return [{"type": t, "count": n} for t, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_statuses(self) -> list[dict]:
        response = self.client.table(self.table).select("status").execute()
        counts: dict[str, int] = {}
        for item in response.data:
            s = item.get("status") or "active"
            counts[s] = counts.get(s, 0) + 1
        return [{"status": s, "count": n} for s, n in sorted(counts.items(), key=lambda x: -x[1])]

    def get_languages(self) -> list[dict]:
        response = self.client.table(self.table).select("language").execute()
        counts: dict[str, int] = {}
        for item in response.data:
            lang = item.get("language")
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
            "tags": data.get("tags"),
            "status": "active",
            "config": data.get("config", {}),
            "notes": data.get("notes"),
        }
        
        # GitHub 类型额外处理
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
        
        response = self.client.table(self.table).insert(insert_data).execute()
        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create")
        return response.data[0]

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
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        return response.data[0]

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
        
        response = self.client.table(self.table).update(update_data).eq("id", id).execute()
        return response.data[0]

    def refresh_all(self, category: str | None = None) -> dict:
        query = self.client.table(self.table).select("id, url, type, category, stars, forks, language").eq("type", "github")
        if category:
            query = query.eq("category", category)
        
        response = query.execute()
        
        total = len(response.data)
        updated = 0
        unchanged = 0
        errors = []
        by_category: dict[str, dict] = {}
        changes: list[dict] = []
        
        for item in response.data:
            item_category = item.get("category") or "uncategorized"
            old_stars = item.get("stars") or 0
            old_forks = item.get("forks") or 0
            
            # 初始化分类统计
            if item_category not in by_category:
                by_category[item_category] = {"total": 0, "updated": 0, "unchanged": 0, "errors": 0}
            by_category[item_category]["total"] += 1
            
            try:
                refreshed_item = self.refresh(item["id"])
                new_stars = refreshed_item.get("stars") or 0
                new_forks = refreshed_item.get("forks") or 0
                
                # 检查是否有变化
                has_changes = (new_stars != old_stars) or (new_forks != old_forks)
                
                if has_changes:
                    updated += 1
                    by_category[item_category]["updated"] += 1
                    
                    # 记录变化详情（只记录前20个）
                    if len(changes) < 20:
                        change_info = {
                            "url": item["url"],
                            "name": refreshed_item.get("name") or item["url"].split("/")[-1],
                        }
                        if new_stars != old_stars:
                            change_info["stars"] = {"old": old_stars, "new": new_stars, "diff": new_stars - old_stars}
                        if new_forks != old_forks:
                            change_info["forks"] = {"old": old_forks, "new": new_forks, "diff": new_forks - old_forks}
                        changes.append(change_info)
                else:
                    unchanged += 1
                    by_category[item_category]["unchanged"] += 1
                    
            except Exception as e:
                errors.append({"id": item["id"], "url": item["url"], "error": str(e)})
                by_category[item_category]["errors"] += 1
        
        # 转换 by_category 为列表格式
        category_stats = [
            {"category": cat, **stats}
            for cat, stats in sorted(by_category.items(), key=lambda x: -x[1]["total"])
        ]
        
        return {
            "total": total,
            "updated": updated,
            "unchanged": unchanged,
            "errors": errors,
            "by_category": category_stats,
            "changes": changes,
        }

    # ========== 删除 ==========
    def delete(self, id: str) -> None:
        existing = self.find_by_id(id)
        if not existing:
            raise AppError(AppErrorCode.NOT_FOUND, f"Data source {id} not found")
        self.client.table(self.table).delete().eq("id", id).execute()

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
    def discover_github(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 30,
    ) -> list[dict]:
        """搜索 GitHub 仓库"""
        from src.common.logger import log_with_extra
        from src.common.config import get_settings
        
        settings = get_settings()
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        # 如果配置了 GitHub Token，使用它来提高 API 限制
        github_token = getattr(settings, 'github_token', None)
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": min(per_page, 100),
        }
        
        log_with_extra("debug", f"[DataSource] GitHub API request: query={query}",
                      query=query, sort=sort, per_page=per_page)
        
        try:
            response = requests.get(
                f"{GITHUB_API}/search/repositories",
                headers=headers,
                params=params,
                timeout=15,
            )
            
            log_with_extra("debug", f"[DataSource] GitHub API response: status={response.status_code}",
                          status_code=response.status_code, query=query)
            
            if response.status_code == 403:
                # Rate limit exceeded
                rate_limit = response.headers.get('X-RateLimit-Remaining', 'unknown')
                reset_time = response.headers.get('X-RateLimit-Reset', 'unknown')
                log_with_extra("error", f"[DataSource] GitHub API rate limit exceeded. Remaining: {rate_limit}, Reset: {reset_time}",
                              rate_limit=rate_limit, reset_time=reset_time)
                raise AppError(
                    AppErrorCode.INTERNAL_ERROR,
                    f"GitHub API rate limit exceeded. Please configure GITHUB_TOKEN or wait.",
                )
            
            if response.status_code != 200:
                error_body = response.text[:500]
                log_with_extra("error", f"[DataSource] GitHub API error: {response.status_code} - {error_body}",
                              status_code=response.status_code, error=error_body)
                raise AppError(
                    AppErrorCode.INTERNAL_ERROR,
                    f"GitHub API error: {response.status_code}",
                )
            
            data = response.json()
            results = []
            
            # 获取已存在的 URL 列表
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

    def get_domain_keywords(self) -> list[dict]:
        """从 domains 表获取领域关键词配置"""
        response = (
            self.client.table("domains")
            .select("code, name, name_en, discovery_keywords")
            .eq("is_active", True)
            .execute()
        )
        
        result = []
        for d in response.data:
            keywords = d.get("discovery_keywords") or []
            if keywords:
                result.append({
                    "domain": d["code"],
                    "name_zh": d.get("name") or d["code"],
                    "name_en": d.get("name_en") or d["code"],
                    "keywords": keywords,
                })
        
        # 如果数据库没有配置，使用默认关键词
        if not result:
            result = self._get_default_domain_keywords()
        
        return result

    def _get_default_domain_keywords(self) -> list[dict]:
        """默认领域关键词（数据库未配置时使用）"""
        return [
            {
                "domain": "flight",
                "name_zh": "机票预订",
                "name_en": "Flight Booking",
                "keywords": [
                    "awesome-flights",
                    "awesome-aviation",
                    "flight-api stars:>50",
                    "flight-tracker stars:>50",
                    "topic:flight",
                    "topic:aviation",
                    "topic:airline",
                ],
            },
            {
                "domain": "hotel",
                "name_zh": "酒店预订",
                "name_en": "Hotel Booking",
                "keywords": [
                    "awesome-travel",
                    "hotel-api stars:>30",
                    "hotel-booking stars:>50",
                    "topic:hotel",
                    "topic:travel",
                    "topic:booking",
                ],
            },
            {
                "domain": "car_rental",
                "name_zh": "租车服务",
                "name_en": "Car Rental",
                "keywords": [
                    "car-rental-api stars:>20",
                    "vehicle-rental stars:>20",
                    "topic:car-rental",
                    "topic:vehicle",
                ],
            },
            {
                "domain": "housing",
                "name_zh": "租房买房",
                "name_en": "Housing",
                "keywords": [
                    "awesome-real-estate",
                    "real-estate-api stars:>50",
                    "rental-platform stars:>30",
                    "topic:real-estate",
                    "topic:housing",
                    "topic:rental",
                ],
            },
            {
                "domain": "moving",
                "name_zh": "搬家服务",
                "name_en": "Moving Service",
                "keywords": [
                    "moving-service stars:>10",
                    "relocation stars:>20",
                    "topic:moving",
                ],
            },
            {
                "domain": "job",
                "name_zh": "求职就业",
                "name_en": "Job Search",
                "keywords": [
                    "awesome-interview",
                    "awesome-job",
                    "job-board stars:>50",
                    "topic:job-search",
                    "topic:career",
                ],
            },
            {
                "domain": "resume",
                "name_zh": "简历优化",
                "name_en": "Resume",
                "keywords": [
                    "awesome-resume",
                    "resume-builder stars:>100",
                    "cv-builder stars:>50",
                    "topic:resume",
                    "topic:cv",
                ],
            },
            {
                "domain": "investment",
                "name_zh": "投资理财",
                "name_en": "Investment",
                "keywords": [
                    "awesome-quant",
                    "awesome-trading",
                    "stock-trading stars:>100",
                    "topic:trading",
                    "topic:investment",
                    "topic:fintech",
                ],
            },
            {
                "domain": "insurance",
                "name_zh": "保险规划",
                "name_en": "Insurance",
                "keywords": [
                    "awesome-insurance",
                    "insurance-api stars:>20",
                    "topic:insurance",
                    "topic:insurtech",
                ],
            },
            {
                "domain": "tax",
                "name_zh": "税务规划",
                "name_en": "Tax Planning",
                "keywords": [
                    "tax-calculator stars:>30",
                    "tax-software stars:>20",
                    "topic:tax",
                    "topic:accounting",
                ],
            },
            {
                "domain": "school",
                "name_zh": "学校选择",
                "name_en": "School Selection",
                "keywords": [
                    "awesome-education",
                    "school-ranking stars:>20",
                    "university-api stars:>20",
                    "topic:education",
                    "topic:university",
                ],
            },
            {
                "domain": "language",
                "name_zh": "语言学习",
                "name_en": "Language Learning",
                "keywords": [
                    "awesome-language-learning",
                    "language-learning stars:>100",
                    "flashcard stars:>50",
                    "topic:language-learning",
                    "topic:spaced-repetition",
                ],
            },
            {
                "domain": "visa",
                "name_zh": "签证移民",
                "name_en": "Visa & Immigration",
                "keywords": [
                    "immigration-api stars:>10",
                    "visa-tracker stars:>10",
                    "h1b stars:>50",
                    "green-card stars:>20",
                    "topic:immigration",
                    "topic:visa",
                ],
            },
            {
                "domain": "healthcare",
                "name_zh": "医疗健康",
                "name_en": "Healthcare",
                "keywords": [
                    "awesome-healthcare",
                    "awesome-health",
                    "healthcare-api stars:>50",
                    "medical-api stars:>30",
                    "topic:healthcare",
                    "topic:health",
                    "topic:medical",
                ],
            },
            {
                "domain": "banking",
                "name_zh": "银行金融",
                "name_en": "Banking & Finance",
                "keywords": [
                    "awesome-fintech",
                    "banking-api stars:>50",
                    "credit-card stars:>30",
                    "plaid stars:>50",
                    "topic:banking",
                    "topic:fintech",
                    "topic:credit",
                ],
            },
            {
                "domain": "legal",
                "name_zh": "法律服务",
                "name_en": "Legal Services",
                "keywords": [
                    "awesome-legal",
                    "legal-api stars:>20",
                    "contract-analysis stars:>20",
                    "topic:legal",
                    "topic:law",
                    "topic:legaltech",
                ],
            },
            {
                "domain": "childcare",
                "name_zh": "育儿托管",
                "name_en": "Childcare",
                "keywords": [
                    "awesome-parenting",
                    "daycare stars:>10",
                    "childcare stars:>20",
                    "school-district stars:>10",
                    "topic:parenting",
                    "topic:childcare",
                    "topic:education",
                ],
            },
            {
                "domain": "phone",
                "name_zh": "手机套餐",
                "name_en": "Phone Plans",
                "keywords": [
                    "phone-plan stars:>10",
                    "carrier-comparison stars:>10",
                    "mobile-plan stars:>20",
                    "topic:telecom",
                    "topic:mobile",
                ],
            },
            {
                "domain": "internet",
                "name_zh": "网络宽带",
                "name_en": "Internet Service",
                "keywords": [
                    "isp-comparison stars:>10",
                    "internet-speed stars:>20",
                    "broadband stars:>20",
                    "topic:internet",
                    "topic:isp",
                ],
            },
            {
                "domain": "utilities",
                "name_zh": "水电煤气",
                "name_en": "Utilities",
                "keywords": [
                    "utility-api stars:>10",
                    "energy-comparison stars:>10",
                    "topic:utilities",
                    "topic:energy",
                ],
            },
            {
                "domain": "shopping",
                "name_zh": "购物比价",
                "name_en": "Shopping",
                "keywords": [
                    "awesome-deals",
                    "price-comparison stars:>50",
                    "cashback stars:>30",
                    "coupon stars:>50",
                    "topic:shopping",
                    "topic:deals",
                    "topic:ecommerce",
                ],
            },
            {
                "domain": "dining",
                "name_zh": "餐饮美食",
                "name_en": "Dining",
                "keywords": [
                    "awesome-food",
                    "restaurant-api stars:>30",
                    "yelp-api stars:>20",
                    "food-delivery stars:>30",
                    "topic:food",
                    "topic:restaurant",
                ],
            },
            {
                "domain": "social",
                "name_zh": "社交融入",
                "name_en": "Social Integration",
                "keywords": [
                    "community-platform stars:>30",
                    "event-platform stars:>30",
                    "meetup stars:>20",
                    "topic:community",
                    "topic:social",
                ],
            },
            {
                "domain": "pet",
                "name_zh": "宠物服务",
                "name_en": "Pet Services",
                "keywords": [
                    "awesome-pets",
                    "pet-api stars:>10",
                    "vet-finder stars:>10",
                    "topic:pets",
                    "topic:veterinary",
                ],
            },
            {
                "domain": "driving",
                "name_zh": "驾照考试",
                "name_en": "Driver License",
                "keywords": [
                    "dmv stars:>20",
                    "driving-test stars:>30",
                    "driver-license stars:>20",
                    "topic:driving",
                    "topic:dmv",
                ],
            },
            {
                "domain": "ssn",
                "name_zh": "SSN/ITIN",
                "name_en": "SSN/ITIN",
                "keywords": [
                    "ssn stars:>10",
                    "itin stars:>10",
                    "social-security stars:>20",
                    "topic:ssn",
                    "topic:tax-id",
                ],
            },
            {
                "domain": "credit",
                "name_zh": "信用建立",
                "name_en": "Credit Building",
                "keywords": [
                    "awesome-credit",
                    "credit-score stars:>50",
                    "credit-builder stars:>30",
                    "fico stars:>20",
                    "topic:credit",
                    "topic:credit-score",
                    "topic:personal-finance",
                ],
            },
            {
                "domain": "travel",
                "name_zh": "旅游攻略",
                "name_en": "Travel",
                "keywords": [
                    "awesome-travel",
                    "travel-api stars:>50",
                    "trip-planner stars:>30",
                    "topic:travel",
                    "topic:tourism",
                ],
            },
            {
                "domain": "shipping",
                "name_zh": "国际快递",
                "name_en": "International Shipping",
                "keywords": [
                    "shipping-api stars:>30",
                    "package-tracking stars:>20",
                    "topic:shipping",
                    "topic:logistics",
                ],
            },
            {
                "domain": "remittance",
                "name_zh": "跨境汇款",
                "name_en": "Remittance",
                "keywords": [
                    "remittance stars:>20",
                    "money-transfer stars:>30",
                    "currency-exchange stars:>20",
                    "topic:remittance",
                    "topic:fintech",
                ],
            },
            {
                "domain": "secondhand",
                "name_zh": "二手交易",
                "name_en": "Secondhand",
                "keywords": [
                    "marketplace stars:>50",
                    "classifieds stars:>20",
                    "topic:marketplace",
                    "topic:secondhand",
                ],
            },
            {
                "domain": "fitness",
                "name_zh": "健身运动",
                "name_en": "Fitness",
                "keywords": [
                    "awesome-fitness",
                    "fitness-api stars:>30",
                    "workout stars:>50",
                    "topic:fitness",
                    "topic:health",
                ],
            },
            {
                "domain": "entertainment",
                "name_zh": "娱乐休闲",
                "name_en": "Entertainment",
                "keywords": [
                    "awesome-entertainment",
                    "movie-api stars:>50",
                    "event-api stars:>30",
                    "topic:entertainment",
                    "topic:movies",
                ],
            },
            {
                "domain": "wedding",
                "name_zh": "婚礼服务",
                "name_en": "Wedding",
                "keywords": [
                    "wedding-planner stars:>20",
                    "wedding stars:>30",
                    "topic:wedding",
                ],
            },
            {
                "domain": "funeral",
                "name_zh": "殡葬服务",
                "name_en": "Funeral Services",
                "keywords": [
                    "funeral stars:>10",
                    "memorial stars:>10",
                    "topic:funeral",
                ],
            },
            {
                "domain": "storage",
                "name_zh": "仓储服务",
                "name_en": "Storage",
                "keywords": [
                    "storage-api stars:>20",
                    "self-storage stars:>10",
                    "topic:storage",
                ],
            },
            {
                "domain": "cleaning",
                "name_zh": "清洁服务",
                "name_en": "Cleaning",
                "keywords": [
                    "cleaning-service stars:>20",
                    "home-service stars:>30",
                    "topic:cleaning",
                    "topic:home-services",
                ],
            },
            {
                "domain": "repair",
                "name_zh": "维修服务",
                "name_en": "Repair Services",
                "keywords": [
                    "repair-service stars:>20",
                    "home-repair stars:>20",
                    "topic:repair",
                    "topic:maintenance",
                ],
            },
            {
                "domain": "tutoring",
                "name_zh": "家教补习",
                "name_en": "Tutoring",
                "keywords": [
                    "awesome-tutoring",
                    "tutoring-platform stars:>30",
                    "online-tutoring stars:>30",
                    "topic:tutoring",
                    "topic:education",
                ],
            },
        ]

    def auto_discover(self, domain: str, limit_per_keyword: int = 10) -> dict:
        """自动探索某个领域的资源 - 多策略探索"""
        from src.common.logger import log_with_extra
        
        domain_keywords = self.get_domain_keywords()
        domain_config = next((d for d in domain_keywords if d["domain"] == domain), None)
        
        if not domain_config:
            raise AppError(AppErrorCode.NOT_FOUND, f"Domain {domain} not found")
        
        all_results = []
        seen_urls = set()
        strategies_used = []
        
        # 策略1: 基于预设关键词搜索
        keyword_results = self._discover_by_keywords(
            domain_config["keywords"], 
            limit_per_keyword, 
            seen_urls
        )
        all_results.extend(keyword_results)
        strategies_used.append({"strategy": "keywords", "count": len(keyword_results)})
        
        # 策略2: 基于已有数据源的 topics 扩展搜索
        topic_results = self._discover_by_existing_topics(domain, limit_per_keyword, seen_urls)
        all_results.extend(topic_results)
        strategies_used.append({"strategy": "topics_expansion", "count": len(topic_results)})
        
        # 策略3: 探索优质仓库作者的其他项目
        author_results = self._discover_by_authors(domain, limit_per_keyword // 2, seen_urls)
        all_results.extend(author_results)
        strategies_used.append({"strategy": "author_exploration", "count": len(author_results)})
        
        # 策略4: GitHub Trending (如果可用)
        trending_results = self._discover_trending(domain_config.get("trending_topics", []), seen_urls)
        all_results.extend(trending_results)
        strategies_used.append({"strategy": "trending", "count": len(trending_results)})
        
        # 按 stars 排序并去重
        all_results.sort(key=lambda x: x["stars"], reverse=True)
        
        log_with_extra("info", f"[DataSource] Auto discover completed for {domain}",
                      domain=domain, total=len(all_results), strategies=strategies_used)
        
        return {
            "domain": domain,
            "name_zh": domain_config["name_zh"],
            "name_en": domain_config["name_en"],
            "keywords_used": domain_config["keywords"],
            "strategies_used": strategies_used,
            "results": all_results,
            "total": len(all_results),
        }

    def _discover_by_keywords(self, keywords: list[str], limit: int, seen_urls: set) -> list[dict]:
        """策略1: 基于关键词搜索"""
        from src.common.logger import log_with_extra
        
        results = []
        for keyword in keywords:
            try:
                items = self.discover_github(
                    query=keyword,
                    sort="stars",
                    order="desc",
                    per_page=limit,
                )
                for r in items:
                    if r["url"] not in seen_urls:
                        seen_urls.add(r["url"])
                        r["discovery_source"] = f"keyword:{keyword}"
                        results.append(r)
                log_with_extra("debug", f"[DataSource] Keyword '{keyword}' found {len(items)} items",
                              keyword=keyword, found=len(items))
            except Exception as e:
                log_with_extra("warn", f"[DataSource] Keyword search failed: {keyword} - {str(e)}",
                              keyword=keyword, error=str(e))
                continue
        return results

    def _discover_by_existing_topics(self, category: str, limit: int, seen_urls: set) -> list[dict]:
        """策略2: 基于已有数据源的 topics 扩展搜索"""
        from src.common.logger import log_with_extra
        
        results = []
        
        # 获取该分类下已有数据源的 topics
        try:
            response = (
                self.client.table(self.table)
                .select("topics")
                .eq("category", category)
                .eq("type", "github")
                .not_.is_("topics", "null")
                .limit(50)
                .execute()
            )
        except Exception as e:
            log_with_extra("warn", f"[DataSource] Failed to fetch existing topics: {str(e)}",
                          category=category, error=str(e))
            return results
        
        # 统计 topic 出现频率
        topic_counts: dict[str, int] = {}
        for item in response.data:
            topics = item.get("topics") or []
            for topic in topics:
                if topic and len(topic) > 2:  # 过滤太短的 topic
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        if not topic_counts:
            log_with_extra("info", f"[DataSource] No existing topics found for category: {category}",
                          category=category)
            return results
        
        # 取出现频率最高的 topics 进行搜索
        top_topics = sorted(topic_counts.items(), key=lambda x: -x[1])[:10]
        log_with_extra("info", f"[DataSource] Found {len(top_topics)} top topics for expansion",
                      category=category, topics=[t[0] for t in top_topics])
        
        for topic, count in top_topics:
            try:
                items = self.discover_github(
                    query=f"topic:{topic}",
                    sort="stars",
                    order="desc",
                    per_page=limit // 2,
                )
                added = 0
                for r in items:
                    if r["url"] not in seen_urls:
                        seen_urls.add(r["url"])
                        r["discovery_source"] = f"topic:{topic}"
                        results.append(r)
                        added += 1
                log_with_extra("debug", f"[DataSource] Topic '{topic}' found {len(items)} items, added {added} new",
                              topic=topic, found=len(items), added=added)
            except Exception as e:
                log_with_extra("warn", f"[DataSource] Topic search failed: {topic} - {str(e)}",
                              topic=topic, error=str(e))
                continue
        
        return results

    def _discover_by_authors(self, category: str, limit: int, seen_urls: set) -> list[dict]:
        """策略3: 探索优质仓库作者的其他项目"""
        from src.common.logger import log_with_extra
        
        results = []
        
        # 获取该分类下 stars 最高的仓库的作者
        try:
            response = (
                self.client.table(self.table)
                .select("owner, stars")
                .eq("category", category)
                .eq("type", "github")
                .not_.is_("owner", "null")
                .order("stars", desc=True)
                .limit(10)
                .execute()
            )
        except Exception as e:
            log_with_extra("warn", f"[DataSource] Failed to fetch top authors: {str(e)}",
                          category=category, error=str(e))
            return results
        
        if not response.data:
            log_with_extra("info", f"[DataSource] No existing authors found for category: {category}",
                          category=category)
            return results
        
        # 获取这些作者的其他仓库
        seen_owners = set()
        for item in response.data:
            owner = item.get("owner")
            if not owner or owner in seen_owners:
                continue
            seen_owners.add(owner)
            
            try:
                items = self.discover_github(
                    query=f"user:{owner}",
                    sort="stars",
                    order="desc",
                    per_page=limit,
                )
                added = 0
                for r in items:
                    if r["url"] not in seen_urls:
                        seen_urls.add(r["url"])
                        r["discovery_source"] = f"author:{owner}"
                        results.append(r)
                        added += 1
                log_with_extra("debug", f"[DataSource] Author '{owner}' found {len(items)} repos, added {added} new",
                              owner=owner, found=len(items), added=added)
            except Exception as e:
                log_with_extra("warn", f"[DataSource] Author search failed: {owner} - {str(e)}",
                              owner=owner, error=str(e))
                continue
        
        return results

    def _discover_trending(self, topics: list[str], seen_urls: set) -> list[dict]:
        """策略4: 获取 GitHub Trending (通过搜索近期高星项目模拟)"""
        from src.common.logger import log_with_extra
        
        results = []
        
        # 搜索最近创建且星标增长快的项目
        try:
            # 搜索最近30天创建的高星项目
            from datetime import timedelta
            thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
            
            items = self.discover_github(
                query=f"created:>{thirty_days_ago} stars:>100",
                sort="stars",
                order="desc",
                per_page=20,
            )
            for r in items:
                if r["url"] not in seen_urls:
                    seen_urls.add(r["url"])
                    r["discovery_source"] = "trending:recent"
                    results.append(r)
            log_with_extra("info", f"[DataSource] Trending search found {len(items)} items, added {len(results)} new",
                          found=len(items), added=len(results))
        except Exception as e:
            log_with_extra("warn", f"[DataSource] Trending search failed: {str(e)}",
                          error=str(e))
        
        return results

    def get_discovery_stats(self, category: str | None = None) -> dict:
        """获取探索统计信息，用于优化探索策略"""
        query = self.client.table(self.table).select("topics, language, owner, stars")
        if category:
            query = query.eq("category", category)
        
        response = query.execute()
        
        # 统计 topics
        topic_counts: dict[str, int] = {}
        language_counts: dict[str, int] = {}
        owner_counts: dict[str, int] = {}
        
        for item in response.data:
            # Topics
            for topic in (item.get("topics") or []):
                if topic:
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            # Languages
            lang = item.get("language")
            if lang:
                language_counts[lang] = language_counts.get(lang, 0) + 1
            
            # Owners
            owner = item.get("owner")
            if owner:
                owner_counts[owner] = owner_counts.get(owner, 0) + 1
        
        return {
            "total_sources": len(response.data),
            "top_topics": sorted(topic_counts.items(), key=lambda x: -x[1])[:20],
            "top_languages": sorted(language_counts.items(), key=lambda x: -x[1])[:10],
            "top_owners": sorted(owner_counts.items(), key=lambda x: -x[1])[:10],
        }

    def batch_import(self, items: list[dict], category_id: str, domain_id: str | None) -> dict:
        """批量导入探索结果到数据源"""
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
                    "notes": "",
                    "config": {},
                })
                added += 1
            except Exception as e:
                errors.append({"url": url, "error": str(e)})
        
        return {"added": added, "skipped": skipped, "errors": errors}
