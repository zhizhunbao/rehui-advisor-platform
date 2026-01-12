"""
从 GitHub 获取开源 Prompt 库并存入数据库

数据源：
1. f/awesome-chatgpt-prompts (97.5k ⭐) - CSV 格式
2. langgptai/awesome-claude-prompts - Markdown 格式
3. ai-boost/awesome-prompts - GPTs Store Prompts
4. Anthropic 官方 Prompt Library

使用方式：
    cd backend
    uv run python scripts/fetch_prompts.py
"""
import csv
import io
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from common.supabase import get_supabase_admin

# GitHub Raw URL
RAW_GITHUB = "https://raw.githubusercontent.com"

# 分类映射
CATEGORY_MAP = {
    # 角色扮演
    "act as": "roleplay",
    "pretend": "roleplay",
    "simulate": "roleplay",
    "character": "roleplay",
    # 写作
    "write": "writing",
    "essay": "writing",
    "story": "writing",
    "poem": "writing",
    "article": "writing",
    "blog": "writing",
    "content": "writing",
    "copywriter": "writing",
    # 编程
    "code": "coding",
    "programming": "coding",
    "developer": "coding",
    "software": "coding",
    "debug": "coding",
    "python": "coding",
    "javascript": "coding",
    "sql": "coding",
    # 商业
    "business": "business",
    "marketing": "business",
    "sales": "business",
    "startup": "business",
    "entrepreneur": "business",
    "product": "business",
    # 教育
    "teach": "education",
    "learn": "education",
    "tutor": "education",
    "explain": "education",
    "instructor": "education",
    "coach": "education",
    # 创意
    "creative": "creative",
    "brainstorm": "creative",
    "idea": "creative",
    "design": "creative",
    "art": "creative",
    # 分析
    "analyze": "analysis",
    "research": "analysis",
    "data": "analysis",
    "review": "analysis",
    "evaluate": "analysis",
    # 翻译
    "translate": "translation",
    "language": "translation",
    "interpreter": "translation",
    # 助手
    "assistant": "assistant",
    "helper": "assistant",
    "advisor": "assistant",
    "consultant": "assistant",
}


def categorize_prompt(title: str, content: str) -> str:
    """根据标题和内容自动分类"""
    text = (title + " " + content).lower()
    
    for keyword, category in CATEGORY_MAP.items():
        if keyword in text:
            return category
    
    return "general"


def fetch_awesome_chatgpt_prompts() -> list[dict]:
    """获取 f/awesome-chatgpt-prompts (CSV 格式)"""
    print("1. 获取 f/awesome-chatgpt-prompts...")
    
    url = f"{RAW_GITHUB}/f/awesome-chatgpt-prompts/main/prompts.csv"
    response = requests.get(url, timeout=30)
    
    if response.status_code != 200:
        print(f"   ✗ 无法访问: {response.status_code}")
        return []
    
    prompts = []
    reader = csv.DictReader(io.StringIO(response.text))
    
    for row in reader:
        title = row.get("act", "").strip()
        content = row.get("prompt", "").strip()
        
        if not title or not content:
            continue
        
        prompts.append({
            "name": title,
            "description": f"Act as {title}",
            "content": content,
            "category": categorize_prompt(title, content),
            "source": "awesome-chatgpt-prompts",
            "repo": "f/awesome-chatgpt-prompts",
        })
        print(f"   ✓ {title}")
    
    print(f"   共 {len(prompts)} 个 prompts")
    return prompts


