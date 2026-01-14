#!/usr/bin/env python3
"""添加 LLM 模型同步源到 github_links 表"""
import os
import sys
from pathlib import Path

# 加载 .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

# 添加 src 到 path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.common.supabase import get_supabase_admin

# LLM 模型数据源
SOURCES = [
    {
        "name": "OpenRouter Models",
        "url": "https://openrouter.ai/models",
        "description": "OpenRouter 提供的 LLM 模型列表，包含价格和能力信息",
        "category": "llm-models",
        "status": "active",
    },
    {
        "name": "LiteLLM Model Prices",
        "url": "https://github.com/BerriAI/litellm",
        "description": "LiteLLM 维护的模型价格和上下文窗口信息",
        "category": "llm-models",
        "status": "active",
    },
]


def main():
    client = get_supabase_admin()
    
    added = 0
    skipped = 0
    
    for source in SOURCES:
        # 检查是否已存在
        existing = (
            client.table("github_links")
            .select("id")
            .eq("url", source["url"])
            .execute()
        )
        
        if existing.data and len(existing.data) > 0:
            print(f"⏭️  Skipped (exists): {source['name']}")
            skipped += 1
            continue
        
        # 插入
        client.table("github_links").insert(source).execute()
        print(f"✅ Added: {source['name']}")
        added += 1
    
    print(f"\n📊 Summary: {added} added, {skipped} skipped")


if __name__ == "__main__":
    main()
