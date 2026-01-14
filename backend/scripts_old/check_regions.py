"""Check region distribution in llm_models"""
from src.modules.llm.service import LLMService

service = LLMService()
models, total = service.find_all_models(1, 3000)

print(f"Total models: {total}")

# Check region distribution
regions = {}
for m in models:
    r = m.get("region") or "null"
    regions[r] = regions.get(r, 0) + 1

print(f"\nRegion distribution:")
for r, count in sorted(regions.items(), key=lambda x: -x[1]):
    print(f"  {r}: {count}")
