"""
从 GitHub 获取 Anthropic Claude Skills 并存入数据库

使用方式：
    cd backend
    uv run python scripts/fetch_claude_skills.py
"""
import sys
import re
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from common.supabase import get_supabase_admin

# GitHub API
GITHUB_API = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com"

# 官方仓库
OFFICIAL_REPO = "anthropics/skills"
OFFICIAL_SKILLS_PATH = "skills"

# Claude Plugins Official 仓库
PLUGINS_OFFICIAL_REPO = "anthropics/claude-plugins-official"
PLUGINS_OFFICIAL_PATH = "plugins"

# 分类描述
CATEGORY_INFO = {
    "document": {"name": "文档处理", "name_en": "Document"},
    "design": {"name": "设计创意", "name_en": "Design & Creative"},
    "development": {"name": "开发工具", "name_en": "Development"},
    "communication": {"name": "沟通协作", "name_en": "Communication"},
    "tool": {"name": "实用工具", "name_en": "Tool"},
    "visualization": {"name": "数据可视化", "name_en": "Visualization"},
    "science": {"name": "科学计算", "name_en": "Science"},
    "security": {"name": "安全测试", "name_en": "Security"},
    "data": {"name": "数据分析", "name_en": "Data & Analysis"},
    "writing": {"name": "写作研究", "name_en": "Writing & Research"},
    "learning": {"name": "学习知识", "name_en": "Learning & Knowledge"},
    "media": {"name": "媒体内容", "name_en": "Media & Content"},
    "collaboration": {"name": "协作管理", "name_en": "Collaboration"},
    "automation": {"name": "自动化", "name_en": "Automation"},
    "community": {"name": "社区贡献", "name_en": "Community"},
}

# 官方 Skills 分类映射
OFFICIAL_CATEGORIES = {
    "docx": "document",
    "pdf": "document",
    "pptx": "document",
    "xlsx": "document",
    "algorithmic-art": "design",
    "brand-guidelines": "design",
    "canvas-design": "design",
    "frontend-design": "design",
    "theme-factory": "design",
    "web-artifacts-builder": "design",
    "mcp-builder": "development",
    "webapp-testing": "security",
    "doc-coauthoring": "communication",
    "internal-comms": "communication",
    "slack-gif-creator": "media",
    "skill-creator": "tool",
}

# Claude Code 官方 Plugins (来自 anthropics/claude-code/plugins)
CLAUDE_CODE_PLUGINS = {
    "agent-sdk-dev": {
        "category": "development",
        "description": "Development kit for working with the Claude Agent SDK",
    },
    "claude-opus-4-5-migration": {
        "category": "development",
        "description": "Migrate code and prompts from Sonnet 4.x and Opus 4.1 to Opus 4.5",
    },
    "code-review": {
        "category": "collaboration",
        "description": "Automated PR code review using multiple specialized agents with confidence-based scoring",
    },
    "commit-commands": {
        "category": "collaboration",
        "description": "Git workflow automation for committing, pushing, and creating pull requests",
    },
    "explanatory-output-style": {
        "category": "learning",
        "description": "Adds educational insights about implementation choices and codebase patterns",
    },
    "feature-dev": {
        "category": "development",
        "description": "Comprehensive feature development workflow with a structured 7-phase approach",
    },
    "hookify": {
        "category": "automation",
        "description": "Easily create custom hooks to prevent unwanted behaviors by analyzing conversation patterns",
    },
    "learning-output-style": {
        "category": "learning",
        "description": "Interactive learning mode that requests meaningful code contributions at decision points",
    },
    "plugin-dev": {
        "category": "development",
        "description": "Comprehensive toolkit for developing Claude Code plugins with 7 expert skills",
    },
    "pr-review-toolkit": {
        "category": "collaboration",
        "description": "Comprehensive PR review agents for comments, tests, error handling, type design, code quality",
    },
    "ralph-wiggum": {
        "category": "automation",
        "description": "Interactive self-referential AI loops for iterative development until completion",
    },
    "security-guidance": {
        "category": "security",
        "description": "Security reminder hook that warns about potential security issues when editing files",
    },
}

