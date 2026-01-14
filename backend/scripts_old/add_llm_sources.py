"""Add more LLM data sources to data_sources"""
from dotenv import load_dotenv
load_dotenv()

from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

sources = [
    {
        "name": "Free LLM API Resources",
        "url": "https://github.com/cheahjs/free-llm-api-resources",
        "description": "免费 LLM API 资源列表，包含各种免费额度和开源模型",
        "category": "llm-models",
        "type": "github",
        "status": "active",
    },
    {
        "name": "Hugging Face Text Generation",
        "url": "https://huggingface.co/models?pipeline_tag=text-generation",
        "description": "Hugging Face 上的文本生成模型，包含开源模型信息",
        "category": "llm-models",
        "type": "website",
        "status": "active",
    },
    {
        "name": "Artificial Analysis LLM Leaderboard",
        "url": "https://artificialanalysis.ai/models",
        "description": "LLM 性能基准测试和排行榜数据",
        "category": "llm-models",
        "type": "website",
        "status": "active",
    },
    {
        "name": "LMSys Chatbot Arena",
        "url": "https://chat.lmsys.org/",
        "description": "LLM 竞技场排名数据，基于用户投票",
        "category": "llm-models",
        "type": "website",
        "status": "active",
    },
    {
        "name": "Ollama Library",
        "url": "https://ollama.com/library",
        "description": "Ollama 支持的本地部署模型列表",
        "category": "llm-models",
        "type": "website",
        "status": "active",
    },
    {
        "name": "OpenAI Models API",
        "url": "https://api.openai.com/v1/models",
        "description": "OpenAI 官方模型列表 API",
        "category": "llm-models",
        "type": "api",
        "status": "active",
    },
    {
        "name": "Anthropic Models API",
        "url": "https://api.anthropic.com/v1/models",
        "description": "Anthropic 官方模型列表 API",
        "category": "llm-models",
        "type": "api",
        "status": "active",
    },
]

for source in sources:
    # Check if exists
    existing = client.table("data_sources").select("id").eq("url", source["url"]).execute()
    if existing.data and len(existing.data) > 0:
        print(f"Already exists: {source['name']}")
        continue
    
    response = client.table("data_sources").insert(source).execute()
    if response.data:
        print(f"Added: {source['name']}")
    else:
        print(f"Failed to add: {source['name']}")

# List all llm-models sources
print("\n=== All LLM Model Sources ===")
sources = client.table("data_sources").select("name, url, type, status").eq("category", "llm-models").execute()
for s in sources.data:
    print(f"  [{s['type']}] [{s['status']}] {s['name']}: {s['url']}")
