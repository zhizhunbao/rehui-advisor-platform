# 发现脚本基类 - 数据源抽象 + domain 发现器
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from scripts.base import ScriptBase, ScriptResult


@dataclass
class DiscoveredItem:
    """发现的资源项"""
    url: str
    title: str
    description: str
    source_type: str
    domain_code: str
    tags: list[str]
    metadata: dict[str, Any]

    def to_standard_format(self, category: str = "other") -> dict[str, Any]:
        """转换为标准格式"""
        repo_info = self._extract_repo_info()
        return {
            "url": self.url,
            "name": self.title,
            "description": self.description,
            "category": category,
            "source": self.source_type,
            "repo": repo_info["repo"],
            "platform": repo_info["platform"],
            "tags": self.tags,
            "metadata": self.metadata,
            "is_active": True,
        }

    def _extract_repo_info(self) -> dict[str, str]:
        """从 URL 提取仓库信息"""
        if "github.com" in self.url:
            parts = self.url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                return {"repo": f"{parts[0]}/{parts[1]}", "platform": "github"}
        return {"repo": "", "platform": "web"}


@dataclass
class QualityScore:
    """质量评分结果"""
    total: float
    source_score: float
    relevance_score: float
    freshness_score: float
    activity_score: float
    details: dict[str, Any]


class QualityEvaluator:
    """URL 质量评估器"""

    TRUSTED_DOMAINS = {
        "github.com": 1.0,
        "anthropic.com": 1.0,
        "openai.com": 1.0,
        "docs.anthropic.com": 1.0,
        "simonwillison.net": 0.9,
        "medium.com": 0.7,
    }

    MIN_SCORE = 0.0
    MAX_SCORE = 100.0
    DEFAULT_SCORE = 50.0
    
    WEIGHT_SOURCE = 0.3
    WEIGHT_RELEVANCE = 0.3
    WEIGHT_FRESHNESS = 0.2
    WEIGHT_ACTIVITY = 0.2

    def __init__(self, keywords: list[str]) -> None:
        self.keywords = [k.lower() for k in keywords]

    def evaluate(self, url: str, title: str, description: str, source_type: str, metadata: dict[str, Any]) -> QualityScore:
        """综合评估 URL 质量"""
        source_score = self._evaluate_source(url, source_type, metadata)
        relevance_score = self._evaluate_relevance(url, title, description)
        freshness_score = self._evaluate_freshness(metadata)
        activity_score = self._evaluate_activity(source_type, metadata)

        total = (
            source_score * self.WEIGHT_SOURCE
            + relevance_score * self.WEIGHT_RELEVANCE
            + freshness_score * self.WEIGHT_FRESHNESS
            + activity_score * self.WEIGHT_ACTIVITY
        )

        return QualityScore(
            total=round(total, 2),
            source_score=round(source_score, 2),
            relevance_score=round(relevance_score, 2),
            freshness_score=round(freshness_score, 2),
            activity_score=round(activity_score, 2),
            details={"url": url, "source_type": source_type, "metadata": metadata},
        )

    def _evaluate_source(self, url: str, source_type: str, metadata: dict[str, Any]) -> float:
        """评估来源可信度 (0-100)"""
        score = self.DEFAULT_SCORE
        domain = urlparse(url).netloc.lower()
        
        for trusted_domain, trust_score in self.TRUSTED_DOMAINS.items():
            if trusted_domain in domain:
                score = 60 + (trust_score * 40)
                break

        return self._adjust_score_by_source_type(score, source_type, metadata)

    def _adjust_score_by_source_type(self, score: float, source_type: str, metadata: dict[str, Any]) -> float:
        """根据来源类型调整分数"""
        if source_type == "github":
            return self._adjust_github_score(score, metadata)
        if source_type == "hackernews":
            return self._adjust_hackernews_score(score, metadata)
        return score

    def _adjust_github_score(self, score: float, metadata: dict[str, Any]) -> float:
        """根据 GitHub stars 调整分数"""
        stars = metadata.get("stars", 0)
        if stars >= 1000:
            return min(self.MAX_SCORE, score + 20)
        if stars >= 500:
            return min(self.MAX_SCORE, score + 15)
        if stars >= 100:
            return min(self.MAX_SCORE, score + 10)
        return score

    def _adjust_hackernews_score(self, score: float, metadata: dict[str, Any]) -> float:
        """根据 HackerNews points 调整分数"""
        points = metadata.get("points", 0)
        if points >= 200:
            return min(self.MAX_SCORE, score + 20)
        if points >= 100:
            return min(self.MAX_SCORE, score + 15)
        if points >= 50:
            return min(self.MAX_SCORE, score + 10)
        return score

    def _evaluate_relevance(self, url: str, title: str, description: str) -> float:
        """评估内容相关性 (0-100)"""
        score = self.MIN_SCORE
        text = f"{url} {title} {description}".lower()

        keyword_matches = sum(1 for kw in self.keywords if kw in text)
        if keyword_matches > 0:
            score = min(self.MAX_SCORE, 40 + (keyword_matches * 15))

        if any(kw in title.lower() for kw in self.keywords):
            score = min(self.MAX_SCORE, score + 20)

        return score

    def _evaluate_freshness(self, metadata: dict[str, Any]) -> float:
        """评估时效性 (0-100)"""
        date_str = metadata.get("updated_at") or metadata.get("created_at")
        if not date_str:
            return self.DEFAULT_SCORE

        try:
            date = self._parse_date(date_str)
            days_old = (datetime.now(date.tzinfo) - date).days
            return self._score_by_age(days_old)
        except Exception:
            return self.DEFAULT_SCORE

    def _parse_date(self, date_str: str | datetime) -> datetime:
        """解析日期字符串"""
        if isinstance(date_str, str):
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_str

    def _score_by_age(self, days_old: int) -> float:
        """根据天数计算时效性分数"""
        if days_old <= 30:
            return 100.0
        if days_old <= 90:
            return 90.0
        if days_old <= 180:
            return 75.0
        if days_old <= 365:
            return 60.0
        if days_old <= 730:
            return 40.0
        return 20.0

    def _evaluate_activity(self, source_type: str, metadata: dict[str, Any]) -> float:
        """评估活跃度 (0-100)"""
        if source_type == "github":
            return self._evaluate_github_activity(metadata)
        if source_type == "hackernews":
            return self._evaluate_hackernews_activity(metadata)
        return self.DEFAULT_SCORE

    def _evaluate_github_activity(self, metadata: dict[str, Any]) -> float:
        """评估 GitHub 活跃度"""
        stars = metadata.get("stars", 0)
        if stars >= 1000:
            return 100.0
        if stars >= 500:
            return 85.0
        if stars >= 100:
            return 70.0
        if stars >= 50:
            return 55.0
        return 40.0

    def _evaluate_hackernews_activity(self, metadata: dict[str, Any]) -> float:
        """评估 HackerNews 活跃度"""
        points = metadata.get("points", 0)
        if points >= 200:
            return 100.0
        if points >= 100:
            return 85.0
        if points >= 50:
            return 70.0
        return 55.0

    def filter_high_quality(self, items: list[DiscoveredItem], min_score: float = 60.0) -> list[DiscoveredItem]:
        """过滤高质量 URL"""
        scored_items = []
        for item in items:
            score = self.evaluate(item.url, item.title, item.description, item.source_type, item.metadata)
            if score.total >= min_score:
                item.metadata["quality_score"] = score.total
                item.metadata["quality_details"] = {
                    "source": score.source_score,
                    "relevance": score.relevance_score,
                    "freshness": score.freshness_score,
                    "activity": score.activity_score,
                }
                scored_items.append(item)

        return sorted(scored_items, key=lambda x: x.metadata["quality_score"], reverse=True)



