"""Check prompts table - get sample high-quality structured prompts"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Get longer, more structured prompts
response = client.table("prompt_templates").select("name, description, template, category").execute()

# Find prompts with longer templates (more detailed)
long_prompts = [p for p in response.data if len(p.get("template") or "") > 1000]
print(f"Found {len(long_prompts)} prompts with >1000 chars")

# Show a few good examples
for p in long_prompts[:3]:
    print(f"\n{'='*60}")
    print(f"NAME: {p['name']} ({p['category']})")
    print(f"DESC: {p['description'][:100]}...")
    print(f"\nTEMPLATE ({len(p['template'])} chars):")
    print(p['template'][:2000])
    print(f"\n{'='*60}")
