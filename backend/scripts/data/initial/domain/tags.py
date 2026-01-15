# 标签数据定义 - 通过 domain_code 关联领域
from typing import Any, Dict, List

TAGS: List[Dict[str, Any]] = [
    # immigration - 移民签证
    {
        "code": "work_permit",
        "name": "工签",
        "name_en": "Work Permit",
        "domain_code": "work_permit",
    },
    {
        "code": "lmia",
        "name": "LMIA",
        "name_en": "LMIA",
        "domain_code": "work_permit",
    },
    {
        "code": "employment",
        "name": "工作许可",
        "name_en": "Employment",
        "domain_code": "work_permit",
    },
    {
        "code": "pr",
        "name": "PR",
        "name_en": "PR",
        "domain_code": "pr_application",
    },
    {
        "code": "permanent_resident",
        "name": "永久居民",
        "name_en": "Permanent Resident",
        "domain_code": "pr_application",
    },
    {
        "code": "express_entry",
        "name": "EE快速通道",
        "name_en": "Express Entry",
        "domain_code": "pr_application",
    },
    {
        "code": "pnp",
        "name": "省提名",
        "name_en": "PNP",
        "domain_code": "pr_application",
    },
    {
        "code": "citizenship",
        "name": "入籍",
        "name_en": "Citizenship",
        "domain_code": "citizenship",
    },
    {
        "code": "citizenship_test",
        "name": "入籍考试",
        "name_en": "Citizenship Test",
        "domain_code": "citizenship",
    },
    {
        "code": "visa_renewal",
        "name": "续签",
        "name_en": "Visa Renewal",
        "domain_code": "visa_renewal",
    },
    {
        "code": "visitor_visa",
        "name": "访客签证",
        "name_en": "Visitor Visa",
        "domain_code": "visa_renewal",
    },
    {
        "code": "family_sponsorship",
        "name": "家庭团聚",
        "name_en": "Family Sponsorship",
        "domain_code": "family_sponsorship",
    },
    {
        "code": "spouse_sponsorship",
        "name": "配偶担保",
        "name_en": "Spouse Sponsorship",
        "domain_code": "family_sponsorship",
    },

    # housing - 住房安居
    {
        "code": "rental",
        "name": "租房",
        "name_en": "Rental",
        "domain_code": "rental",
    },
    {
        "code": "apartment",
        "name": "公寓",
        "name_en": "Apartment",
        "domain_code": "rental",
    },
    {
        "code": "lease",
        "name": "租约",
        "name_en": "Lease",
        "domain_code": "rental",
    },
    {
        "code": "home_buying",
        "name": "买房",
        "name_en": "Home Buying",
        "domain_code": "home_buying",
    },
    {
        "code": "mortgage",
        "name": "房贷",
        "name_en": "Mortgage",
        "domain_code": "home_buying",
    },
    {
        "code": "down_payment",
        "name": "首付",
        "name_en": "Down Payment",
        "domain_code": "home_buying",
    },
    {
        "code": "moving",
        "name": "搬家",
        "name_en": "Moving",
        "domain_code": "moving",
    },
    {
        "code": "movers",
        "name": "搬家公司",
        "name_en": "Movers",
        "domain_code": "moving",
    },
    {
        "code": "furniture",
        "name": "家具",
        "name_en": "Furniture",
        "domain_code": "furniture",
    },
    {
        "code": "appliances",
        "name": "家电",
        "name_en": "Appliances",
        "domain_code": "furniture",
    },
    {
        "code": "ikea",
        "name": "IKEA",
        "name_en": "IKEA",
        "domain_code": "furniture",
    },
    {
        "code": "utilities",
        "name": "水电",
        "name_en": "Utilities",
        "domain_code": "utilities",
    },
    {
        "code": "hydro",
        "name": "电费",
        "name_en": "Hydro",
        "domain_code": "utilities",
    },
    {
        "code": "internet",
        "name": "网络",
        "name_en": "Internet",
        "domain_code": "utilities",
    },

    # career - 职业发展
    {
        "code": "job_search",
        "name": "求职",
        "name_en": "Job Search",
        "domain_code": "job_search",
    },
    {
        "code": "linkedin",
        "name": "LinkedIn",
        "name_en": "LinkedIn",
        "domain_code": "job_search",
    },
    {
        "code": "indeed",
        "name": "Indeed",
        "name_en": "Indeed",
        "domain_code": "job_search",
    },
    {
        "code": "resume",
        "name": "简历",
        "name_en": "Resume",
        "domain_code": "resume",
    },
    {
        "code": "cv",
        "name": "CV",
        "name_en": "CV",
        "domain_code": "resume",
    },
    {
        "code": "cover_letter",
        "name": "求职信",
        "name_en": "Cover Letter",
        "domain_code": "resume",
    },
    {
        "code": "interview",
        "name": "面试",
        "name_en": "Interview",
        "domain_code": "interview",
    },
    {
        "code": "behavioral_interview",
        "name": "行为面试",
        "name_en": "Behavioral Interview",
        "domain_code": "interview",
    },
    {
        "code": "technical_interview",
        "name": "技术面试",
        "name_en": "Technical Interview",
        "domain_code": "interview",
    },
    {
        "code": "certification",
        "name": "认证",
        "name_en": "Certification",
        "domain_code": "certification",
    },
    {
        "code": "license",
        "name": "执照",
        "name_en": "License",
        "domain_code": "certification",
    },
    {
        "code": "entrepreneurship",
        "name": "创业",
        "name_en": "Entrepreneurship",
        "domain_code": "entrepreneurship",
    },
    {
        "code": "startup",
        "name": "初创公司",
        "name_en": "Startup",
        "domain_code": "entrepreneurship",
    },
    {
        "code": "business_registration",
        "name": "注册公司",
        "name_en": "Business Registration",
        "domain_code": "entrepreneurship",
    },

    # finance - 金融理财
    {
        "code": "banking",
        "name": "银行",
        "name_en": "Banking",
        "domain_code": "banking",
    },
    {
        "code": "bank_account",
        "name": "开户",
        "name_en": "Bank Account",
        "domain_code": "banking",
    },
    {
        "code": "td_bank",
        "name": "TD银行",
        "name_en": "TD Bank",
        "domain_code": "banking",
    },
    {
        "code": "rbc",
        "name": "RBC",
        "name_en": "RBC",
        "domain_code": "banking",
    },

    {
        "code": "credit_card",
        "name": "信用卡",
        "name_en": "Credit Card",
        "domain_code": "credit_card",
    },
    {
        "code": "credit_score",
        "name": "信用分",
        "name_en": "Credit Score",
        "domain_code": "credit_card",
    },
    {
        "code": "cashback",
        "name": "返现",
        "name_en": "Cashback",
        "domain_code": "credit_card",
    },
    {
        "code": "investment",
        "name": "投资",
        "name_en": "Investment",
        "domain_code": "investment",
    },
    {
        "code": "tfsa",
        "name": "TFSA",
        "name_en": "TFSA",
        "domain_code": "investment",
    },
    {
        "code": "rrsp",
        "name": "RRSP",
        "name_en": "RRSP",
        "domain_code": "investment",
    },
    {
        "code": "etf",
        "name": "ETF",
        "name_en": "ETF",
        "domain_code": "investment",
    },
    {
        "code": "insurance",
        "name": "保险",
        "name_en": "Insurance",
        "domain_code": "insurance",
    },
    {
        "code": "life_insurance",
        "name": "人寿保险",
        "name_en": "Life Insurance",
        "domain_code": "insurance",
    },
    {
        "code": "tax",
        "name": "税务",
        "name_en": "Tax",
        "domain_code": "tax",
    },
    {
        "code": "tax_filing",
        "name": "报税",
        "name_en": "Tax Filing",
        "domain_code": "tax",
    },
    {
        "code": "cra",
        "name": "CRA",
        "name_en": "CRA",
        "domain_code": "tax",
    },
    {
        "code": "remittance",
        "name": "汇款",
        "name_en": "Remittance",
        "domain_code": "remittance",
    },
    {
        "code": "wise",
        "name": "Wise",
        "name_en": "Wise",
        "domain_code": "remittance",
    },
    {
        "code": "forex",
        "name": "外汇",
        "name_en": "Forex",
        "domain_code": "remittance",
    },

    # healthcare - 医疗健康
    {
        "code": "health_insurance",
        "name": "医保",
        "name_en": "Health Insurance",
        "domain_code": "health_insurance",
    },
    {
        "code": "ohip",
        "name": "OHIP",
        "name_en": "OHIP",
        "domain_code": "health_insurance",
    },
    {
        "code": "msp",
        "name": "MSP",
        "name_en": "MSP",
        "domain_code": "health_insurance",
    },
    {
        "code": "family_doctor",
        "name": "家庭医生",
        "name_en": "Family Doctor",
        "domain_code": "family_doctor",
    },
    {
        "code": "clinic",
        "name": "诊所",
        "name_en": "Clinic",
        "domain_code": "family_doctor",
    },
    {
        "code": "walk_in_clinic",
        "name": "Walk-in诊所",
        "name_en": "Walk-in Clinic",
        "domain_code": "clinic_visit",
    },
    {
        "code": "emergency",
        "name": "急诊",
        "name_en": "Emergency",
        "domain_code": "clinic_visit",
    },
    {
        "code": "pharmacy",
        "name": "药房",
        "name_en": "Pharmacy",
        "domain_code": "pharmacy",
    },
    {
        "code": "prescription",
        "name": "处方",
        "name_en": "Prescription",
        "domain_code": "pharmacy",
    },
    {
        "code": "mental_health",
        "name": "心理健康",
        "name_en": "Mental Health",
        "domain_code": "mental_health",
    },
    {
        "code": "counseling",
        "name": "心理咨询",
        "name_en": "Counseling",
        "domain_code": "mental_health",
    },
    {
        "code": "childcare",
        "name": "儿童保健",
        "name_en": "Childcare",
        "domain_code": "childcare",
    },
    {
        "code": "daycare",
        "name": "托儿所",
        "name_en": "Daycare",
        "domain_code": "childcare",
    },
    {
        "code": "vaccination",
        "name": "疫苗",
        "name_en": "Vaccination",
        "domain_code": "childcare",
    },

    # transportation - 交通出行
    {
        "code": "driving_license",
        "name": "驾照",
        "name_en": "Driving License",
        "domain_code": "driving_license",
    },
    {
        "code": "g1_test",
        "name": "G1考试",
        "name_en": "G1 Test",
        "domain_code": "driving_license",
    },
    {
        "code": "g2_test",
        "name": "G2考试",
        "name_en": "G2 Test",
        "domain_code": "driving_license",
    },
    {
        "code": "road_test",
        "name": "路考",
        "name_en": "Road Test",
        "domain_code": "driving_license",
    },
    {
        "code": "car_buying",
        "name": "买车",
        "name_en": "Car Buying",
        "domain_code": "car_buying",
    },
    {
        "code": "used_car",
        "name": "二手车",
        "name_en": "Used Car",
        "domain_code": "car_buying",
    },
    {
        "code": "car_dealer",
        "name": "车行",
        "name_en": "Car Dealer",
        "domain_code": "car_buying",
    },
    {
        "code": "car_insurance",
        "name": "车险",
        "name_en": "Car Insurance",
        "domain_code": "car_insurance",
    },
    {
        "code": "auto_insurance",
        "name": "汽车保险",
        "name_en": "Auto Insurance",
        "domain_code": "car_insurance",
    },
    {
        "code": "public_transit",
        "name": "公共交通",
        "name_en": "Public Transit",
        "domain_code": "public_transit",
    },
    {
        "code": "ttc",
        "name": "TTC",
        "name_en": "TTC",
        "domain_code": "public_transit",
    },
    {
        "code": "presto",
        "name": "Presto",
        "name_en": "Presto",
        "domain_code": "public_transit",
    },
    {
        "code": "flight",
        "name": "机票",
        "name_en": "Flight",
        "domain_code": "flight",
    },
    {
        "code": "airline",
        "name": "航空公司",
        "name_en": "Airline",
        "domain_code": "flight",
    },

    # ai - 人工智能
    {
        "code": "llm",
        "name": "大语言模型",
        "name_en": "LLM",
        "domain_code": "llm_models",
    },
    {
        "code": "gpt",
        "name": "GPT",
        "name_en": "GPT",
        "domain_code": "llm_models",
    },
    {
        "code": "claude",
        "name": "Claude",
        "name_en": "Claude",
        "domain_code": "llm_models",
    },
    {
        "code": "llama",
        "name": "Llama",
        "name_en": "Llama",
        "domain_code": "llm_models",
    },
    {
        "code": "ai_agent",
        "name": "AI Agent",
        "name_en": "AI Agent",
        "domain_code": "agents",
    },
    {
        "code": "autogen",
        "name": "AutoGen",
        "name_en": "AutoGen",
        "domain_code": "agents",
    },
    {
        "code": "crewai",
        "name": "CrewAI",
        "name_en": "CrewAI",
        "domain_code": "agents",
    },
    {
        "code": "langchain",
        "name": "LangChain",
        "name_en": "LangChain",
        "domain_code": "agents",
    },
    {
        "code": "langgraph",
        "name": "LangGraph",
        "name_en": "LangGraph",
        "domain_code": "agents",
    },
    {
        "code": "prompt",
        "name": "提示词",
        "name_en": "Prompt",
        "domain_code": "prompts",
    },
    {
        "code": "prompt_engineering",
        "name": "提示工程",
        "name_en": "Prompt Engineering",
        "domain_code": "prompts",
    },
    {
        "code": "claude_skills",
        "name": "Claude Skills",
        "name_en": "Claude Skills",
        "domain_code": "skills",
    },
    {
        "code": "anthropic",
        "name": "Anthropic",
        "name_en": "Anthropic",
        "domain_code": "skills",
    },
    {
        "code": "rag",
        "name": "RAG",
        "name_en": "RAG",
        "domain_code": "retrieval",
    },
    {
        "code": "vector_db",
        "name": "向量数据库",
        "name_en": "Vector DB",
        "domain_code": "retrieval",
    },
    {
        "code": "embedding",
        "name": "Embedding",
        "name_en": "Embedding",
        "domain_code": "retrieval",
    },
    {
        "code": "llamaindex",
        "name": "LlamaIndex",
        "name_en": "LlamaIndex",
        "domain_code": "retrieval",
    },
]