# 社区 Skills 仓库列表 - 会动态扫描这些仓库获取 skills
COMMUNITY_REPOS = [
    {"repo": "ComposioHQ/awesome-claude-skills", "branch": "master"},
    {"repo": "michalparkola/tapestry-skills-for-claude-code", "branch": "main"},
    {"repo": "BehiSecc/awesome-claude-skills", "branch": "main"},
]

# 额外的独立仓库 skills (不在上述仓库中的)
EXTRA_COMMUNITY_SKILLS = {
    "prompt-engineering": {
        "category": "development",
        "description": "Teaches prompt engineering techniques including Anthropic best practices",
        "repo": "anthropics/courses",
        "path": "prompt_engineering_interactive_tutorial",
    },
}


def get_skill_folders(repo: str, path: str = "") -> list[dict]:
    """获取仓库中的 skill 文件夹"""
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}" if path else f"{GITHUB_API}/repos/{repo}/contents"
    response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    
    if response.status_code != 200:
        print(f"   ✗ 无法访问 {repo}/{path}: {response.status_code}")
        return []
    
    folders = []
    for item in response.json():
        if item["type"] == "dir":
            folders.append({
                "name": item["name"],
                "path": item["path"],
            })
    return folders


def get_skill_content(repo: str, skill_path: str) -> str | None:
    """获取 SKILL.md 内容"""
    url = f"{RAW_GITHUB}/{repo}/main/{skill_path}/SKILL.md"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    
    # 尝试 master 分支
    url = f"{RAW_GITHUB}/{repo}/master/{skill_path}/SKILL.md"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    
    # 尝试根目录
    url = f"{RAW_GITHUB}/{repo}/main/SKILL.md"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    
    return None


def parse_skill_md(content: str) -> dict:
    """解析 SKILL.md 内容"""
    name = ""
    description = ""
    
    # 尝试匹配表格格式
    table_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
    matches = re.findall(table_pattern, content)
    
    if len(matches) >= 2:
        for match in matches:
            col1, col2, col3 = [m.strip() for m in match]
            if col1.lower() == "name" or col1.startswith("-"):
                continue
            name = col1
            description = col2
            break
    
    # 如果没有表格，尝试从 frontmatter 解析
    if not name:
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            fm = frontmatter_match.group(1)
            name_match = re.search(r'name:\s*["\']?([^"\'\n]+)', fm)
            desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)', fm)
            if name_match:
                name = name_match.group(1).strip()
            if desc_match:
                description = desc_match.group(1).strip()
    
    # 提取正文
    body = content
    body = re.sub(r'\|[^\n]+\|(\n\|[^\n]+\|)*', '', body)
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', body, flags=re.DOTALL)
    body = body.strip()
    
    return {
        "name": name,
        "description": description,
        "template": body,
    }


def fetch_official_skills() -> list[dict]:
    """获取官方 Skills"""
    print("1. 获取官方 Skills...")
    
    folders = get_skill_folders(OFFICIAL_REPO, OFFICIAL_SKILLS_PATH)
    print(f"   找到 {len(folders)} 个官方 skills")
    
    skills = []
    for folder in folders:
        skill_name = folder["name"]
        content = get_skill_content(OFFICIAL_REPO, folder["path"])
        
        if content:
            parsed = parse_skill_md(content)
            if not parsed["name"]:
                parsed["name"] = skill_name
            
            parsed["folder"] = skill_name
            parsed["source"] = "official"
            parsed["repo"] = OFFICIAL_REPO
            parsed["category"] = OFFICIAL_CATEGORIES.get(skill_name, "tool")
            
            skills.append(parsed)
            print(f"   ✓ {skill_name} [{parsed['category']}]")
        else:
            print(f"   ✗ {skill_name} (无 SKILL.md)")
    
    return skills


