"""List all domain categories"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

response = (
    client.table("domain_categories")
    .select("code, name, name_en, description")
    .order("sort_order")
    .execute()
)

print("Current domain categories:")
print("-" * 80)
for c in response.data:
    print(f"{c['code']:20} {c['name']:12} {c['name_en']}")
