# Claude Prompts 资源发现脚本
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from scripts.discover.base import DomainDiscoverScript, DiscoveredItem
from scripts.discover.sources.github import GitHubSource
from scripts.discover.sources.hackernews import HackerNewsSource


class DiscoverPromptsScript(DomainDiscoverScript):
    """从 GitHub 和 HackerNews 发现最新的 Prompt 资源"""

    NAME = "discover_prompts"
    DESCRIPTION = "发现 Claude Prompt Engineering 最新资源"
    DOMAIN_CODE = "ai_prompts"
    KEYWORDS = ["claude prompt", "prompt engineering", "claude prompts", "anthropic prompt"]
    MIN_QUALITY_SCORE = 60.0
    
    CATEGORY_KEYWORDS = {
        "library": ["library", "collection", "repository", "prompts"],
        "tutorial": ["tutorial", "guide", "course", "learning"],
        "tool": ["tool", "generator", "builder", "template"],
        "best-practices": ["best practices", "tips", "techniques", "patterns"],
    }
    
    RAW_AI_PROMPTS_DIR = Path(__file__).parent.parent / "raw_data" / "ai_prompts"
    RAW_EXAMPLES_DIR = RAW_AI_PROMPTS_DIR / "examples"
    
    DOWNLOAD_REPOS = [
        "f/awesome-chatgpt-prompts",
        "brexhq/prompt-engineering",
        "dair-ai/Prompt-Engineering-Guide",
    ]

    def __init__(self, verbose: bool = False, download_samples: bool = True) -> None:
        super().__init__(verbose, enable_quality_filter=True, sync_to_db=False)
        self.download_samples = download_samples
        load_dotenv(Path(__file__).parents[3] / ".env", override=True)
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        
        if self.download_samples:
            os.makedirs(self.RAW_AI_PROMPTS_DIR, exist_ok=True)
            os.makedirs(self.RAW_EXAMPLES_DIR, exist_ok=True)

    def _init_sources(self) -> None:
        self.add_source(GitHubSource(verbose=self.verbose, min_stars=50))
        self.add_source(HackerNewsSource(verbose=self.verbose, min_points=30))

    def discover(self, limit_per_source: int = 10) -> list[DiscoveredItem]:
        """发现资源并下载样例"""
        items = super().discover(limit_per_source)
        
        if self.download_samples:
            self._download_prompt_samples()
        
        return items

    def _download_prompt_samples(self) -> None:
        """下载精选的 Prompt 样例"""
        self.info("开始下载 Prompt 样例...")
        
        for repo in self.DOWNLOAD_REPOS:
            self._download_repo_samples(repo)

    def _download_repo_samples(self, repo: str) -> None:
        """下载单个仓库的样例"""
        self.info(f"  下载 {repo}...")
        
        repo_name = repo.split("/")[1]
        repo_dir = self.RAW_EXAMPLES_DIR / repo_name
        os.makedirs(repo_dir, exist_ok=True)
        
        url = f"https://api.github.com/repos/{repo}/contents"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            contents = resp.json()
            
            downloaded = 0
            for item in contents:
                if item["type"] == "file":
                    if self._should_download_file(item["name"]):
                        if self._download_file(item, repo_dir):
                            downloaded += 1
                            if downloaded >= 10:
                                break
            
            self.info(f"    ✓ 已下载 {downloaded} 个文件")
            
        except Exception as e:
            self.error(f"    下载失败: {e}")

    def _should_download_file(self, filename: str) -> bool:
        """判断是否应该下载该文件"""
        allowed_extensions = [".md", ".txt", ".json", ".yaml", ".yml"]
        excluded_files = ["LICENSE", "CONTRIBUTING", "CODE_OF_CONDUCT"]
        
        if any(filename.upper().startswith(ex) for ex in excluded_files):
            return False
        
        return any(filename.endswith(ext) for ext in allowed_extensions)

    def _download_file(self, file_item: dict, target_dir: Path) -> bool:
        """下载单个文件"""
        file_name = file_item["name"]
        download_url = file_item.get("download_url")
        
        if not download_url:
            return False
        
        try:
            resp = requests.get(download_url, timeout=30)
            resp.raise_for_status()
            
            file_path = target_dir / file_name
            with open(file_path, "wb") as f:
                f.write(resp.content)
            
            return True
        except Exception:
            return False




if __name__ == "__main__":
    script = DiscoverPromptsScript(verbose=True)
    result = script.run()
    print(result)
