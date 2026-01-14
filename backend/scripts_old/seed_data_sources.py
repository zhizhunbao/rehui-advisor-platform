"""数据源种子数据 - 北美生活各领域 GitHub 资源"""
from src.common.supabase import get_supabase_admin

DATA_SOURCES = [
    # ==================== AI 工具 (ai_tools) ====================
    # --- Claude 相关 ---
    {
        "url": "https://github.com/anthropics/claude-plugins-official",
        "name": "Claude Plugins Official",
        "description": "Anthropic 官方维护的高质量 Claude Code 插件目录",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "claude",
        "tags": ["claude", "plugins", "anthropic", "ai"],
    },
    # --- Agent 框架 (agent_framework) ---
    {
        "url": "https://github.com/jd-opensource/joyagent-jdgenie",
        "name": "JoyAgent-JDGenie",
        "description": "京东开源的端到端多智能体产品，支持报告生成、代码、PPT等多种Agent，GAIA榜单表现优异",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "multi-agent", "jd", "gaia", "report", "ppt"],
    },
    {
        "url": "https://github.com/microsoft/autogen",
        "name": "AutoGen",
        "description": "微软开源的多智能体对话框架，支持多Agent协作完成复杂任务",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "multi-agent", "microsoft", "conversation"],
    },
    {
        "url": "https://github.com/crewAIInc/crewAI",
        "name": "CrewAI",
        "description": "角色扮演式多智能体协作框架，让AI Agent像团队一样协作",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "multi-agent", "crew", "role-playing"],
    },
    {
        "url": "https://github.com/langchain-ai/langgraph",
        "name": "LangGraph",
        "description": "LangChain 团队的有状态多Agent编排框架，支持循环和条件逻辑",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "langchain", "graph", "workflow"],
    },
    {
        "url": "https://github.com/camel-ai/camel",
        "name": "CAMEL (OWL)",
        "description": "首个LLM多智能体框架，支持角色扮演和任务协作",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "multi-agent", "camel", "owl", "role-playing"],
    },
    {
        "url": "https://github.com/langgenius/dify",
        "name": "Dify",
        "description": "开源LLM应用开发平台，支持Agent和Workflow可视化编排",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "workflow", "llm-platform", "low-code"],
    },
    {
        "url": "https://github.com/huggingface/smolagents",
        "name": "Smolagents",
        "description": "Hugging Face 的轻量级Agent框架，简洁易用",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "huggingface", "lightweight"],
    },
    {
        "url": "https://github.com/mannaandpoem/OpenManus",
        "name": "OpenManus",
        "description": "开源通用Agent框架，xManus的开源实现",
        "type": "github",
        "category": "ai_tools",
        "subcategory": "agent_framework",
        "tags": ["agent", "manus", "general-purpose"],
    },
    # ==================== 求职就业 (job) ====================
    {
        "url": "https://github.com/Lamiiine/Awesome-daily-list-of-visa-sponsored-jobs",
        "name": "Awesome Visa Sponsored Jobs",
        "description": "每日更新的签证担保工作机会列表",
        "type": "github",
        "category": "job",
        "subcategory": "visa_sponsorship",
        "tags": ["visa", "job", "sponsorship", "H1B"],
    },
    {
        "url": "https://github.com/poteto/hiring-without-whiteboards",
        "name": "Hiring Without Whiteboards",
        "description": "不使用白板面试的公司列表，更人性化的面试流程",
        "type": "github",
        "category": "job",
        "subcategory": "interview",
        "tags": ["interview", "hiring", "job"],
    },
    {
        "url": "https://github.com/jwasham/coding-interview-university",
        "name": "Coding Interview University",
        "description": "完整的计算机科学学习计划，帮助准备大厂面试",
        "type": "github",
        "category": "job",
        "subcategory": "interview",
        "tags": ["interview", "coding", "study", "FAANG"],
    },
    {
        "url": "https://github.com/yangshun/tech-interview-handbook",
        "name": "Tech Interview Handbook",
        "description": "技术面试手册，包含算法、系统设计、行为面试等",
        "type": "github",
        "category": "job",
        "subcategory": "interview",
        "tags": ["interview", "algorithm", "system-design"],
    },
    {
        "url": "https://github.com/donnemartin/system-design-primer",
        "name": "System Design Primer",
        "description": "系统设计面试准备资源，大规模系统设计学习",
        "type": "github",
        "category": "job",
        "subcategory": "interview",
        "tags": ["system-design", "interview", "architecture"],
    },
    {
        "url": "https://github.com/kdn251/interviews",
        "name": "Interviews",
        "description": "软件工程技术面试必备知识",
        "type": "github",
        "category": "job",
        "subcategory": "interview",
        "tags": ["interview", "algorithm", "data-structure"],
    },
    {
        "url": "https://github.com/emredurukn/awesome-job-boards",
        "name": "Awesome Job Boards",
        "description": "精选求职网站列表，覆盖各行业和地区",
        "type": "github",
        "category": "job",
        "subcategory": "job_board",
        "tags": ["job", "career", "job-board"],
    },
    {
        "url": "https://github.com/remoteintech/remote-jobs",
        "name": "Remote Jobs",
        "description": "提供远程工作的科技公司列表",
        "type": "github",
        "category": "job",
        "subcategory": "remote",
        "tags": ["remote", "job", "work-from-home"],
    },
    {
        "url": "https://github.com/Awesome-Interview/Awesome-Interview",
        "name": "Awesome Interview",
        "description": "面试资源汇总，包含各类技术栈面试题",
        "type": "github",
        "category": "job",
        "subcategory": "interview",
        "tags": ["interview", "frontend", "backend"],
    },
    {
        "url": "https://github.com/imkgarg/Awesome-Software-Engineering-Interview",
        "name": "Awesome Software Engineering Interview",
        "description": "软件工程面试资源大全",
        "type": "github",
        "category": "job",
        "subcategory": "interview",
        "tags": ["interview", "software-engineering"],
    },
    # ==================== 教育培训 (education) ====================
    {
        "url": "https://github.com/ossu/computer-science",
        "name": "OSSU Computer Science",
        "description": "开源社会大学计算机科学自学课程",
        "type": "github",
        "category": "education",
        "subcategory": "cs",
        "tags": ["education", "computer-science", "self-study"],
    },
    {
        "url": "https://github.com/prakhar1989/awesome-courses",
        "name": "Awesome Courses",
        "description": "精选在线课程列表，涵盖CS各领域",
        "type": "github",
        "category": "education",
        "subcategory": "online_course",
        "tags": ["education", "course", "MOOC"],
    },
    {
        "url": "https://github.com/EbookFoundation/free-programming-books",
        "name": "Free Programming Books",
        "description": "免费编程书籍资源，多语言支持",
        "type": "github",
        "category": "education",
        "subcategory": "books",
        "tags": ["education", "books", "programming", "free"],
    },
    {
        "url": "https://github.com/freeCodeCamp/freeCodeCamp",
        "name": "freeCodeCamp",
        "description": "免费学习编程的开源社区",
        "type": "github",
        "category": "education",
        "subcategory": "coding",
        "tags": ["education", "coding", "web-development"],
    },
    {
        "url": "https://github.com/kamranahmedse/developer-roadmap",
        "name": "Developer Roadmap",
        "description": "开发者学习路线图，前端/后端/DevOps等",
        "type": "github",
        "category": "education",
        "subcategory": "roadmap",
        "tags": ["education", "roadmap", "career"],
    },
    {
        "url": "https://github.com/sindresorhus/awesome",
        "name": "Awesome Lists",
        "description": "Awesome 列表的列表，各领域精选资源汇总",
        "type": "github",
        "category": "education",
        "subcategory": "resources",
        "tags": ["awesome", "resources", "curated"],
    },
    {
        "url": "https://github.com/AwesomePresentations/awesome-moocs",
        "name": "Awesome MOOCs",
        "description": "MOOC 在线课程资源列表",
        "type": "github",
        "category": "education",
        "subcategory": "online_course",
        "tags": ["education", "MOOC", "online-learning"],
    },
    # ==================== 投资理财 (investment) ====================
    {
        "url": "https://github.com/wangzhe3224/awesome-systematic-trading",
        "name": "Awesome Systematic Trading",
        "description": "系统化交易资源，涵盖股票、加密货币、期货等",
        "type": "github",
        "category": "investment",
        "subcategory": "trading",
        "tags": ["trading", "stock", "crypto", "finance"],
    },
    {
        "url": "https://github.com/mr-karan/awesome-investing",
        "name": "Awesome Investing",
        "description": "投资与金融相关资源精选",
        "type": "github",
        "category": "investment",
        "subcategory": "general",
        "tags": ["investing", "finance", "stock"],
    },
    {
        "url": "https://github.com/finwiki/awesome-personal-finance",
        "name": "Awesome Personal Finance",
        "description": "个人理财在线资源精选",
        "type": "github",
        "category": "investment",
        "subcategory": "personal_finance",
        "tags": ["personal-finance", "budgeting", "saving"],
    },
    {
        "url": "https://github.com/ashishb/personal-finance-awesome",
        "name": "Personal Finance Awesome",
        "description": "个人理财相关网站和工具列表",
        "type": "github",
        "category": "investment",
        "subcategory": "personal_finance",
        "tags": ["personal-finance", "tools", "robo-advisor"],
    },
    {
        "url": "https://github.com/SpiralDevelopment/Awesome-Crypto-Trading",
        "name": "Awesome Crypto Trading",
        "description": "加密货币交易资源、软件和工具",
        "type": "github",
        "category": "investment",
        "subcategory": "crypto",
        "tags": ["crypto", "trading", "bitcoin"],
    },
    {
        "url": "https://github.com/chromale/awesome-investing-tools",
        "name": "Awesome Investing Tools",
        "description": "投资工具和应用列表",
        "type": "github",
        "category": "investment",
        "subcategory": "tools",
        "tags": ["investing", "tools", "apps"],
    },
    # ==================== 保险规划 (insurance) ====================
    {
        "url": "https://github.com/kakoni/awesome-healthcare",
        "name": "Awesome Healthcare",
        "description": "开源医疗健康软件、库和资源",
        "type": "github",
        "category": "insurance",
        "subcategory": "health",
        "tags": ["healthcare", "health", "medical"],
    },
    {
        "url": "https://github.com/medtorch/awesome-healthcare-ai",
        "name": "Awesome Healthcare AI",
        "description": "医疗健康 AI 工具、算法和数据集",
        "type": "github",
        "category": "insurance",
        "subcategory": "health",
        "tags": ["healthcare", "AI", "medical"],
    },
    # ==================== 房产租房 (house) ====================
    {
        "url": "https://github.com/etewiah/awesome-real-estate",
        "name": "Awesome Real Estate",
        "description": "房地产相关资源和项目精选",
        "type": "github",
        "category": "house",
        "subcategory": "general",
        "tags": ["real-estate", "housing", "property"],
    },
    {
        "url": "https://github.com/ual/rental-listings",
        "name": "Rental Listings Analysis",
        "description": "租房数据分析和可视化",
        "type": "github",
        "category": "house",
        "subcategory": "rental",
        "tags": ["rental", "data-analysis", "housing"],
    },
    # ==================== 租车服务 (car_rental) ====================
    {
        "url": "https://github.com/Marcin214/awesome-automotive",
        "name": "Awesome Automotive",
        "description": "汽车工程资源精选",
        "type": "github",
        "category": "car_rental",
        "subcategory": "automotive",
        "tags": ["automotive", "car", "vehicle"],
    },
    {
        "url": "https://github.com/jaredthecoder/awesome-vehicle-security",
        "name": "Awesome Vehicle Security",
        "description": "汽车安全和黑客技术学习资源",
        "type": "github",
        "category": "car_rental",
        "subcategory": "security",
        "tags": ["vehicle", "security", "car-hacking"],
    },
    {
        "url": "https://github.com/ilyasozkurt/automobile-models-and-specs",
        "name": "Automobile Models and Specs",
        "description": "汽车制造商、型号和规格数据库",
        "type": "github",
        "category": "car_rental",
        "subcategory": "data",
        "tags": ["automobile", "database", "specs"],
    },
    # ==================== 签证移民 (immigration) ====================
    {
        "url": "https://github.com/AwesomeVisa/awesome-immigration",
        "name": "Awesome Immigration",
        "description": "各国移民签证信息汇总",
        "type": "github",
        "category": "immigration",
        "subcategory": "visa",
        "tags": ["immigration", "visa", "green-card"],
    },
    {
        "url": "https://github.com/nickliqian/h1b-salary-database",
        "name": "H1B Salary Database",
        "description": "H1B 签证薪资数据库",
        "type": "github",
        "category": "immigration",
        "subcategory": "h1b",
        "tags": ["H1B", "salary", "visa"],
    },
    # ==================== 机票酒店 (travel) ====================
    {
        "url": "https://github.com/TravelXML/Free-Hotel-Booking-Engine",
        "name": "Free Hotel Booking Engine",
        "description": "开源酒店预订引擎",
        "type": "github",
        "category": "hotel",
        "subcategory": "booking",
        "tags": ["hotel", "booking", "travel"],
    },
    {
        "url": "https://github.com/Nedal-Esrar/Travel-and-Accommodation-Booking-Platform",
        "name": "Travel Booking Platform",
        "description": "旅行住宿预订平台 API",
        "type": "github",
        "category": "hotel",
        "subcategory": "api",
        "tags": ["hotel", "travel", "API"],
    },
]


def seed_data_sources():
    """种子数据源"""
    client = get_supabase_admin()
    
    added = 0
    skipped = 0
    errors = []
    
    for source in DATA_SOURCES:
        url = source["url"]
        
        # 检查是否已存在
        response = (
            client.table("data_sources")
            .select("id")
            .eq("url", url)
            .execute()
        )
        
        if response.data and len(response.data) > 0:
            skipped += 1
            print(f"⏭️  Skipped (exists): {source['name']}")
            continue
        
        try:
            client.table("data_sources").insert({
                "url": url,
                "name": source["name"],
                "description": source["description"],
                "type": source["type"],
                "category": source["category"],
                "subcategory": source.get("subcategory"),
                "tags": source.get("tags", []),
                "status": "active",
            }).execute()
            added += 1
            print(f"✅ Added: {source['name']}")
        except Exception as e:
            errors.append({"name": source["name"], "error": str(e)})
            print(f"❌ Error: {source['name']} - {e}")
    
    print(f"\n📊 Summary: Added {added}, Skipped {skipped}, Errors {len(errors)}")
    return {"added": added, "skipped": skipped, "errors": errors}


if __name__ == "__main__":
    seed_data_sources()