def fetch_awesome_claude_prompts() -> list[dict]:
    """获取 langgptai/awesome-claude-prompts (Markdown 格式)"""
    print("\n2. 获取 langgptai/awesome-claude-prompts...")
    
    url = f"{RAW_GITHUB}/langgptai/awesome-claude-prompts/main/README.md"
    response = requests.get(url, timeout=30)
    
    if response.status_code != 200:
        print(f"   ✗ 无法访问: {response.status_code}")
        return []
    
    prompts = []
    content = response.text
    
    # 解析 Markdown 格式: ## Title\n> prompt content
    pattern = r'##\s+(.+?)\n+(?:>\s*(.+?)(?:\n|$))+'
    
    # 更简单的解析：找 ## 标题后的引用块
    sections = re.split(r'\n##\s+', content)
    
    for section in sections[1:]:  # 跳过第一个（标题前的内容）
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        title = lines[0].strip()
        
        # 跳过目录等非 prompt 部分
        if title.lower() in ['table of contents', 'contributing', 'license', 'contributors']:
            continue
        
        # 提取引用块内容
        prompt_lines = []
        for line in lines[1:]:
            if line.startswith('>'):
                prompt_lines.append(line[1:].strip())
            elif prompt_lines and not line.strip():
                break
        
        prompt_content = '\n'.join(prompt_lines).strip()
        
        if not prompt_content or len(prompt_content) < 20:
            continue
        
        prompts.append({
            "name": title,
            "description": f"Claude prompt: {title}",
            "content": prompt_content,
            "category": categorize_prompt(title, prompt_content),
            "source": "awesome-claude-prompts",
            "repo": "langgptai/awesome-claude-prompts",
        })
        print(f"   ✓ {title}")
    
    print(f"   共 {len(prompts)} 个 prompts")
    return prompts


def fetch_ai_boost_prompts() -> list[dict]:
    """获取 ai-boost/awesome-prompts (GPTs Store Prompts)"""
    print("\n3. 获取 ai-boost/awesome-prompts...")
    
    # 获取 prompts 目录列表
    api_url = "https://api.github.com/repos/ai-boost/awesome-prompts/contents/prompts"
    response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=30)
    
    if response.status_code != 200:
        print(f"   ✗ 无法访问: {response.status_code}")
        return []
    
    prompts = []
    files = response.json()
    
    for file in files[:50]:  # 限制数量避免太多请求
        if not file["name"].endswith(".md"):
            continue
        
        # 获取文件内容
        file_url = file["download_url"]
        file_response = requests.get(file_url, timeout=10)
        
        if file_response.status_code != 200:
            continue
        
        content = file_response.text
        title = file["name"].replace(".md", "").replace("-", " ").title()
        
        # 提取 prompt 内容（通常在代码块中）
        code_match = re.search(r'```(?:markdown|text)?\n(.*?)```', content, re.DOTALL)
        if code_match:
            prompt_content = code_match.group(1).strip()
        else:
            # 尝试提取主要内容
            prompt_content = content.strip()
        
        if len(prompt_content) < 50:
            continue
        
        prompts.append({
            "name": title,
            "description": f"GPTs Store: {title}",
            "content": prompt_content[:5000],  # 限制长度
            "category": categorize_prompt(title, prompt_content),
            "source": "ai-boost-prompts",
            "repo": "ai-boost/awesome-prompts",
        })
        print(f"   ✓ {title}")
    
    print(f"   共 {len(prompts)} 个 prompts")
    return prompts


