#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "playwright>=1.40.0",
#     "beautifulsoup4>=4.12.0",
#     "lxml>=4.9.0",
# ]
# ///
"""
抓取 links.md 文件中的所有链接，生成中英对照文档

用法:
    uv run scrapers/fetch_links.py <links_file_path>
    
示例:
    uv run scrapers/fetch_links.py ../courses/rl/links.md

首次使用需要安装浏览器:
    uv run playwright install chromium
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup


class LinkFetcher:
    """链接抓取器"""
    
    def __init__(self, links_file: Path):
        self.links_file = links_file
        self.course_dir = links_file.parent
        
    def parse_links_file(self) -> list[dict]:
        """解析 links.md 文件，提取所有链接"""
        content = self.links_file.read_text(encoding='utf-8')
        
        # 匹配 Markdown 链接格式: [title](url)
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.findall(pattern, content)
        
        links = []
        for title, url in matches:
            links.append({
                'title': title.strip(),
                'url': url.strip()
            })
        
        print(f"✓ 找到 {len(links)} 个链接")
        return links
    
    def fetch_content(self, url: str) -> str:
        """使用 Playwright 模拟浏览器抓取网页内容"""
        print(f"  正在抓取: {url}")
        
        try:
            with sync_playwright() as p:
                # 启动浏览器（无头模式）
                browser = p.chromium.launch(headless=True)
                
                # 创建新页面
                page = browser.new_page(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                # 访问页面
                print(f"  ⏳ 加载页面...")
                page.goto(url, wait_until='networkidle', timeout=30000)
                
                # 等待内容加载（针对 Medium）
                if 'medium.com' in url:
                    try:
                        page.wait_for_selector('article', timeout=10000)
                    except PlaywrightTimeout:
                        print(f"  ⚠️  等待文章内容超时，尝试继续...")
                
                # 获取页面内容
                html = page.content()
                
                # 关闭浏览器
                browser.close()
                
                print(f"  ✓ 成功获取内容 ({len(html)} 字节)")
                return html
                
        except PlaywrightTimeout:
            print(f"  ✗ 页面加载超时")
            return ""
        except Exception as e:
            print(f"  ✗ 抓取失败: {e}")
            if "Executable doesn't exist" in str(e):
                print(f"  💡 提示: 请先安装浏览器:")
                print(f"     uv run playwright install chromium")
            return ""
    
    def extract_article_content(self, html: str, url: str) -> dict:
        """提取文章内容"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 根据不同网站提取内容
        if 'medium.com' in url:
            return self._extract_medium(soup)
        else:
            return self._extract_generic(soup)
    
    def _extract_medium(self, soup: BeautifulSoup) -> dict:
        """提取 Medium 文章"""
        article = soup.find('article')
        if not article:
            return {'title': '', 'content': ''}
        
        # 提取标题
        title_elem = article.find(['h1', 'h2'])
        title = title_elem.get_text(strip=True) if title_elem else ''
        
        # 提取段落
        paragraphs = []
        for elem in article.find_all(['p', 'h1', 'h2', 'h3', 'pre', 'code']):
            text = elem.get_text(strip=True)
            if text:
                paragraphs.append(text)
        
        return {
            'title': title,
            'content': '\n\n'.join(paragraphs)
        }
    
    def _extract_generic(self, soup: BeautifulSoup) -> dict:
        """通用内容提取"""
        # 移除脚本和样式
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # 提取标题
        title_elem = soup.find(['h1', 'title'])
        title = title_elem.get_text(strip=True) if title_elem else ''
        
        # 提取正文
        main_content = soup.find(['article', 'main', 'div.content', 'div.post'])
        if not main_content:
            main_content = soup.find('body')
        
        paragraphs = []
        if main_content:
            for elem in main_content.find_all(['p', 'h1', 'h2', 'h3', 'pre']):
                text = elem.get_text(strip=True)
                if text and len(text) > 20:  # 过滤太短的文本
                    paragraphs.append(text)
        
        return {
            'title': title,
            'content': '\n\n'.join(paragraphs)
        }
    
    def create_bilingual_doc(self, link_info: dict, article: dict) -> str:
        """创建中英对照文档"""
        title = link_info['title']
        url = link_info['url']
        content = article['content']
        
        # 分段
        paragraphs = content.split('\n\n')
        
        doc = f"""# {title} (中英对照)

> **原文链接:** {url}

---

"""
        
        for i, para in enumerate(paragraphs, 1):
            if not para.strip():
                continue
            
            # 检测是否是标题
            if para.startswith('#') or len(para) < 100:
                doc += f"## 段落 {i}\n\n"
            
            doc += f"""**原文:**
{para}

**翻译:**
[待翻译]

---

"""
        
        doc += """
## 学习建议

根据 RL skill 的指导，现在你可以：

1. **理解核心概念** - 仔细阅读原文和翻译
2. **做笔记** - 标记重点和疑问
3. **实践** - 如果有代码示例，动手实现
4. **提问** - 对不理解的部分提问

需要我帮你：
- 翻译某个段落？
- 解释某个概念？
- 实现相关代码？
"""
        
        return doc
    
    def save_document(self, filename: str, content: str):
        """保存文档"""
        output_path = self.course_dir / filename
        output_path.write_text(content, encoding='utf-8')
        print(f"  ✓ 已保存: {output_path}")
    
    def run(self):
        """执行抓取"""
        print(f"\n开始处理: {self.links_file}")
        print("=" * 60)
        
        # 解析链接
        links = self.parse_links_file()
        if not links:
            print("✗ 没有找到链接")
            return
        
        # 处理每个链接
        success_count = 0
        for i, link in enumerate(links, 1):
            print(f"\n[{i}/{len(links)}] {link['title']}")
            
            # 抓取内容
            html = self.fetch_content(link['url'])
            if not html:
                print("  ⚠️  跳过此链接，你可以:")
                print("     - 手动复制文章内容到文件")
                print("     - 或使用我之前创建的中英对照文档")
                continue
            
            # 提取文章
            article = self.extract_article_content(html, link['url'])
            if not article['content']:
                print("  ✗ 无法提取内容")
                continue
            
            # 生成文件名
            safe_title = re.sub(r'[^\w\s-]', '', link['title'].lower())
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title}_bilingual.md"
            
            # 创建文档
            doc = self.create_bilingual_doc(link, article)
            self.save_document(filename, doc)
            success_count += 1
        
        print("\n" + "=" * 60)
        print(f"✓ 完成! 成功处理 {success_count}/{len(links)} 个链接")
        
        if success_count == 0:
            print("\n💡 如果抓取失败，请确保:")
            print("   1. 已安装浏览器: uv run playwright install chromium")
            print("   2. 网络连接正常")
            print("   3. 或使用我之前创建的中英对照文档")


def main():
    if len(sys.argv) < 2:
        print("用法: uv run fetch_links.py <links_file_path>")
        print("示例: uv run fetch_links.py ../courses/rl/links.md")
        print("\n首次使用需要安装浏览器:")
        print("  uv run playwright install chromium")
        sys.exit(1)
    
    links_file = Path(sys.argv[1])
    
    if not links_file.exists():
        print(f"✗ 文件不存在: {links_file}")
        sys.exit(1)
    
    fetcher = LinkFetcher(links_file)
    fetcher.run()


if __name__ == '__main__':
    main()
