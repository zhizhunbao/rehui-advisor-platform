"""Check latest models from OpenRouter"""
import requests

response = requests.get("https://openrouter.ai/api/v1/models", timeout=30)
data = response.json()
models = data.get("data", [])

print(f"Total models from OpenRouter: {len(models)}")

# Search for GPT-5, Claude Opus 4
print("\n--- Searching for GPT-5, Claude Opus 4 ---")
for m in models:
    name = m.get("id", "").lower()
    if "gpt-5" in name or "opus-4" in name or "opus4" in name:
        print(m.get("id"))

print("\n--- Latest OpenAI models ---")
for m in models:
    if m.get("id", "").startswith("openai/"):
        print(f"  {m.get('id')}")

print("\n--- Latest Anthropic models ---")
for m in models:
    if m.get("id", "").startswith("anthropic/"):
        print(f"  {m.get('id')}")