def fetch_community_skills() -> list[dict]:
    """获取社区 Skills - 动态扫描社区仓库"""
    print("\n2. 获取社区 Skills...")
    
    skills = []
    
    # 扫描社区仓库
    for repo_info in COMMUNITY_REPOS:
        repo = repo_info["repo"]
        branch = repo_info["branch"]
        print(f"\n   扫描 {repo}...")
        
        repo_skills = scan_repo_for_skills(repo, branch)
        skills.extend(repo_skills)
    
    # 添加额外的独立仓库 skills
    print(f"\n   获取额外的独立 skills...")
    for skill_name, info in EXTRA_COMMUNITY_SKILLS.items():
        repo = info.get("repo", "")
        path = info.get("path", skill_name)
        content = get_community_skill_content(repo, path) if repo else ""
        
        parsed = {
            "name": skill_name,
            "description": info["description"],
            "template": content,
            "folder": skill_name,
            "source": "community",
            "repo": repo,
            "category": info["category"],
        }
        
        status = "✓" if content else "○"
        print(f"   {status} {skill_name} [{parsed['category']}]")
        skills.append(parsed)
    
    return skills


def scan_repo_for_skills(repo: str, branch: str = "main") -> list[dict]:
    """扫描仓库获取所有 skills"""
    skills = []
    
    # 获取仓库根目录内容
    url = f"{GITHUB_API}/repos/{repo}/contents"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"   ✗ 无法访问 {repo}: {response.status_code}")
            return skills
        
        items = response.json()
        
        for item in items:
            if item["type"] != "dir":
                continue
            
            folder_name = item["name"]
            
            # 跳过非 skill 文件夹
            if folder_name.startswith(".") or folder_name in ["node_modules", "dist", "build", "__pycache__"]:
                continue
            
            # 尝试获取 SKILL.md
            content = get_community_skill_content(repo, folder_name)
            if not content:
                continue
            
            # 解析 SKILL.md 获取 name 和 description
            parsed = parse_skill_md(content)
            name = parsed.get("name") or folder_name
            description = parsed.get("description") or f"Skill from {repo}"
            
            # 推断分类
            category = infer_category(name, description, content)
            
            skill = {
                "name": folder_name,
                "description": description[:500],
                "template": content,
                "folder": folder_name,
                "source": "community",
                "repo": repo,
                "category": category,
            }
            
            skills.append(skill)
            print(f"   ✓ {folder_name} [{category}] ({len(content)} chars)")
            
    except Exception as e:
        print(f"   ✗ 扫描 {repo} 出错: {e}")
    
    return skills


def infer_category(name: str, description: str, content: str) -> str:
    """根据名称和描述推断分类"""
    text = (name + " " + description + " " + content[:500]).lower()
    
    category_keywords = {
        "development": ["code", "develop", "build", "test", "debug", "git", "branch", "implement", "architecture", "sdk", "plugin"],
        "collaboration": ["review", "team", "meeting", "linear", "notion", "parallel", "agent", "dispatch"],
        "learning": ["learn", "knowledge", "pattern", "think", "insight", "understand"],
        "security": ["security", "test", "verify", "debug", "fuzzing", "penetration"],
        "automation": ["automate", "organize", "file", "invoice", "template", "hook"],
        "writing": ["write", "article", "content", "research", "brainstorm"],
        "data": ["data", "csv", "sql", "postgres", "analyze", "trace"],
        "media": ["video", "youtube", "image", "epub", "transcript"],
        "design": ["design", "image", "visual", "art", "canvas"],
        "document": ["document", "pdf", "pptx", "docx", "presentation", "reveal"],
        "science": ["scientific", "simulation", "materials", "bioinformatics"],
        "visualization": ["d3", "chart", "visualization", "graph"],
    }
    
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return "tool"


def get_community_skill_content(repo: str, path: str) -> str:
    """从社区仓库获取 SKILL.md 内容"""
    # 尝试不同的分支和路径组合
    branches = ["main", "master"]
    filenames = ["SKILL.md", "skill.md"]
    
    for branch in branches:
        for filename in filenames:
            url = f"{RAW_GITHUB}/{repo}/{branch}/{path}/{filename}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return response.text
            except Exception:
                pass
    
    return ""


