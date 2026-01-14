"""Check tech domains"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# 获取 tech 分类下的所有 domains
cat = client.table("domain_categories").select("id").eq("code", "tech").single().execute()
domains = client.table("domains").select("code, name, name_en, description, icon").eq("category_id", cat.data["id"]).execute()

print("Tech 分类下的领域:")
for d in domains.data:
    print(f"  {d['icon']} {d['code']:12} {d['name']:12} {d['name_en']}")
    print(f"     {d['description']}")
