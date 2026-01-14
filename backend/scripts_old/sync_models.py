"""Sync models from OpenRouter"""
from src.modules.llm.service import LLMService

s = LLMService()
r = s._sync_from_openrouter()
print(f"Synced: {r['synced']}, Errors: {len(r['errors'])}")

# Check if latest models are in DB
models, total = s.find_all_models(page=1, limit=1000)
latest = ["gpt-5.2", "gpt-5.1", "gpt-5", "claude-opus-4.5", "claude-opus-4"]
print(f"\nTotal models in DB: {total}")
print("\nLatest models found:")
for m in models:
    name = m["name"].lower()
    if any(k in name for k in latest):
        print(f"  {m['name']}")
