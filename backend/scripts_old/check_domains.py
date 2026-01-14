"""Check domains and categories in database"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Check categories
print("=== Domain Categories ===")
cat_response = client.table("domain_categories").select("*").order("sort_order").execute()
print(f"Total categories: {len(cat_response.data)}")
for c in cat_response.data:
    print(f"  - {c['id'][:8]}... : {c['name']} ({c.get('name_en', '')})")

# Check domains by category
print("\n=== Domains by Category ===")
dom_response = client.table("domains").select("code, name, category_id").order("code").execute()
print(f"Total domains: {len(dom_response.data)}")

# Group by category
by_cat: dict[str, list] = {}
for d in dom_response.data:
    cat_id = d.get("category_id") or "uncategorized"
    if cat_id not in by_cat:
        by_cat[cat_id] = []
    by_cat[cat_id].append(d["code"])

for cat_id, domains in by_cat.items():
    cat_name = next((c["name"] for c in cat_response.data if c["id"] == cat_id), "未分类")
    print(f"\n{cat_name} ({len(domains)}):")
    print(f"  {', '.join(domains)}")