def fetch_anthropic_prompts() -> list[dict]:
    """Anthropic 官方 Prompt Library (手动整理的精选)"""
    print("\n4. 添加 Anthropic 官方 Prompt Library...")
    
    # 这些是从 Anthropic 官方文档整理的精选 prompts
    official_prompts = [
        {
            "name": "Code Reviewer",
            "description": "Review code for bugs, security issues, and improvements",
            "content": """You are an expert code reviewer. Analyze the provided code and:
1. Identify potential bugs or errors
2. Point out security vulnerabilities
3. Suggest performance improvements
4. Check for code style and best practices
5. Provide specific, actionable feedback

Be constructive and explain the reasoning behind each suggestion.""",
            "category": "coding",
        },
        {
            "name": "Technical Writer",
            "description": "Create clear technical documentation",
            "content": """You are a technical writer specializing in creating clear, comprehensive documentation. When writing:
1. Use simple, precise language
2. Structure content logically with headers and sections
3. Include code examples where appropriate
4. Anticipate reader questions
5. Define technical terms on first use

Focus on clarity and completeness while keeping the content accessible.""",
            "category": "writing",
        },
        {
            "name": "Data Analyst",
            "description": "Analyze data and provide insights",
            "content": """You are a data analyst. When analyzing data:
1. First understand the context and goals
2. Identify patterns, trends, and anomalies
3. Calculate relevant statistics
4. Create clear visualizations descriptions
5. Provide actionable insights and recommendations

Always explain your methodology and note any limitations in the data.""",
            "category": "analysis",
        },
        {
            "name": "Product Manager",
            "description": "Help with product strategy and planning",
            "content": """You are an experienced product manager. Help with:
1. Defining product requirements and user stories
2. Prioritizing features using frameworks like RICE or MoSCoW
3. Creating product roadmaps
4. Analyzing market and competition
5. Writing PRDs and specifications

Focus on user value and business impact in all recommendations.""",
            "category": "business",
        },
        {
            "name": "Language Tutor",
            "description": "Teach languages with patience and clarity",
            "content": """You are a patient, encouraging language tutor. When teaching:
1. Adapt to the student's level
2. Explain grammar rules clearly with examples
3. Correct mistakes gently and constructively
4. Provide cultural context when relevant
5. Use spaced repetition for vocabulary

Make learning engaging and celebrate progress.""",
            "category": "education",
        },
        {
            "name": "Creative Brainstormer",
            "description": "Generate creative ideas and solutions",
            "content": """You are a creative brainstorming partner. When generating ideas:
1. Start with quantity over quality
2. Build on and combine ideas
3. Challenge assumptions
4. Explore unconventional approaches
5. Organize ideas by feasibility and impact

Encourage wild ideas while also providing practical options.""",
            "category": "creative",
        },
        {
            "name": "SQL Expert",
            "description": "Write and optimize SQL queries",
            "content": """You are a SQL expert. When helping with databases:
1. Write efficient, readable queries
2. Explain query logic step by step
3. Suggest indexes for optimization
4. Handle edge cases and NULL values
5. Follow SQL best practices

Always consider performance implications and data integrity.""",
            "category": "coding",
        },
        {
            "name": "Email Composer",
            "description": "Write professional emails",
            "content": """You are an expert at writing professional emails. When composing:
1. Match the tone to the context (formal/casual)
2. Be clear and concise
3. Structure with a clear purpose upfront
4. Include specific calls to action
5. Proofread for grammar and clarity

Adapt style based on the recipient and relationship.""",
            "category": "writing",
        },
        {
            "name": "Debate Partner",
            "description": "Explore topics from multiple perspectives",
            "content": """You are a thoughtful debate partner. When discussing topics:
1. Present multiple perspectives fairly
2. Use evidence and logical reasoning
3. Acknowledge valid points from all sides
4. Identify assumptions and biases
5. Synthesize insights from the discussion

Aim for understanding rather than winning.""",
            "category": "analysis",
        },
        {
            "name": "API Designer",
            "description": "Design RESTful APIs following best practices",
            "content": """You are an API design expert. When designing APIs:
1. Follow RESTful conventions
2. Use clear, consistent naming
3. Design for extensibility
4. Include proper error handling
5. Document with OpenAPI/Swagger

Consider versioning, pagination, and rate limiting from the start.""",
            "category": "coding",
        },
    ]
    
    prompts = []
    for p in official_prompts:
        prompts.append({
            **p,
            "source": "anthropic-official",
            "repo": "",
        })
        print(f"   ✓ {p['name']}")
    
    print(f"   共 {len(prompts)} 个 prompts")
    return prompts


