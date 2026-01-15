# Dev.to 资源发现脚本 - 通过标签搜索文章
import os
import time
from typing import Any, Dict, List
import requests

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.domain.tags import TAGS
from scripts.data.initial.domain.domains import DOMAINS
from scripts.data.initial.domain.categories import CATEGORIES


class DiscoverDevToScript(ScriptBase):
    """通过标签搜索 Dev.to 文章"""

    NAME = "discover_devto"
    DESCRIPTION = "通过标签搜索 Dev.to 文章"

    API_URL = "https://dev.to/api"

    def get_all_tags(self) -> List[str]:
        """获取所有标签 - 转换为 Dev.to 格式（小写 + 连字符）"""
        tags = []
        for tag in TAGS:
            name = tag["name_en"].lower().replace(" ", "-")
            tags.append(name)
        return tags

    def get_tag_info(self, tag_code: str) -> Dict[str, str]:
        """获取标签的完整信息（类别、领域、标签）"""
        for tag in TAGS:
            if tag["code"] == tag_code:
                domain_code = tag["domain_code"]
                domain_info = next((d for d in DOMAINS if d["code"] == domain_code), None)
                if domain_info:
                    category_code = domain_info["category_code"]
                    category_info = next((c for c in CATEGORIES if c["code"] == category_code), None)
                    return {
                        "category": category_info["name_en"] if category_info else "Unknown",
                        "domain": domain_info["name_en"],
                        "tag": tag["name_en"],
                    }
        return {"category": "Unknown", "domain": "Unknown", "tag": "Unknown"}

    def search_articles(self, tag: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """搜索文章"""
        url = f"{self.API_URL}/articles"
        params = {"tag": tag, "per_page": per_page, "top": 30}
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            self.error(f"搜索失败: {tag} - {e}")
            return []

    def init_file(self) -> None:
        """初始化输出文件"""
        file_path = os.path.join(
            os.path.dirname(__file__),
            "data_source",
            "devto",
            "__init__.py",
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# Dev.to 数据源 - 按 category 组织\n")
            f.write("# 由 discover_devto.py 脚本自动生成和更新\n")
            f.write("from typing import List, Dict, Any\n\n")
            f.write("DEVTO_SOURCES: List[Dict[str, Any]] = [\n")

    def append_to_file(self, item: Dict[str, Any]) -> None:
        """追加单条记录到文件"""
        file_path = os.path.join(
            os.path.dirname(__file__),
            "data_source",
            "devto",
            "__init__.py",
        )
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("    {\n")
            f.write(f'        "url": "{item["url"]}",\n')
            f.write(f'        "name": "{item["name"].replace(chr(34), chr(39))}",\n')
            f.write(f'        "description": "{item["description"].replace(chr(34), chr(39))}",\n')
            f.write(f'        "source_type": "{item["source_type"]}",\n')
            f.write(f'        "reactions": {item["reactions"]},\n')
            f.write(f'        "comments": {item["comments"]},\n')
            f.write(f'        "published_at": "{item["published_at"]}",\n')
            f.write(f'        "tags": {item["tags"]},\n')
            f.write("    },\n")

    def close_file(self) -> None:
        """关闭文件（写入结束标记）"""
        file_path = os.path.join(
            os.path.dirname(__file__),
            "data_source",
            "devto",
            "__init__.py",
        )
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("]\n")

    def discover_all(self) -> int:
        """发现所有资源"""
        all_tags = [(tag["code"], tag["name_en"].lower().replace(" ", "-")) for tag in TAGS]
        seen_urls: set = set()
        count = 0

        self.init_file()

        for tag_code, tag_name in all_tags:
            tag_info = self.get_tag_info(tag_code)
            self.info(
                f"搜索 [{tag_info['category']}] > [{tag_info['domain']}] > {tag_name}"
            )
            articles = self.search_articles(tag_name)

            for article in articles:
                url = article.get("url", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                
                item = {
                    "url": url,
                    "name": article.get("title", ""),
                    "description": article.get("description", ""),
                    "source_type": "devto",
                    "reactions": article.get("positive_reactions_count", 0),
                    "comments": article.get("comments_count", 0),
                    "published_at": article.get("published_at", ""),
                    "tags": article.get("tag_list", []),
                }
                self.append_to_file(item)
                count += 1

            time.sleep(0.5)

        self.close_file()
        return count

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 Dev.to 资源发现...")

        try:
            count = self.discover_all()
            self.success(f"发现 {count} 个资源并保存到文件")
            return ScriptResult(
                success=True,
                message=f"Discovered {count} resources",
                created=count,
            )
        except Exception as e:
            self.error(f"发现失败: {e}")
            return ScriptResult(success=False, message=str(e), errors=[str(e)])


if __name__ == "__main__":
    script = DiscoverDevToScript(verbose=True)
    result = script.run()
    print(result)
