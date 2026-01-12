"""Migrate dev and llm data sources to tech category"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# 获取 tech 分类和领域的 ID
cat = client.table("domain_categories").select("id").eq("code", "tech").single().execute()
tech_cat_id = cat.data["id"]

domains = client.table("domains").select("id, code").eq("category_id", tech_cat_id).execute()
domain_map = {d["code"]: d["id"] for d in domains.data}

print(f"Tech category ID: {tech_cat_id}")
print(f"Domains: {list(domain_map.keys())}")

# 映射旧分类到新领域
mapping = {
    "dev": "dev_tools",
    "llm": "llm",
}

# 更新数据源
for old_cat, new_domain_code in mapping.items():
    domain_id = domain_map.get(new_domain_code)
    if not domain_id:
        print(f"Domain not found: {new_domain_code}")
        continue
    
    # 获取该分类的数据源
    sources = client.table("data_sources").select("id, name").eq("category", old_cat).execute()
    print(f"\nUpdating {len(sources.data)} sources from {old_cat} to {new_domain_code}:")
    
    for s in sources.data:
        client.table("data_sources").update({
            "category_id": tech_cat_id,
            "domain_id": domain_id,
        }).eq("id", s["id"]).execute()
        print(f"  - {s['name']}")

print("\nDone!")