class DataSource(ABC):
    """数据源抽象基类"""

    NAME: str = ""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def log(self, msg: str) -> None:
        if self.verbose:
            print(f"  [{self.NAME}] {msg}")

    @abstractmethod
    def search(self, keywords: list[str], limit: int = 10) -> list[DiscoveredItem]:
        """根据关键词搜索资源"""
        pass


class DomainDiscoverScript(ScriptBase):
    """Domain 发现脚本基类"""

    DOMAIN_CODE: str = ""
    KEYWORDS: list[str] = []
    SOURCES: list[DataSource] = []
    OUTPUT_DIR: Path = Path(__file__).parent / "raw_data"
    MIN_QUALITY_SCORE: float = 60.0
    SLEEP_SECONDS: int = 1
    CATEGORY_KEYWORDS: dict[str, list[str]] = {}

    def __init__(self, verbose: bool = False, enable_quality_filter: bool = True, sync_to_db: bool = True) -> None:
        super().__init__(verbose)
        self.enable_quality_filter = enable_quality_filter
        self.sync_to_db = sync_to_db
        self._init_sources()

    def _init_sources(self) -> None:
        """初始化数据源，子类可重写"""
        pass

    def add_source(self, source: DataSource) -> None:
        """添加数据源"""
        self.SOURCES.append(source)

    def _get_output_path(self) -> Path:
        return self.OUTPUT_DIR / f"raw_{self.DOMAIN_CODE}_urls.py"

    def _escape(self, s: str) -> str:
        if not s:
            return ""
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", "")

    def _map_category(self, item: DiscoveredItem) -> str:
        """根据标签和内容映射分类"""
        if not self.CATEGORY_KEYWORDS:
            return "other"
        
        text = f"{' '.join(item.tags)} {item.title} {item.description}".lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return category
        return "other"

    def _get_domain_tags(self) -> list[dict[str, Any]]:
        """获取当前领域的标签列表，子类可重写"""
        return []

    def _match_tags(self, item: DiscoveredItem) -> list[str]:
        """根据内容匹配标签"""
        domain_tags = self._get_domain_tags()
        if not domain_tags:
            return []
        
        matched_tags = []
        text = f"{item.title} {item.description}".lower()
        
        for tag in domain_tags:
            name_en = tag.get("name_en", "").lower()
            code = tag.get("code", "").replace("_", " ").lower()
            
            if name_en and name_en in text:
                matched_tags.append(tag["code"])
            elif code and code in text:
                matched_tags.append(tag["code"])
        
        return list(set(matched_tags))

    def _save_to_file(self, items: list[DiscoveredItem]) -> None:
        """保存数据到文件（每次覆盖）"""
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        output_path = self._get_output_path()

        data_name = f"RAW_{self.DOMAIN_CODE.upper()}_URLS"
        data_list = []
        
        for item in items:
            category = self._map_category(item)
            data_list.append(item.to_standard_format(category))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {self.DOMAIN_CODE} 领域 URL 资源 - 自动生成\n")
            f.write("from typing import Any\n\n")
            f.write(f"{data_name}: list[dict[str, Any]] = [\n")

            for item in data_list:
                f.write("    {\n")
                f.write(f'        "url": "{self._escape(item["url"])}",\n')
                f.write(f'        "name": "{self._escape(item["name"])}",\n')
                f.write(f'        "description": "{self._escape(item["description"][:500])}",\n')
                f.write(f'        "category": "{item["category"]}",\n')
                f.write(f'        "source": "{item["source"]}",\n')
                f.write(f'        "repo": "{self._escape(item["repo"])}",\n')
                f.write(f'        "platform": "{item["platform"]}",\n')
                f.write(f'        "tags": {item["tags"]},\n')
                f.write(f'        "metadata": {item["metadata"]},\n')
                f.write(f'        "is_active": {item["is_active"]},\n')
                f.write("    },\n")

            f.write("]\n")

        self.info(f"已保存 {len(data_list)} 条数据到 {output_path}")

    def discover(self, limit_per_source: int = 10) -> list[DiscoveredItem]:
        """从所有数据源发现资源"""
        all_items: dict[str, DiscoveredItem] = {}

        for source in self.SOURCES:
            self.info(f"从 {source.NAME} 搜索...")
            try:
                items = source.search(self.KEYWORDS, limit_per_source)
                self._process_discovered_items(items, all_items)
                self.info(f"  发现 {len(items)} 个资源")
            except Exception as e:
                self.error(f"  {source.NAME} 搜索失败: {e}")
            time.sleep(self.SLEEP_SECONDS)

        items_list = list(all_items.values())
        return self._apply_quality_filter(items_list)

    def _process_discovered_items(self, items: list[DiscoveredItem], all_items: dict[str, DiscoveredItem]) -> None:
        """处理发现的资源项"""
        for item in items:
            item.domain_code = self.DOMAIN_CODE
            item.tags = self._match_tags(item)
            if item.url not in all_items:
                all_items[item.url] = item
                print(f"    - {item.title}: {item.url}")

    def _apply_quality_filter(self, items: list[DiscoveredItem]) -> list[DiscoveredItem]:
        """应用质量过滤"""
        if not self.enable_quality_filter or not items:
            return items

        items = [item for item in items if item.tags]
        self.info(f"过滤无标签资源后剩余 {len(items)} 个")

        self.info(f"开始质量评估（最低分数: {self.MIN_QUALITY_SCORE}）...")
        evaluator = QualityEvaluator(self.KEYWORDS)
        filtered_items = evaluator.filter_high_quality(items, self.MIN_QUALITY_SCORE)
        self.info(f"  过滤后保留 {len(filtered_items)}/{len(items)} 个高质量资源")
        return filtered_items

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info(f"开始发现 [{self.DOMAIN_CODE}] 领域资源...")

        try:
            items = self.discover()
            self._save_to_file(items)
            self.success(f"共发现 {len(items)} 个资源")
            return ScriptResult(success=True, message=f"Discovered {len(items)}", created=len(items))
        except Exception as e:
            self.error(f"发现失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])
