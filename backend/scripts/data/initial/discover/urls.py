# 平台 URL 配置 - 每个平台对应一个 discover 脚本
from typing import Dict, List

# 平台 URL 映射 - key 对应 discover 脚本名（不需要 API Key）
PLATFORMS: Dict[str, str] = {
    "github": "https://github.com",
    "hackernews": "https://news.ycombinator.com",
    "reddit": "https://reddit.com",
    "huggingface": "https://huggingface.co",
    "stackoverflow": "https://stackoverflow.com",
    "devto": "https://dev.to",
    "producthunt": "https://producthunt.com",
    "medium": "https://medium.com",
}

# Awesome Lists - 特殊处理，从这些列表提取链接
AWESOME_LISTS: List[str] = [
    "https://github.com/Hannibal046/Awesome-LLM",
    "https://github.com/steven2358/awesome-generative-ai",
    "https://github.com/e2b-dev/awesome-ai-agents",
    "https://github.com/kyrolabs/awesome-langchain",
    "https://github.com/f/awesome-chatgpt-prompts",
    "https://github.com/dair-ai/Prompt-Engineering-Guide",
    "https://github.com/yangshun/tech-interview-handbook",
    "https://github.com/jwasham/coding-interview-university",
]

# RSS 订阅源 - 特殊处理，解析 feed
RSS_FEEDS: List[str] = [
    "https://huggingface.co/blog/feed.xml",
    "https://openai.com/blog/rss.xml",
    "https://www.anthropic.com/feed.xml",
    "https://blog.langchain.dev/rss/",
    "https://www.pinecone.io/blog/rss.xml",
]
