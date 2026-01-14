"""Create tech category for development resources"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# 获取当前最大 sort_order
response = client.table("domain_categories").select("sort_order").order("sort_order", desc=True).limit(1).execute()
max_order = response.data[0]["sort_order"] if response.data else 0

# 创建技术分类
category = {
    "code": "tech",
    "name": "技术开发",
    "name_en": "Technology & Development",
    "description": "软件开发、AI/ML、DevOps 等技术相关资源",
    "description_en": "Software development, AI/ML, DevOps and other tech resources",
    "icon": "Code",
    "sort_order": max_order + 1,
    "is_active": True,
}

result = client.table("domain_categories").insert(category).execute()
cat_id = result.data[0]["id"]
print(f"Created category: tech (id: {cat_id})")

# 创建子领域
domains = [
    {"code": "dev_tools", "name": "开发工具", "name_en": "Dev Tools", "sort_order": 1},
    {"code": "ai_ml", "name": "AI/机器学习", "name_en": "AI & Machine Learning", "sort_order": 2},
    {"code": "llm", "name": "大语言模型", "name_en": "Large Language Models", "sort_order": 3},
    {"code": "devops", "name": "DevOps", "name_en": "DevOps & Infrastructure", "sort_order": 4},
    {"code": "prompts", "name": "Prompt工程", "name_en": "Prompt Engineering", "sort_order": 5},
]

for d in domains:
    d["category_id"] = cat_id
    d["is_active"] = True
    result = client.table("domains").insert(d).execute()
    print(f"  Created domain: {d['code']}")

print("Done!")
