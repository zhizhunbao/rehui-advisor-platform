"""Fix provider names in llm_models table and re-sync"""
from src.common.supabase import get_supabase_admin
from src.modules.llm.service import LLMService

client = get_supabase_admin()

# Delete all models synced from OpenRouter (they have wrong provider names)
# We'll identify them by api_endpoint containing openrouter
print("Deleting models with incorrect provider names...")
response = client.table("llm_models").delete().eq("api_endpoint", "https://openrouter.ai/api/v1").execute()
print(f"Deleted {len(response.data)} models")

# Re-sync from OpenRouter
print("\nRe-syncing from OpenRouter...")
service = LLMService()
result = service._sync_from_openrouter()
print(f"Synced: {result['synced']}, Errors: {len(result['errors'])}")

# Verify
models, total = service.find_all_models(page=1, limit=10)
print(f"\nSample models after fix:")
for m in models[:5]:
    print(f"  {m['provider']}: {m['name']}")
