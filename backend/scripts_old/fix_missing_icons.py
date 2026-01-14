"""Fix missing icons for domains"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# 检查哪些 domains 缺少 icon
response = client.table("domains").select("code, name, icon").execute()
missing = [d for d in response.data if not d.get("icon")]
print(f"缺少 icon 的 domains ({len(missing)}):")
for d in missing:
    print(f"  {d['code']}: {d['name']}")

# Icon 映射
ICONS = {
    # tech 分类
    "dev_tools": "🛠️",
    "ai_ml": "🤖",
    "llm": "🧠",
    "devops": "☁️",
    "prompts": "💬",
    # government 分类
    "benefits": "🏛️",
    "employment_insurance": "💼",
    "pension": "👴",
    "child_benefits": "👶",
    "housing_subsidy": "🏠",
    "healthcare_benefits": "🏥",
    "newcomer_services": "🌟",
    "disability_benefits": "♿",
    "social_assistance": "🤝",
}

print("\n更新 icons:")
for code, icon in ICONS.items():
    result = client.table("domains").update({"icon": icon}).eq("code", code).execute()
    if result.data:
        print(f"  {icon} {code}")

print("\nDone!")