def fetch_system_prompts() -> list[dict]:
    """获取 dontriskit/awesome-ai-system-prompts"""
    print("\n5. 获取 dontriskit/awesome-ai-system-prompts...")
    
    # 获取根目录
    api_url = "https://api.github.com/repos/dontriskit/awesome-ai-system-prompts/contents"
    response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=30)
    
    if response.status_code != 200:
        print(f"   ✗ 无法访问: {response.status_code}")
        return []
    
    prompts = []
    items = response.json()
    
    # 跳过的文件夹
    skip_folders = ["LICENSE", "README.md", "readme_old.md"]
    
    for item in items:
        if item["type"] != "dir" or item["name"] in skip_folders:
            continue
        
        folder_name = item["name"]
        
        # 获取文件夹内的 md 文件
        folder_url = f"https://api.github.com/repos/dontriskit/awesome-ai-system-prompts/contents/{folder_name}"
        folder_response = requests.get(folder_url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=10)
        
        if folder_response.status_code != 200:
            continue
        
        files = folder_response.json()
        
        for file in files:
            if not file["name"].endswith(".md"):
                continue
            
            # 获取文件内容
            file_response = requests.get(file["download_url"], timeout=10)
            if file_response.status_code != 200:
                continue
            
            content = file_response.text
            title = file["name"].replace(".md", "").replace("-", " ").replace("_", " ").title()
            
            # 清理内容 - 移除 frontmatter
            content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            content = content.strip()
            
            if len(content) < 100:
                continue
            
            prompts.append({
                "name": f"{folder_name} - {title}",
                "description": f"System prompt for {folder_name}: {title}",
                "content": content[:8000],  # 限制长度
                "category": "system",
                "source": "awesome-system-prompts",
                "repo": "dontriskit/awesome-ai-system-prompts",
            })
            print(f"   ✓ {folder_name}/{title}")
    
    print(f"   共 {len(prompts)} 个 prompts")
    return prompts


def save_to_database(prompts: list[dict]) -> None:
    """保存到数据库 prompt_templates 表"""
    client = get_supabase_admin()
    
    saved = 0
    updated = 0
    errors = 0
    
    for prompt in prompts:
        try:
            # 检查是否已存在（按名称和来源）
            existing = (
                client.table("prompt_templates")
                .select("id")
                .eq("name", prompt["name"])
                .eq("source", prompt.get("source", ""))
                .execute()
            )
            
            data = {
                "name": prompt["name"],
                "description": prompt.get("description", ""),
                "template": prompt["content"],
                "category": prompt.get("category", "general"),
                "source": prompt.get("source", ""),
                "repo": prompt.get("repo", ""),
                "is_active": True,
            }
            
            if existing.data:
                # 更新
                client.table("prompt_templates").update({
                    "description": data["description"],
                    "template": data["template"],
                    "category": data["category"],
                }).eq("id", existing.data[0]["id"]).execute()
                updated += 1
            else:
                # 创建
                client.table("prompt_templates").insert(data).execute()
                saved += 1
                
        except Exception as e:
            print(f"  ✗ 错误 {prompt['name']}: {e}")
            errors += 1
    
    print(f"\n保存结果: 新增 {saved}, 更新 {updated}, 错误 {errors}")


def main():
    print("=" * 60)
    print("Prompt 库抓取工具")
    print("=" * 60)
    print()
    
    all_prompts = []
    
    # 1. f/awesome-chatgpt-prompts
    prompts1 = fetch_awesome_chatgpt_prompts()
    all_prompts.extend(prompts1)
    
    # 2. langgptai/awesome-claude-prompts
    prompts2 = fetch_awesome_claude_prompts()
    all_prompts.extend(prompts2)
    
    # 3. ai-boost/awesome-prompts
    prompts3 = fetch_ai_boost_prompts()
    all_prompts.extend(prompts3)
    
    # 4. Anthropic 官方
    prompts4 = fetch_anthropic_prompts()
    all_prompts.extend(prompts4)
    
    # 5. System Prompts
    prompts5 = fetch_system_prompts()
    all_prompts.extend(prompts5)
    
    # 去重（按名称）
    seen = set()
    unique_prompts = []
    for p in all_prompts:
        key = p["name"].lower()
        if key not in seen:
            seen.add(key)
            unique_prompts.append(p)
    
    # 统计
    print("\n" + "=" * 60)
    print("统计")
    print("=" * 60)
    
    categories = {}
    sources = {}
    for p in unique_prompts:
        cat = p.get("category", "general")
        src = p.get("source", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
        sources[src] = sources.get(src, 0) + 1
    
    print(f"\n总计: {len(unique_prompts)} 个 Prompts (去重后)\n")
    
    print("按分类:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    print("\n按来源:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src}: {count}")
    
    # 保存到数据库
    print(f"\n保存到数据库...")
    save_to_database(unique_prompts)
    
    print("\n完成!")


if __name__ == "__main__":
    main()
