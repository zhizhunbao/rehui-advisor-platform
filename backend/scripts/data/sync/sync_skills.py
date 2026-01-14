# 同步脚本 - 从 GitHub 同步 Claude Skills 到本地文件
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from scripts.base import SyncScript


GITHUB_API = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com"
OFFICIAL_REPO = "anthropics/skills"
OFFICIAL_SKILLS_PATH = "skills"


class SyncSkillsScript(SyncScript):
    """从 GitHub 同步 Claude Skills 到本地文件"""

    NAME = "Skills 同步"
    DESCRIPTION = "从 GitHub 同步 Anthropic Claude Skills 到本地数据文件"

    def sync(self) -> int:
        """执行同步"""
        all_skills: List[Dict[str, Any]] = []

        official = self._fetch_official_skills()
        all_skills.extend(official)

        seen = set()
        unique_skills = []
        for skill in all_skills:
            if skill["name"] not in seen:
                seen.add(skill["name"])
                unique_skills.append(skill)

        self._save_to_file(unique_skills)
        return len(unique_skills)

    def _fetch_official_skills(self) -> List[Dict[str, Any]]:
        """获取官方 Skills"""
        self.info("获取官方 Skills...")

        folders = self._get_skill_folders(OFFICIAL_REPO, OFFICIAL_SKILLS_PATH)
        self.info(f"  找到 {len(folders)} 个官方 skills")

        skills = []
        for folder in folders:
            skill_name = folder["name"]
            content = self._get_skill_content(OFFICIAL_REPO, folder["path"])

            if content:
                parsed = self._parse_skill_md(content)
                if not parsed["name"]:
                    parsed["name"] = skill_name

                parsed["folder"] = skill_name
                parsed["source"] = "official"
                parsed["repo"] = OFFICIAL_REPO
                parsed["category"] = self._infer_category(skill_name, parsed.get("description", ""), content)

                skills.append(parsed)
                self.info(f"  ✓ {skill_name} [{parsed['category']}]")
            else:
                self.warning(f"  ✗ {skill_name} (无 SKILL.md)")

        return skills

    def _get_skill_folders(self, repo: str, path: str = "") -> List[Dict[str, str]]:
        """获取仓库中的 skill 文件夹"""
        url = f"{GITHUB_API}/repos/{repo}/contents/{path}" if path else f"{GITHUB_API}/repos/{repo}/contents"
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=30)

        if response.status_code != 200:
            self.warning(f"无法访问 {repo}/{path}: {response.status_code}")
            return []

        folders = []
        for item in response.json():
            if item["type"] == "dir":
                folders.append({"name": item["name"], "path": item["path"]})
        return folders

    def _get_skill_content(self, repo: str, skill_path: str) -> Optional[str]:
        """获取 SKILL.md 内容"""
        for branch in ["main", "master"]:
            url = f"{RAW_GITHUB}/{repo}/{branch}/{skill_path}/SKILL.md"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
        return None

    def _parse_skill_md(self, content: str) -> Dict[str, str]:
        """解析 SKILL.md 内容"""
        name = ""
        description = ""

        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            fm = frontmatter_match.group(1)
            name_match = re.search(r'name:\s*["\']?([^"\'\n]+)', fm)
            desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)', fm)
            if name_match:
                name = name_match.group(1).strip()
            if desc_match:
                description = desc_match.group(1).strip()

        body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL).strip()

        return {"name": name, "description": description, "template": body}

    def _infer_category(self, name: str, description: str, content: str) -> str:
        """根据名称和描述推断分类"""
        text = (name + " " + description + " " + content[:500]).lower()

        category_keywords = {
            "development": ["code", "develop", "build", "test", "debug", "git"],
            "collaboration": ["review", "team", "meeting", "linear", "notion"],
            "learning": ["learn", "knowledge", "pattern", "think", "insight"],
            "security": ["security", "test", "verify", "debug", "fuzzing"],
            "automation": ["automate", "organize", "file", "invoice", "template"],
            "writing": ["write", "article", "content", "research", "brainstorm"],
            "data": ["data", "csv", "sql", "postgres", "analyze"],
            "media": ["video", "youtube", "image", "epub", "transcript"],
            "design": ["design", "image", "visual", "art", "canvas"],
            "document": ["document", "pdf", "pptx", "docx", "presentation"],
        }

        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return category

        return "tool"

    def _save_to_file(self, skills: List[Dict[str, Any]]) -> None:
        """保存到本地 Python 文件"""
        output_path = Path(__file__).parent / "data" / "skills.py"

        lines = [
            "# Claude Skills 数据 (自动生成，请勿手动修改)",
            "from typing import Any, Dict, List",
            "",
            "SKILLS: List[Dict[str, Any]] = [",
        ]

        for skill in skills:
            lines.append("    {")
            lines.append(f'        "name": {repr(skill.get("name", ""))},')
            lines.append(f'        "description": {repr(skill.get("description", ""))},')
            lines.append(f'        "category": {repr(skill.get("category", "tool"))},')
            lines.append(f'        "source": {repr(skill.get("source", "official"))},')
            lines.append(f'        "repo": {repr(skill.get("repo", ""))},')
            lines.append(f'        "folder": {repr(skill.get("folder", ""))},')
            template = skill.get("template", "")
            lines.append(f'        "template": {repr(template)},')
            lines.append("    },")

        lines.append("]")
        lines.append("")

        output_path.write_text("\n".join(lines), encoding="utf-8")
        self.success(f"已保存到 {output_path}")


if __name__ == "__main__":
    script = SyncSkillsScript()
    result = script.run()
    exit(0 if result.success else 1)
