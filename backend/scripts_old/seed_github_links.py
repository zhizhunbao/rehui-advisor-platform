#!/usr/bin/env python3
"""
从已知的 GitHub 仓库中导入链接到 github_links 表
"""
import os
import sys
import requests
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common.supabase import get_supabase_admin

GITHUB_API = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com"

# 已知的有价值的 GitHub 仓库
GITHUB_REPOS = [
    # Skills 相关
    {"url": "https://github.com/anthropics/courses", "category": "docs", "name": "Anthropic Courses"},
    {"url": "https://github.com/anthropics/anthropic-cookbook", "category": "docs", "name": "Anthropic Cookbook"},
    {"url": "https://github.com/anthropics/anthropic-quickstarts", "category": "examples", "name": "Anthropic Quickstarts"},
    {"url": "https://github.com/anthropics/prompt-eng-interactive-tutorial", "category": "docs", "name": "Prompt Engineering Tutorial"},
    {"url": "https://github.com/anthropics/skills", "category": "skills", "name": "Anthropic Official Skills"},
    {"url": "https://github.com/anthropics/claude-code", "category": "tools", "name": "Claude Code"},
    {"url": "https://github.com/anthropics/claude-plugins-official", "category": "skills", "name": "Claude Plugins Official"},
    
    # Community Skills
    {"url": "https://github.com/ComposioHQ/awesome-claude-skills", "category": "skills", "name": "Awesome Claude Skills"},
    {"url": "https://github.com/michalparkola/tapestry-skills-for-claude-code", "category": "skills", "name": "Tapestry Skills"},
    
    # Prompts 相关
    {"url": "https://github.com/f/awesome-chatgpt-prompts", "category": "prompts", "name": "Awesome ChatGPT Prompts"},
    {"url": "https://github.com/langgptai/awesome-claude-prompts", "category": "prompts", "name": "Awesome Claude Prompts"},
    {"url": "https://github.com/ai-boost/awesome-prompts", "category": "prompts", "name": "AI Boost Prompts"},
    {"url": "https://github.com/mustvlad/ChatGPT-System-Prompts", "category": "prompts", "name": "ChatGPT System Prompts"},
    
    # MCP 相关
    {"url": "https://github.com/modelcontextprotocol/servers", "category": "tools", "name": "MCP Servers"},
    {"url": "https://github.com/punkpeye/awesome-mcp-servers", "category": "tools", "name": "Awesome MCP Servers"},
    
    # AI 工具和资源
    {"url": "https://github.com/Hannibal046/Awesome-LLM", "category": "docs", "name": "Awesome LLM"},
    {"url": "https://github.com/steven2358/awesome-generative-ai", "category": "docs", "name": "Awesome Generative AI"},
    {"url": "https://github.com/e2b-dev/awesome-ai-agents", "category": "tools", "name": "Awesome AI Agents"},
    {"url": "https://github.com/kyrolabs/awesome-langchain", "category": "tools", "name": "Awesome LangChain"},
    
    # Cursor/IDE 相关
    {"url": "https://github.com/PatrickJS/awesome-cursorrules", "category": "tools", "name": "Awesome Cursor Rules"},
    {"url": "https://github.com/pontusab/cursor.directory", "category": "tools", "name": "Cursor Directory"},
    
    # 开发工具
    {"url": "https://github.com/continuedev/continue", "category": "tools", "name": "Continue Dev"},
    {"url": "https://github.com/Aider-AI/aider", "category": "tools", "name": "Aider"},
]


def fetch_github_metadata(owner: str, repo: str) -> dict:
    """获取 GitHub 仓库元数据"""
    metadata = {}
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # 获取仓库信息
    api_url = f"{GITHUB_API}/repos/{owner}/{repo}"
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            metadata["description"] = data.get("description")
            metadata["stars"] = data.get("stargazers_count")
            metadata["forks"] = data.get("forks_count")
            metadata["open_issues"] = data.get("open_issues_count")
            metadata["language"] = data.get("language")
            metadata["topics"] = data.get("topics", [])
            metadata["last_updated_at"] = data.get("updated_at")
            
            if data.get("license"):
                metadata["license"] = data["license"].get("spdx_id")
    except Exception as e:
        print(f"  ⚠️  API error: {e}")
    
    # 检查 SKILL.md
    for branch in ["main", "master"]:
        skill_url = f"{RAW_GITHUB}/{owner}/{repo}/{branch}/SKILL.md"
        try:
            resp = requests.get(skill_url, timeout=10)
            if resp.status_code == 200:
                metadata["has_skill_md"] = True
                metadata["content_preview"] = resp.text[:500]
                metadata["branch"] = branch
                break
        except Exception:
            pass
    
    # 检查 README
    for branch in ["main", "master"]:
        readme_url = f"{RAW_GITHUB}/{owner}/{repo}/{branch}/README.md"
        try:
            resp = requests.get(readme_url, timeout=10)
            if resp.status_code == 200:
                metadata["has_readme"] = True
                if not metadata.get("content_preview"):
                    metadata["content_preview"] = resp.text[:500]
                if not metadata.get("branch"):
                    metadata["branch"] = branch
                break
        except Exception:
            pass
    
    return metadata


def main():
    client = get_supabase_admin()
    
    added = 0
    updated = 0
    errors = []
    
    for repo in GITHUB_REPOS:
        url = repo["url"]
        
        # 解析 URL
        parts = url.replace("https://github.com/", "").split("/")
        owner = parts[0] if len(parts) > 0 else None
        repo_name = parts[1] if len(parts) > 1 else None
        
        if not owner or not repo_name:
            print(f"❌ Invalid URL: {url}")
            continue
        
        print(f"📦 Processing: {owner}/{repo_name}...")
        
        # 获取 GitHub 元数据
        metadata = fetch_github_metadata(owner, repo_name)
        
        # 检查是否已存在
        existing = client.table("github_links").select("id").eq("url", url).execute()
        
        insert_data = {
            "url": url,
            "name": repo.get("name", repo_name),
            "owner": owner,
            "repo": repo_name,
            "category": repo.get("category"),
            "status": "active",
            "description": metadata.get("description"),
            "stars": metadata.get("stars"),
            "forks": metadata.get("forks"),
            "open_issues": metadata.get("open_issues"),
            "language": metadata.get("language"),
            "topics": metadata.get("topics"),
            "license": metadata.get("license"),
            "has_skill_md": metadata.get("has_skill_md", False),
            "has_readme": metadata.get("has_readme", False),
            "content_preview": metadata.get("content_preview"),
            "branch": metadata.get("branch", "main"),
            "last_checked_at": datetime.now(timezone.utc).isoformat(),
            "last_updated_at": metadata.get("last_updated_at"),
        }
        
        try:
            if existing.data and len(existing.data) > 0:
                # 更新
                client.table("github_links").update(insert_data).eq("id", existing.data[0]["id"]).execute()
                print(f"  ✅ Updated: ⭐{metadata.get('stars', 0)} | {metadata.get('language', '-')}")
                updated += 1
            else:
                # 新增
                client.table("github_links").insert(insert_data).execute()
                print(f"  ✅ Added: ⭐{metadata.get('stars', 0)} | {metadata.get('language', '-')}")
                added += 1
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            errors.append({"url": url, "error": str(e)})
    
    print(f"\n{'='*50}")
    print(f"Added: {added}")
    print(f"Updated: {updated}")
    print(f"Errors: {len(errors)}")


if __name__ == "__main__":
    main()
