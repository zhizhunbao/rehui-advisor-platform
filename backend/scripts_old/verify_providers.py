"""Verify provider names are correct"""
from src.modules.llm.service import LLMService

service = LLMService()
models, total = service.find_all_models(1, 1000)

print(f"Total models: {total}")

# Check latest models
latest = [m for m in models if "gpt-5" in m["name"].lower() or "opus-4" in m["name"].lower()]
print(f"\nLatest models ({len(latest)}):")
for m in latest[:15]:
    print(f"  {m['provider']}: {m['name']}")

# Check provider distribution
providers = {}
for m in models:
    p = m["provider"]
    providers[p] = providers.get(p, 0) + 1

print(f"\nTop providers:")
for p, count in sorted(providers.items(), key=lambda x: -x[1])[:15]:
    print(f"  {p}: {count}")
