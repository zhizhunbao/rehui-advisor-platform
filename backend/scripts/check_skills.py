"""Check skills data"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Get skills count and sample
response = client.table("skills").select("id, name, category, source", count="exact").limit(10).execute()

print(f"Total skills: {response.count}")
print("\nSample skills:")
print("-" * 80)
for s in response.data:
    name = s["name"][:40] if s["name"] else ""
    category = s["category"] or ""
    source = s["source"] or ""
    print(f"  {name:40} | {category:15} | {source}")

# Get category distribution
cat_response = client.table("skills").select("category").execute()
categories = {}
for s in cat_response.data:
    cat = s["category"] or "uncategorized"
    categories[cat] = categories.get(cat, 0) + 1

print("\nCategory distribution:")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")
