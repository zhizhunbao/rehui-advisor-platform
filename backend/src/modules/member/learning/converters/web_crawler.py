"""网页抓取转 markdown"""
import httpx
from src.common.errors import AppError, AppErrorCode


class WebCrawler:
    """抓取网页内容并转换为 markdown"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def fetch(self, url: str) -> str:
        """抓取网页并转换为 markdown"""
        try:
            import html2text
        except ImportError:
            raise AppError(
                AppErrorCode.CONFIGURATION_ERROR,
                "html2text library not installed. Run: pip install html2text",
            )
        
        try:
            response = httpx.get(url, timeout=self.timeout, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise AppError(
                AppErrorCode.EXTERNAL_SERVICE_ERROR,
                f"Failed to fetch URL: {str(e)}",
            )
        
        # 转换为 markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # 不换行
        
        markdown = h.handle(response.text)
        return markdown.strip()
