# Claude Skills 官方仓库发现脚本
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from scripts.discover.base import DomainDiscoverScript, DiscoveredItem


class DiscoverSkillsScript(DomainDiscoverScript):
    """从 anthropics/skills 官方仓库发现 Claude Skills"""

    NAME = "discover_skills"
    DESCRIPTION = "发现 Claude Skills 官方资源"
    DOMAIN_CODE = "ai_skills"
    KEYWORDS = ["claude", "skill"]
    OFFICIAL_REPO = "anthropics/skills"
    MIN_QUALITY_SCORE = 0.0
    RAW_AI_SKILLS_DIR = Path(__file__).parent.parent / "raw_data" / "ai_skills"
    RAW_SKILLS_DIR = RAW_AI_SKILLS_DIR / "skills"
    RAW_SPEC_DIR = RAW_AI_SKILLS_DIR / "spec"

    def __init__(self, verbose: bool = False, download_content: bool = True) -> None:
        super().__init__(verbose, enable_quality_filter=False, sync_to_db=False)
        self.download_content = download_content
        load_dotenv(Path(__file__).parents[3] / ".env", override=True)
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        
        if self.download_content:
            os.makedirs(self.RAW_AI_SKILLS_DIR, exist_ok=True)
            os.makedirs(self.RAW_SKILLS_DIR, exist_ok=True)
            os.makedirs(self.RAW_SPEC_DIR, exist_ok=True)

    def discover(self, limit_per_source: int = 10) -> list[DiscoveredItem]:
        """从官方仓库发现 skills"""
        self.info(f"从官方仓库 {self.OFFICIAL_REPO} 获取 skills...")
        
        try:
            if self.download_content:
                self._download_spec_docs()
            
            repo_item = self._fetch_repo_info()
            skills = self._fetch_skills_from_repo()
            
            spec_item = self._create_spec_item()
            if spec_item:
                skills.append(spec_item)
            
            if not skills:
                self.info("  未发现 skills，返回仓库信息")
                return [repo_item] if repo_item else []
            
            self.info(f"  发现 {len(skills)} 个资源")
            return skills
            
        except Exception as e:
            self.error(f"获取失败: {e}")
            return []

    def _create_spec_item(self) -> DiscoveredItem | None:
        """创建 spec 规范文档的资源项"""
        return DiscoveredItem(
            url="https://github.com/anthropics/skills/tree/main/spec",
            title="agent-skills-spec",
            description="Agent Skills 规范文档，定义了 skills 的标准格式和最佳实践",
            source_type="github",
            domain_code=self.DOMAIN_CODE,
            tags=["spec", "documentation", "official"],
            metadata={
                "repo": self.OFFICIAL_REPO,
                "resource_type": "specification",
                "spec_url": "https://agentskills.io/specification",
            },
        )

    def _download_spec_docs(self) -> None:
        """下载 spec 规范文档"""
        url = "https://api.github.com/repos/anthropics/skills/contents/spec"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            contents = resp.json()
            
            for item in contents:
                if item["type"] == "file":
                    download_url = item.get("download_url")
                    if download_url:
                        file_resp = requests.get(download_url, timeout=30)
                        file_resp.raise_for_status()
                        
                        file_path = self.RAW_SPEC_DIR / item["name"]
                        with open(file_path, "wb") as f:
                            f.write(file_resp.content)
                        
                        self.info(f"  ✓ 已下载规范: {item['name']}")
        except Exception as e:
            self.error(f"下载规范文档失败: {e}")

    def _fetch_repo_info(self) -> DiscoveredItem | None:
        """获取仓库基本信息"""
        url = f"https://api.github.com/repos/{self.OFFICIAL_REPO}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            repo = resp.json()
            
            return DiscoveredItem(
                url=repo["html_url"],
                title=repo["name"],
                description=repo.get("description") or "Claude Skills 官方仓库",
                source_type="github",
                domain_code=self.DOMAIN_CODE,
                tags=[t.lower() for t in repo.get("topics", [])],
                metadata={
                    "stars": repo["stargazers_count"],
                    "updated_at": repo["updated_at"],
                    "full_name": repo["full_name"],
                },
            )
        except Exception as e:
            self.error(f"获取仓库信息失败: {e}")
            return None

    def _fetch_skills_from_repo(self) -> list[DiscoveredItem]:
        """从仓库中获取所有 skills"""
        skills = []
        
        skills.extend(self._fetch_skills_from_path(""))
        skills.extend(self._fetch_skills_from_path("skills"))
        
        return skills

    def _fetch_skills_from_path(self, path: str) -> list[DiscoveredItem]:
        """从指定路径获取 skills"""
        url = f"https://api.github.com/repos/{self.OFFICIAL_REPO}/contents/{path}" if path else f"https://api.github.com/repos/{self.OFFICIAL_REPO}/contents"
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            contents = resp.json()
            
            skills = []
            for item in contents:
                if item["type"] == "dir" and not item["name"].startswith("."):
                    skill_path = f"{path}/{item['name']}" if path else item["name"]
                    
                    if self._has_skill_md(skill_path):
                        skill = self._parse_skill_dir(item, skill_path)
                        if skill:
                            skills.append(skill)
                            print(f"    - {skill.title} ({skill_path})")
            
            return skills
            
        except Exception as e:
            self.error(f"获取路径 {path} 失败: {e}")
            return []

    def _has_skill_md(self, skill_path: str) -> bool:
        """检查目录是否包含 SKILL.md"""
        url = f"https://api.github.com/repos/{self.OFFICIAL_REPO}/contents/{skill_path}/SKILL.md"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            return resp.status_code == 200
        except Exception:
            return False

    def _parse_skill_dir(self, dir_item: dict, skill_path: str) -> DiscoveredItem | None:
        """解析 skill 目录信息"""
        skill_name = dir_item["name"]
        skill_url = f"https://github.com/{self.OFFICIAL_REPO}/tree/main/{skill_path}"
        
        skill_md_content = self._fetch_skill_md(skill_path)
        
        if skill_md_content:
            metadata = self._parse_skill_metadata(skill_md_content, skill_name, skill_path)
            description = metadata.get("description", f"Claude Skill: {skill_name}")
            tags = metadata.get("keywords", ["skill", "official"])
            
            if self.download_content:
                self._download_skill_content(skill_name, skill_path, skill_md_content, metadata)
        else:
            readme_content = self._fetch_readme(skill_path)
            description = self._extract_description(readme_content) if readme_content else f"Claude Skill: {skill_name}"
            tags = ["skill", "official"]
            metadata = {
                "repo": self.OFFICIAL_REPO,
                "skill_name": skill_name,
                "skill_path": skill_path,
                "has_skill_md": False,
            }
        
        return DiscoveredItem(
            url=skill_url,
            title=metadata.get("name", skill_name),
            description=description,
            source_type="github",
            domain_code=self.DOMAIN_CODE,
            tags=tags,
            metadata=metadata,
        )

    def _fetch_readme(self, skill_path: str) -> str | None:
        """获取 skill 的 README 内容"""
        url = f"https://api.github.com/repos/{self.OFFICIAL_REPO}/contents/{skill_path}/README.md"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            
            import base64
            content = resp.json().get("content", "")
            return base64.b64decode(content).decode("utf-8")
            
        except Exception:
            return None

    def _fetch_skill_md(self, skill_path: str) -> str | None:
        """获取 skill 的 SKILL.md 内容"""
        url = f"https://api.github.com/repos/{self.OFFICIAL_REPO}/contents/{skill_path}/SKILL.md"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            
            import base64
            content = resp.json().get("content", "")
            return base64.b64decode(content).decode("utf-8")
            
        except Exception:
            return None

    def _parse_skill_metadata(self, skill_md: str, skill_name: str, skill_path: str) -> dict:
        """从 SKILL.md 解析元数据"""
        metadata = {
            "repo": self.OFFICIAL_REPO,
            "skill_name": skill_name,
            "skill_path": skill_path,
            "has_skill_md": True,
        }
        
        lines = skill_md.split("\n")
        in_frontmatter = False
        frontmatter_lines = []
        content_lines = []
        
        for line in lines:
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    in_frontmatter = False
                    continue
            
            if in_frontmatter:
                frontmatter_lines.append(line)
            else:
                content_lines.append(line)
        
        for line in frontmatter_lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                
                if key == "keywords":
                    metadata["keywords"] = [k.strip() for k in value.split(",")]
                elif key in ["name", "description", "version", "author"]:
                    metadata[key] = value
        
        instructions = "\n".join(content_lines).strip()
        if instructions:
            metadata["instructions"] = instructions[:500]
        
        if "keywords" not in metadata:
            metadata["keywords"] = ["skill", "official"]
        
        return metadata

    def _extract_description(self, readme: str) -> str:
        """从 README 提取描述"""
        lines = readme.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("# "):
                if i + 1 < len(lines) and lines[i + 1].strip():
                    return lines[i + 1].strip()[:200]
        
        for line in lines:
            if line.strip() and not line.startswith("#"):
                return line.strip()[:200]
        
        return "Claude Skill"

    def _download_skill_content(self, skill_name: str, skill_path: str, skill_md: str, metadata: dict) -> None:
        """下载 skill 的完整内容到本地目录"""
        skill_dir = self.RAW_SKILLS_DIR / skill_name
        os.makedirs(skill_dir, exist_ok=True)
        
        with open(skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_md)
        
        with open(skill_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        readme = self._fetch_readme(skill_path)
        if readme:
            with open(skill_dir / "README.md", "w", encoding="utf-8") as f:
                f.write(readme)
        
        self._download_skill_files(skill_path, skill_dir)
        
        self.info(f"  ✓ 已下载: {skill_name}")

    def _download_skill_files(self, skill_path: str, skill_dir: Path) -> None:
        """下载 skill 目录下的所有文件"""
        url = f"https://api.github.com/repos/{self.OFFICIAL_REPO}/contents/{skill_path}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            contents = resp.json()
            
            for item in contents:
                if item["name"] in ["SKILL.md", "README.md", "LICENSE.txt", "LICENSE"]:
                    continue
                
                if item["type"] == "file":
                    self._download_file(item, skill_dir)
                    
        except Exception as e:
            self.error(f"下载文件失败 {skill_path}: {e}")

    def _download_file(self, file_item: dict, skill_dir: Path) -> None:
        """下载单个文件"""
        file_name = file_item["name"]
        download_url = file_item.get("download_url")
        
        if not download_url:
            return
        
        try:
            resp = requests.get(download_url, timeout=30)
            resp.raise_for_status()
            
            file_path = skill_dir / file_name
            with open(file_path, "wb") as f:
                f.write(resp.content)
                
        except Exception:
            pass

    def _map_category(self, item: DiscoveredItem) -> str:
        """映射资源分类"""
        if "spec" in item.tags or "documentation" in item.tags:
            return "documentation"
        return "skill"


if __name__ == "__main__":
    script = DiscoverSkillsScript(verbose=True)
    result = script.run()
    print(result)