def fetch_claude_code_plugins() -> list[dict]:
    """获取 Claude Code 官方 Plugins - 从 GitHub 抓取实际内容"""
    print("\n3. 获取 Claude Code 官方 Plugins...")
    
    skills = []
    repo = "anthropics/claude-code"
    
    # 获取 plugins 目录
    url = f"{GITHUB_API}/repos/{repo}/contents/plugins"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"   ✗ 无法访问 {repo}/plugins: {response.status_code}")
            # 回退到硬编码列表
            return fetch_claude_code_plugins_fallback()
        
        items = response.json()
        
        for item in items:
            if item["type"] != "dir":
                continue
            
            folder_name = item["name"]
            
            # 跳过非 plugin 文件夹
            if folder_name.startswith("."):
                continue
            
            # 尝试获取 SKILL.md 或 README.md
            content = get_plugin_content(repo, f"plugins/{folder_name}")
            
            # 获取描述
            description = CLAUDE_CODE_PLUGINS.get(folder_name, {}).get("description", f"Claude Code plugin: {folder_name}")
            category = CLAUDE_CODE_PLUGINS.get(folder_name, {}).get("category", "development")
            
            skill = {
                "name": f"cc-{folder_name}",
                "description": description,
                "template": content,
                "folder": folder_name,
                "source": "claude-code",
                "repo": repo,
                "category": category,
            }
            
            skills.append(skill)
            status = "✓" if content else "○"
            print(f"   {status} {folder_name} [{category}]" + (f" ({len(content)} chars)" if content else ""))
            
    except Exception as e:
        print(f"   ✗ 获取 plugins 出错: {e}")
        return fetch_claude_code_plugins_fallback()
    
    return skills


def get_plugin_content(repo: str, path: str) -> str:
    """获取 plugin 的 SKILL.md 或 README.md 内容"""
    branches = ["main", "master"]
    filenames = ["SKILL.md", "skill.md", "README.md"]
    
    for branch in branches:
        for filename in filenames:
            url = f"{RAW_GITHUB}/{repo}/{branch}/{path}/{filename}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return response.text
            except Exception:
                pass
    
    return ""


def fetch_claude_code_plugins_fallback() -> list[dict]:
    """回退方案：使用硬编码的 plugins 列表"""
    skills = []
    
    for skill_name, info in CLAUDE_CODE_PLUGINS.items():
        parsed = {
            "name": f"cc-{skill_name}",
            "description": info["description"],
            "template": "",
            "folder": skill_name,
            "source": "claude-code",
            "repo": "anthropics/claude-code",
            "category": info["category"],
        }
        
        skills.append(parsed)
        print(f"   ✓ {skill_name} [{parsed['category']}]")
    
    return skills


def save_to_database(skills: list[dict]) -> None:
    """保存到数据库 skills 表"""
    client = get_supabase_admin()
    
    for skill in skills:
        try:
            # 检查是否已存在
            existing = (
                client.table("skills")
                .select("id")
                .eq("name", skill["name"])
                .execute()
            )
            
            data = {
                "description": skill["description"],
                "content": skill["template"],
                "category": skill.get("category", "tool"),
                "source": skill.get("source", "official"),
                "repo": skill.get("repo", ""),
            }
            
            if existing.data:
                # 更新
                client.table("skills").update(data).eq("name", skill["name"]).execute()
                print(f"  ✓ 更新: {skill['name']}")
            else:
                # 创建
                data["name"] = skill["name"]
                data["is_active"] = True
                client.table("skills").insert(data).execute()
                print(f"  + 创建: {skill['name']}")
                
        except Exception as e:
            print(f"  ✗ 错误 {skill['name']}: {e}")