# AI 补充标签 - 更多搜索关键词
AI_EXTRA_TAGS: List[Dict[str, Any]] = [
    # llm_models - 更多模型和框架
    {"code": "openai", "name": "OpenAI", "name_en": "OpenAI", "domain_code": "llm_models"},
    {"code": "mistral", "name": "Mistral", "name_en": "Mistral", "domain_code": "llm_models"},
    {"code": "gemini", "name": "Gemini", "name_en": "Gemini", "domain_code": "llm_models"},
    {"code": "ollama", "name": "Ollama", "name_en": "Ollama", "domain_code": "llm_models"},
    {"code": "vllm", "name": "vLLM", "name_en": "vLLM", "domain_code": "llm_models"},
    {"code": "huggingface", "name": "HuggingFace", "name_en": "HuggingFace", "domain_code": "llm_models"},
    {"code": "transformers", "name": "Transformers", "name_en": "Transformers", "domain_code": "llm_models"},
    {"code": "chatbot", "name": "聊天机器人", "name_en": "Chatbot", "domain_code": "llm_models"},

    # agents - 更多 Agent 框架
    {"code": "dify", "name": "Dify", "name_en": "Dify", "domain_code": "agents"},
    {"code": "smolagents", "name": "Smolagents", "name_en": "Smolagents", "domain_code": "agents"},
    {"code": "camel", "name": "CAMEL", "name_en": "CAMEL", "domain_code": "agents"},
    {"code": "metagpt", "name": "MetaGPT", "name_en": "MetaGPT", "domain_code": "agents"},
    {"code": "agentgpt", "name": "AgentGPT", "name_en": "AgentGPT", "domain_code": "agents"},
    {"code": "autonomous_agent", "name": "自主Agent", "name_en": "Autonomous Agent", "domain_code": "agents"},
    {"code": "multi_agent", "name": "多智能体", "name_en": "Multi Agent", "domain_code": "agents"},
    {"code": "agentic", "name": "Agentic", "name_en": "Agentic", "domain_code": "agents"},

    # prompts - 更多提示词相关
    {"code": "system_prompt", "name": "系统提示词", "name_en": "System Prompt", "domain_code": "prompts"},
    {"code": "few_shot", "name": "少样本", "name_en": "Few Shot", "domain_code": "prompts"},
    {"code": "chain_of_thought", "name": "思维链", "name_en": "Chain of Thought", "domain_code": "prompts"},
    {"code": "jailbreak", "name": "越狱", "name_en": "Jailbreak", "domain_code": "prompts"},

    # retrieval - 更多检索相关
    {"code": "chroma", "name": "Chroma", "name_en": "Chroma", "domain_code": "retrieval"},
    {"code": "pinecone", "name": "Pinecone", "name_en": "Pinecone", "domain_code": "retrieval"},
    {"code": "qdrant", "name": "Qdrant", "name_en": "Qdrant", "domain_code": "retrieval"},
    {"code": "weaviate", "name": "Weaviate", "name_en": "Weaviate", "domain_code": "retrieval"},
    {"code": "milvus", "name": "Milvus", "name_en": "Milvus", "domain_code": "retrieval"},
    {"code": "pgvector", "name": "pgvector", "name_en": "pgvector", "domain_code": "retrieval"},
    {"code": "semantic_search", "name": "语义搜索", "name_en": "Semantic Search", "domain_code": "retrieval"},

    # interview - 更多面试相关
    {"code": "leetcode", "name": "LeetCode", "name_en": "LeetCode", "domain_code": "interview"},
    {"code": "system_design", "name": "系统设计", "name_en": "System Design", "domain_code": "interview"},
    {"code": "coding_interview", "name": "编程面试", "name_en": "Coding Interview", "domain_code": "interview"},
    {"code": "algorithm", "name": "算法", "name_en": "Algorithm", "domain_code": "interview"},
    {"code": "data_structure", "name": "数据结构", "name_en": "Data Structure", "domain_code": "interview"},
]

TAGS.extend(AI_EXTRA_TAGS)
