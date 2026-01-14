"""添加 Agent 框架子领域并导入数据源"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()


def get_or_create_agent_domain():
    """获取或创建 agent_framework 领域"""
    # 获取 tech 分类 ID
    tech_cat = client.table("domain_categories").select("id").eq("code", "tech").maybe_single().execute()
    if not tech_cat.data:
        print("❌ 未找到 tech 分类，请先运行 create_tech_category.py")
        return None
    
    tech_cat_id = tech_cat.data["id"]
    
    # 检查 agent_framework 是否已存在
    existing = client.table("domains").select("id").eq("code", "agent_framework").execute()
    if existing.data and len(existing.data) > 0:
        print(f"✅ agent_framework 领域已存在: {existing.data[0]['id']}")
        return existing.data[0]["id"], tech_cat_id
    
    # 获取最大 sort_order
    max_order_resp = (
        client.table("domains")
        .select("sort_order")
        .eq("category_id", tech_cat_id)
        .order("sort_order", desc=True)
        .limit(1)
        .execute()
    )
    max_order = max_order_resp.data[0]["sort_order"] if max_order_resp.data else 0
    
    # 创建 agent_framework 领域
    domain = {
        "code": "agent_framework",
        "name": "Agent框架",
        "name_en": "Agent Frameworks",
        "description": "AI Agent 和多智能体框架",
        "description_en": "AI Agent and Multi-Agent Frameworks",
        "category_id": tech_cat_id,
        "sort_order": max_order + 1,
        "is_active": True,
    }
    
    result = client.table("domains").insert(domain).execute()
    domain_id = result.data[0]["id"]
    print(f"✅ 创建 agent_framework 领域: {domain_id}")
    return domain_id, tech_cat_id


AGENT_FRAMEWORKS = [
    {
        "url": "https://github.com/jd-opensource/joyagent-jdgenie",
        "name": "JoyAgent-JDGenie",
        "description": "京东开源的端到端多智能体产品，支持报告生成、代码、PPT等多种Agent，GAIA榜单表现优异",
        "tags": ["agent", "multi-agent", "jd", "gaia", "report", "ppt"],
    },
    {
        "url": "https://github.com/microsoft/autogen",
        "name": "AutoGen",
        "description": "微软开源的多智能体对话框架，支持多Agent协作完成复杂任务",
        "tags": ["agent", "multi-agent", "microsoft", "conversation"],
    },
    {
        "url": "https://github.com/crewAIInc/crewAI",
        "name": "CrewAI",
        "description": "角色扮演式多智能体协作框架，让AI Agent像团队一样协作",
        "tags": ["agent", "multi-agent", "crew", "role-playing"],
    },
    {
        "url": "https://github.com/langchain-ai/langgraph",
        "name": "LangGraph",
        "description": "LangChain 团队的有状态多Agent编排框架，支持循环和条件逻辑",
        "tags": ["agent", "langchain", "graph", "workflow"],
    },
    {
        "url": "https://github.com/camel-ai/camel",
        "name": "CAMEL (OWL)",
        "description": "首个LLM多智能体框架，支持角色扮演和任务协作",
        "tags": ["agent", "multi-agent", "camel", "owl", "role-playing"],
    },
    {
        "url": "https://github.com/langgenius/dify",
        "name": "Dify",
        "description": "开源LLM应用开发平台，支持Agent和Workflow可视化编排",
        "tags": ["agent", "workflow", "llm-platform", "low-code"],
    },
    {
        "url": "https://github.com/huggingface/smolagents",
        "name": "Smolagents",
        "description": "Hugging Face 的轻量级Agent框架，简洁易用",
        "tags": ["agent", "huggingface", "lightweight"],
    },
    {
        "url": "https://github.com/mannaandpoem/OpenManus",
        "name": "OpenManus",
        "description": "开源通用Agent框架，xManus的开源实现",
        "tags": ["agent", "manus", "general-purpose"],
    },
]


def seed_agent_frameworks():
    """导入 Agent 框架数据源"""
    result = get_or_create_agent_domain()
    if not result:
        return
    
    domain_id, category_id = result
    
    added = 0
    skipped = 0
    
    for source in AGENT_FRAMEWORKS:
        # 检查是否已存在
        existing = (
            client.table("data_sources")
            .select("id")
            .eq("url", source["url"])
            .execute()
        )
        
        if existing.data and len(existing.data) > 0:
            print(f"⏭️  已存在: {source['name']}")
            skipped += 1
            continue
        
        # 插入数据
        data = {
            "url": source["url"],
            "name": source["name"],
            "description": source["description"],
            "type": "github",
            "category_id": category_id,
            "domain_id": domain_id,
            "tags": source.get("tags", []),
            "status": "active",
        }
        
        client.table("data_sources").insert(data).execute()
        print(f"✅ 添加: {source['name']}")
        added += 1
    
    print(f"\n📊 完成: 添加 {added}, 跳过 {skipped}")


if __name__ == "__main__":
    seed_agent_frameworks()