def fetch_plugins_official() -> list[dict]:
    """获取 claude-plugins-official 仓库的 plugins"""
    print("\n4. 获取 Claude Plugins Official...")
    
    skills = []
    repo = PLUGINS_OFFICIAL_REPO
    
    # 获取 plugins 目录
    url = f"{GITHUB_API}/repos/{repo}/contents/{PLUGINS_OFFICIAL_PATH}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"   ✗ 无法访问 {repo}/{PLUGINS_OFFICIAL_PATH}: {response.status_code}")
            return skills
        
        items = response.json()
        
        for item in items:
            if item["type"] != "dir":
                continue
            
            folder_name = item["name"]
            
            # 跳过非 plugin 文件夹
            if folder_name.startswith("."):
                continue
            
            # 尝试获取 SKILL.md, README.md 或 agents/*.md
            content = get_plugin_official_content(repo, f"{PLUGINS_OFFICIAL_PATH}/{folder_name}")
            
            # 解析内容获取描述
            parsed = parse_skill_md(content) if content else {}
            description = parsed.get("description") or f"Official Claude plugin: {folder_name}"
            
            # 推断分类
            category = infer_category(folder_name, description, content or "")
            
            skill = {
                "name": f"plugin-{folder_name}",
                "description": description[:500],
                "template": content,
                "folder": folder_name,
                "source": "plugins-official",
                "repo": repo,
                "category": category,
            }
            
            skills.append(skill)
            status = "✓" if content else "○"
            print(f"   {status} {folder_name} [{category}]" + (f" ({len(content)} chars)" if content else ""))
            
    except Exception as e:
        print(f"   ✗ 获取 plugins-official 出错: {e}")
    
    return skills


def get_plugin_official_content(repo: str, path: str) -> str:
    """获取 plugin 的内容，优先 agents/*.md，然后 SKILL.md/README.md"""
    branches = ["main", "master"]
    
    # 先尝试获取 agents 目录下的 md 文件
    for branch in branches:
        agents_url = f"{GITHUB_API}/repos/{repo}/contents/{path}/agents"
        try:
            response = requests.get(agents_url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=10)
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    if item["name"].endswith(".md"):
                        md_url = f"{RAW_GITHUB}/{repo}/{branch}/{path}/agents/{item['name']}"
                        md_response = requests.get(md_url, timeout=10)
                        if md_response.status_code == 200:
                            return md_response.text
        except Exception:
            pass
    
    # 回退到 SKILL.md 或 README.md
    filenames = ["SKILL.md", "skill.md", "README.md"]
    
    for branch in branches:
        for filename in filenames:
            url = f"{RAW_GITHUB}/{repo}/{branch}/{path}/{filename}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return response.text
            except Exception:
                pass
    
    return ""


def main():
    print("=" * 60)
    print("Claude Skills 抓取工具")
    print("=" * 60)
    print()
    
    all_skills = []
    
    # 获取官方 Skills
    official = fetch_official_skills()
    all_skills.extend(official)
    
    # 获取社区 Skills
    community = fetch_community_skills()
    all_skills.extend(community)
    
    # 获取 Claude Code 官方 Plugins
    plugins = fetch_claude_code_plugins()
    all_skills.extend(plugins)
    
    # 获取 Claude Plugins Official
    plugins_official = fetch_plugins_official()
    all_skills.extend(plugins_official)
    
    # 去重
    seen = set()
    unique_skills = []
    for skill in all_skills:
        if skill["name"] not in seen:
            seen.add(skill["name"])
            unique_skills.append(skill)
    
    # 统计
    print("\n" + "=" * 60)
    print("统计")
    print("=" * 60)
    
    categories = {}
    for skill in unique_skills:
        cat = skill.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n总计: {len(unique_skills)} 个 Skills\n")
    print("按分类:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        info = CATEGORY_INFO.get(cat, {"name": cat, "name_en": cat})
        print(f"  {info['name']} ({info['name_en']}): {count}")
    
    # 保存到数据库
    print(f"\n3. 保存到数据库 ({len(unique_skills)} 个)...")
    save_to_database(unique_skills)
    
    print("\n完成!")


if __name__ == "__main__":
    main()
