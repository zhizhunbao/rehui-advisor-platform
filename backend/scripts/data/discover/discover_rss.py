# RSS 资源发现脚本 - 解析 RSS 订阅发现新资源
import os
from typing import Any, Dict, List
import feedparser

from scripts.base import ScriptBase, ScriptResult
from scripts.data.initial.discover.urls import RSS_FEEDS
from scripts.data.initial.domain.tags import TAGS


class DiscoverRSSScript(ScriptBase):
    """解析 RSS 订阅发现新资源"""

    NAME = "discover_rss"
    DESCRIPTION = "解析 RSS 订阅发现新资源"
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data_source", "rss", "__init__.py")

    def _escape_string(self, s: str) -> str:
        """转义字符串中的特殊字符"""
        if not s:
            return ""
        return s.replace("\\", "\\\\").replace('"', "'").replace("\n", " ").replace("\r", "")

    def init_file(self) -> None:
        """初始化输出文件"""
        os.makedirs(os.path.dirname(self.OUTPUT_FILE), exist_ok=True)
        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("# RSS 数据源 - 由 discover_rss.py 脚本自动生成\n")
            f.write("from typing import List, Dict, Any\n\n")
            f.write("RSS_SOURCES: List[Dict[str, Any]] = [\n")

    def append_to_file(self, item: Dict[str, Any]) -> None:
        """追加单条记录到文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("    {\n")
            f.write(f'        "url": "{item["url"]}",\n')
            f.write(f'        "name": "{self._escape_string(item["name"])}",\n')
            f.write(f'        "description": "{self._escape_string(item["description"])}",\n')
            f.write(f'        "source_type": "{item["source_type"]}",\n')
            f.write(f'        "source_url": "{item["source_url"]}",\n')
            f.write(f'        "published_at": "{item["published_at"]}",\n')
            f.write(f'        "tags": {item["tags"]},\n')
            f.write("    },\n")

    def close_file(self) -> None:
        """关闭文件"""
        with open(self.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("]\n\n")
            f.write('__all__ = ["RSS_SOURCES"]\n')

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return [tag["name_en"].lower() for tag in TAGS]

    def parse_feed(self, url: str) -> List[Dict[str, Any]]:
        """解析 RSS feed"""
        try:
            feed = feedparser.parse(url)
            return feed.entries
        except Exception as e:
            self.error(f"解析失败: {url} - {e}")
            return []

    def match_tags(self, content: str, tags: List[str]) -> List[str]:
        """匹配内容中的标签"""
        content_lower = content.lower()
        return [tag for tag in tags if tag in content_lower]

    def discover_all(self) -> int:
        """发现所有 RSS 资源"""
        all_tags = self.get_all_tags()
        seen_urls: set = set()
        count = 0

        self.init_file()

        for feed_url in RSS_FEEDS:
            self.info(f"解析 RSS: {feed_url}")
            entries = self.parse_feed(feed_url)

            for entry in entries:
                url = entry.get("link", "")
                if not url or url in seen_urls:
                    continue

                title = entry.get("title", "")
                summary = entry.get("summary", "")
                content = f"{title} {summary}"
                matched_tags = self.match_tags(content, all_tags)

                seen_urls.add(url)
                item = {
                    "url": url,
                    "name": title,
                    "description": summary[:200] if summary else "",
                    "source_type": "rss",
                    "source_url": feed_url,
                    "published_at": entry.get("published", ""),
                    "tags": matched_tags,
                }
                self.append_to_file(item)
                count += 1

        self.close_file()
        return count

    def run(self) -> ScriptResult:
        """执行发现任务"""
        self.info("开始 RSS 资源发现...")

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
    script = DiscoverRSSScript(verbose=True)
    result = script.run()
    print(result)
