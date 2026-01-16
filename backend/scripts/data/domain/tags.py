# 标签数据定义 - 分离搜索关键词和匹配标签
from typing import Any, Dict, List

# ============================================================
# 领域搜索关键词 - 用于 GitHub/HackerNews 搜索（每个领域 2-5 个）
# ============================================================
DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    # AI 相关
    "llm_providers": [],  # 从 MATCH_TAGS 自动生成
    "llm_models": ["open source LLM", "foundation model", "base model"],
    "llm_inference": ["LLM inference engine", "local LLM", "model serving"],
    "llm_finetuning": ["LLM fine-tuning", "LoRA training", "model training"],
    "agents": ["AI agent framework", "multi agent", "agentic workflow"],
    "prompts": ["prompt engineering", "prompt template", "system prompt"],
    "skills": ["claude skill", "SKILL.md", "AI skill"],
    "rag_frameworks": ["RAG framework", "retrieval augmented", "document QA"],
    "vector_databases": ["vector database", "vector store", "embedding database"],
    "search_techniques": ["semantic search", "hybrid search", "neural search"],
    "ai_coding_tools": ["AI code assistant", "AI coding", "code completion"],
    
    # 移民签证
    "work_permit": ["work permit", "LMIA", "employment authorization"],
    "pr_application": ["permanent resident", "express entry", "PNP"],
    "citizenship": ["citizenship application", "naturalization"],
    "visa_renewal": ["visa renewal", "visitor visa"],
    "family_sponsorship": ["family sponsorship", "spouse sponsorship"],
    
    # 住房安居
    "rental": ["apartment rental", "lease agreement"],
    "home_buying": ["home buying", "mortgage", "real estate"],
    "moving": ["moving service", "relocation"],
    "furniture": ["furniture", "home appliances"],
    "utilities": ["utilities setup", "hydro", "internet service"],
    
    # 职业发展
    "job_search": ["job search", "job hunting", "career opportunity"],
    "resume": ["resume writing", "CV template", "cover letter"],
    "interview": ["job interview", "technical interview", "behavioral interview"],
    "certification": ["professional certification", "license exam"],
    "entrepreneurship": ["startup", "business registration", "entrepreneurship"],
    
    # 金融理财
    "banking": ["bank account", "banking service"],
    "credit_card": ["credit card", "credit score"],
    "investment": ["investment", "TFSA", "RRSP"],
    "insurance": ["insurance", "life insurance"],
    "tax": ["tax filing", "tax return", "CRA"],
    "remittance": ["remittance", "money transfer", "forex"],
    
    # 医疗健康
    "health_insurance": ["health insurance", "OHIP", "MSP"],
    "family_doctor": ["family doctor", "clinic"],
    "clinic_visit": ["walk-in clinic", "emergency room"],
    "pharmacy": ["pharmacy", "prescription"],
    "mental_health": ["mental health", "counseling", "therapy"],
    "childcare": ["childcare", "daycare", "vaccination"],
    
    # 交通出行
    "driving_license": ["driving license", "road test", "G1 G2"],
    "car_buying": ["car buying", "used car", "car dealer"],
    "car_insurance": ["car insurance", "auto insurance"],
    "public_transit": ["public transit", "bus subway"],
    "flight": ["flight booking", "airline ticket"],
}

# ============================================================
# 匹配标签 - 用于分类发现的资源（产品名、工具名、具体概念）
# ============================================================
MATCH_TAGS: Dict[str, List[Dict[str, str]]] = {
    # LLM API 服务商 - provider 名字既是搜索关键词也是匹配标签
    "llm_providers": [
        # 国际
        {"code": "openai", "name": "OpenAI", "name_en": "OpenAI"},
        {"code": "anthropic", "name": "Anthropic", "name_en": "Anthropic"},
        {"code": "google_ai", "name": "Google AI", "name_en": "Google AI"},
        {"code": "gemini", "name": "Gemini", "name_en": "Gemini"},
        {"code": "groq", "name": "Groq", "name_en": "Groq"},
        {"code": "together", "name": "Together AI", "name_en": "Together AI"},
        {"code": "cerebras", "name": "Cerebras", "name_en": "Cerebras"},
        {"code": "sambanova", "name": "SambaNova", "name_en": "SambaNova"},
        {"code": "cohere", "name": "Cohere", "name_en": "Cohere"},
        {"code": "openrouter", "name": "OpenRouter", "name_en": "OpenRouter"},
        {"code": "fireworks", "name": "Fireworks AI", "name_en": "Fireworks AI"},
        {"code": "replicate", "name": "Replicate", "name_en": "Replicate"},
        {"code": "xai", "name": "xAI", "name_en": "xAI"},
        {"code": "mistral", "name": "Mistral AI", "name_en": "Mistral AI"},
        {"code": "perplexity", "name": "Perplexity", "name_en": "Perplexity"},
        {"code": "huggingface", "name": "Hugging Face", "name_en": "Hugging Face"},
        {"code": "cloudflare", "name": "Cloudflare AI", "name_en": "Cloudflare AI"},
        # 中国
        {"code": "deepseek", "name": "DeepSeek", "name_en": "DeepSeek"},
        {"code": "zhipu", "name": "智谱AI", "name_en": "Zhipu AI"},
        {"code": "qwen", "name": "通义千问", "name_en": "Qwen"},
        {"code": "baichuan", "name": "百川智能", "name_en": "Baichuan"},
        {"code": "moonshot", "name": "月之暗面", "name_en": "Moonshot"},
        {"code": "minimax", "name": "MiniMax", "name_en": "MiniMax"},
        {"code": "stepfun", "name": "阶跃星辰", "name_en": "StepFun"},
        {"code": "yi", "name": "零一万物", "name_en": "01.AI"},
        {"code": "doubao", "name": "豆包", "name_en": "Doubao"},
        {"code": "hunyuan", "name": "混元", "name_en": "Hunyuan"},
        {"code": "ernie", "name": "文心一言", "name_en": "ERNIE"},
        {"code": "spark", "name": "讯飞星火", "name_en": "Spark"},
    ],
    
    # LLM 模型
    "llm_models": [
        {"code": "llama", "name": "Llama", "name_en": "Llama"},
        {"code": "mistral", "name": "Mistral", "name_en": "Mistral"},
        {"code": "deepseek", "name": "DeepSeek", "name_en": "DeepSeek"},
        {"code": "qwen", "name": "通义千问", "name_en": "Qwen"},
        {"code": "phi", "name": "Phi", "name_en": "Phi"},
        {"code": "gemma", "name": "Gemma", "name_en": "Gemma"},
        {"code": "yi", "name": "Yi", "name_en": "Yi"},
        {"code": "chatglm", "name": "ChatGLM", "name_en": "ChatGLM"},
        {"code": "huggingface", "name": "HuggingFace", "name_en": "HuggingFace"},
    ],
    
    # LLM 推理引擎
    "llm_inference": [
        {"code": "ollama", "name": "Ollama", "name_en": "Ollama"},
        {"code": "vllm", "name": "vLLM", "name_en": "vLLM"},
        {"code": "llama_cpp", "name": "llama.cpp", "name_en": "llama.cpp"},
        {"code": "tgi", "name": "TGI", "name_en": "Text Generation Inference"},
        {"code": "mlx", "name": "MLX", "name_en": "MLX"},
        {"code": "exllama", "name": "ExLlama", "name_en": "ExLlama"},
        {"code": "gguf", "name": "GGUF", "name_en": "GGUF"},
        {"code": "transformers", "name": "Transformers", "name_en": "Transformers"},
    ],
    
    # LLM 微调
    "llm_finetuning": [
        {"code": "unsloth", "name": "Unsloth", "name_en": "Unsloth"},
        {"code": "llamafactory", "name": "LlamaFactory", "name_en": "LlamaFactory"},
        {"code": "axolotl", "name": "Axolotl", "name_en": "Axolotl"},
        {"code": "lora", "name": "LoRA", "name_en": "LoRA"},
        {"code": "qlora", "name": "QLoRA", "name_en": "QLoRA"},
        {"code": "peft", "name": "PEFT", "name_en": "PEFT"},
        {"code": "sft", "name": "SFT", "name_en": "Supervised Fine-Tuning"},
        {"code": "rlhf", "name": "RLHF", "name_en": "RLHF"},
        {"code": "dpo", "name": "DPO", "name_en": "DPO"},
    ],
    
    # AI Agent 框架
    "agents": [
        {"code": "langchain", "name": "LangChain", "name_en": "LangChain"},
        {"code": "langgraph", "name": "LangGraph", "name_en": "LangGraph"},
        {"code": "autogen", "name": "AutoGen", "name_en": "AutoGen"},
        {"code": "crewai", "name": "CrewAI", "name_en": "CrewAI"},
        {"code": "semantic_kernel", "name": "Semantic Kernel", "name_en": "Semantic Kernel"},
        {"code": "openai_swarm", "name": "Swarm", "name_en": "Swarm"},
        {"code": "smolagents", "name": "Smolagents", "name_en": "Smolagents"},
        {"code": "dify", "name": "Dify", "name_en": "Dify"},
        {"code": "metagpt", "name": "MetaGPT", "name_en": "MetaGPT"},
        {"code": "camel", "name": "CAMEL", "name_en": "CAMEL"},
        {"code": "qwen_agent", "name": "Qwen-Agent", "name_en": "Qwen-Agent"},
        {"code": "agentscope", "name": "AgentScope", "name_en": "AgentScope"},
        {"code": "ai_agent", "name": "AI Agent", "name_en": "AI Agent"},
        {"code": "multi_agent", "name": "多智能体", "name_en": "Multi Agent"},
    ],
    
    # 提示词工程
    "prompts": [
        {"code": "prompt", "name": "提示词", "name_en": "Prompt"},
        {"code": "prompt_engineering", "name": "提示工程", "name_en": "Prompt Engineering"},
        {"code": "system_prompt", "name": "系统提示词", "name_en": "System Prompt"},
        {"code": "few_shot", "name": "少样本", "name_en": "Few Shot"},
        {"code": "chain_of_thought", "name": "思维链", "name_en": "Chain of Thought"},
    ],
    
    # Claude Skills
    "skills": [
        {"code": "claude_skill", "name": "Claude Skill", "name_en": "Claude Skill"},
        {"code": "skill_md", "name": "SKILL.md", "name_en": "SKILL.md"},
        {"code": "claude_code_skill", "name": "Claude Code Skill", "name_en": "Claude Code Skill"},
    ],
    
    # RAG 框架
    "rag_frameworks": [
        {"code": "rag", "name": "RAG", "name_en": "RAG"},
        {"code": "llamaindex", "name": "LlamaIndex", "name_en": "LlamaIndex"},
        {"code": "haystack", "name": "Haystack", "name_en": "Haystack"},
        {"code": "dspy", "name": "DSPy", "name_en": "DSPy"},
        {"code": "document_parsing", "name": "文档解析", "name_en": "Document Parsing"},
        {"code": "chunking", "name": "文本分块", "name_en": "Chunking"},
    ],
    
    # 向量数据库
    "vector_databases": [
        {"code": "chroma", "name": "Chroma", "name_en": "Chroma"},
        {"code": "pinecone", "name": "Pinecone", "name_en": "Pinecone"},
        {"code": "qdrant", "name": "Qdrant", "name_en": "Qdrant"},
        {"code": "weaviate", "name": "Weaviate", "name_en": "Weaviate"},
        {"code": "milvus", "name": "Milvus", "name_en": "Milvus"},
        {"code": "pgvector", "name": "pgvector", "name_en": "pgvector"},
        {"code": "faiss", "name": "FAISS", "name_en": "FAISS"},
        {"code": "vector_db", "name": "向量数据库", "name_en": "Vector Database"},
        {"code": "embedding", "name": "嵌入模型", "name_en": "Embedding"},
    ],
    
    # 搜索技术
    "search_techniques": [
        {"code": "semantic_search", "name": "语义搜索", "name_en": "Semantic Search"},
        {"code": "hybrid_search", "name": "混合搜索", "name_en": "Hybrid Search"},
        {"code": "reranking", "name": "重排序", "name_en": "Reranking"},
        {"code": "bm25", "name": "BM25", "name_en": "BM25"},
    ],
    
    # AI 编程工具
    "ai_coding_tools": [
        {"code": "claude_code", "name": "Claude Code", "name_en": "Claude Code"},
        {"code": "cursor", "name": "Cursor", "name_en": "Cursor"},
        {"code": "copilot", "name": "Copilot", "name_en": "Copilot"},
        {"code": "kiro", "name": "Kiro", "name_en": "Kiro"},
        {"code": "windsurf", "name": "Windsurf", "name_en": "Windsurf"},
        {"code": "aider", "name": "Aider", "name_en": "Aider"},
        {"code": "cline", "name": "Cline", "name_en": "Cline"},
        {"code": "continue", "name": "Continue", "name_en": "Continue"},
    ],
}


# ============================================================
# 非 AI 领域的匹配标签
# ============================================================
MATCH_TAGS.update({
    # 移民签证
    "work_permit": [
        {"code": "work_permit", "name": "工签", "name_en": "Work Permit"},
        {"code": "lmia", "name": "LMIA", "name_en": "LMIA"},
        {"code": "employment", "name": "工作许可", "name_en": "Employment"},
    ],
    "pr_application": [
        {"code": "pr", "name": "PR", "name_en": "PR"},
        {"code": "permanent_resident", "name": "永久居民", "name_en": "Permanent Resident"},
        {"code": "express_entry", "name": "EE快速通道", "name_en": "Express Entry"},
        {"code": "pnp", "name": "省提名", "name_en": "PNP"},
    ],
    "citizenship": [
        {"code": "citizenship", "name": "入籍", "name_en": "Citizenship"},
        {"code": "citizenship_test", "name": "入籍考试", "name_en": "Citizenship Test"},
    ],
    "visa_renewal": [
        {"code": "visa_renewal", "name": "续签", "name_en": "Visa Renewal"},
        {"code": "visitor_visa", "name": "访客签证", "name_en": "Visitor Visa"},
    ],
    "family_sponsorship": [
        {"code": "family_sponsorship", "name": "家庭团聚", "name_en": "Family Sponsorship"},
        {"code": "spouse_sponsorship", "name": "配偶担保", "name_en": "Spouse Sponsorship"},
    ],
    
    # 住房安居
    "rental": [
        {"code": "rental", "name": "租房", "name_en": "Rental"},
        {"code": "apartment", "name": "公寓", "name_en": "Apartment"},
        {"code": "lease", "name": "租约", "name_en": "Lease"},
    ],
    "home_buying": [
        {"code": "home_buying", "name": "买房", "name_en": "Home Buying"},
        {"code": "mortgage", "name": "房贷", "name_en": "Mortgage"},
        {"code": "down_payment", "name": "首付", "name_en": "Down Payment"},
    ],
    "moving": [
        {"code": "moving", "name": "搬家", "name_en": "Moving"},
        {"code": "movers", "name": "搬家公司", "name_en": "Movers"},
    ],
    "furniture": [
        {"code": "furniture", "name": "家具", "name_en": "Furniture"},
        {"code": "appliances", "name": "家电", "name_en": "Appliances"},
        {"code": "ikea", "name": "IKEA", "name_en": "IKEA"},
    ],
    "utilities": [
        {"code": "utilities", "name": "水电", "name_en": "Utilities"},
        {"code": "hydro", "name": "电费", "name_en": "Hydro"},
        {"code": "internet", "name": "网络", "name_en": "Internet"},
    ],
    
    # 职业发展
    "job_search": [
        {"code": "job_search", "name": "求职", "name_en": "Job Search"},
        {"code": "linkedin", "name": "LinkedIn", "name_en": "LinkedIn"},
        {"code": "indeed", "name": "Indeed", "name_en": "Indeed"},
    ],
    "resume": [
        {"code": "resume", "name": "简历", "name_en": "Resume"},
        {"code": "cv", "name": "CV", "name_en": "CV"},
        {"code": "cover_letter", "name": "求职信", "name_en": "Cover Letter"},
    ],
    "interview": [
        {"code": "interview", "name": "面试", "name_en": "Interview"},
        {"code": "behavioral_interview", "name": "行为面试", "name_en": "Behavioral Interview"},
        {"code": "technical_interview", "name": "技术面试", "name_en": "Technical Interview"},
        {"code": "leetcode", "name": "LeetCode", "name_en": "LeetCode"},
        {"code": "system_design", "name": "系统设计", "name_en": "System Design"},
    ],
    "certification": [
        {"code": "certification", "name": "认证", "name_en": "Certification"},
        {"code": "license", "name": "执照", "name_en": "License"},
    ],
    "entrepreneurship": [
        {"code": "entrepreneurship", "name": "创业", "name_en": "Entrepreneurship"},
        {"code": "startup", "name": "初创公司", "name_en": "Startup"},
        {"code": "business_registration", "name": "注册公司", "name_en": "Business Registration"},
    ],
    
    # 金融理财
    "banking": [
        {"code": "banking", "name": "银行", "name_en": "Banking"},
        {"code": "bank_account", "name": "开户", "name_en": "Bank Account"},
        {"code": "td_bank", "name": "TD银行", "name_en": "TD Bank"},
        {"code": "rbc", "name": "RBC", "name_en": "RBC"},
    ],
    "credit_card": [
        {"code": "credit_card", "name": "信用卡", "name_en": "Credit Card"},
        {"code": "credit_score", "name": "信用分", "name_en": "Credit Score"},
        {"code": "cashback", "name": "返现", "name_en": "Cashback"},
    ],
    "investment": [
        {"code": "investment", "name": "投资", "name_en": "Investment"},
        {"code": "tfsa", "name": "TFSA", "name_en": "TFSA"},
        {"code": "rrsp", "name": "RRSP", "name_en": "RRSP"},
        {"code": "etf", "name": "ETF", "name_en": "ETF"},
    ],
    "insurance": [
        {"code": "insurance", "name": "保险", "name_en": "Insurance"},
        {"code": "life_insurance", "name": "人寿保险", "name_en": "Life Insurance"},
    ],
    "tax": [
        {"code": "tax", "name": "税务", "name_en": "Tax"},
        {"code": "tax_filing", "name": "报税", "name_en": "Tax Filing"},
        {"code": "cra", "name": "CRA", "name_en": "CRA"},
    ],
    "remittance": [
        {"code": "remittance", "name": "汇款", "name_en": "Remittance"},
        {"code": "wise", "name": "Wise", "name_en": "Wise"},
        {"code": "forex", "name": "外汇", "name_en": "Forex"},
    ],
    
    # 医疗健康
    "health_insurance": [
        {"code": "health_insurance", "name": "医保", "name_en": "Health Insurance"},
        {"code": "ohip", "name": "OHIP", "name_en": "OHIP"},
        {"code": "msp", "name": "MSP", "name_en": "MSP"},
    ],
    "family_doctor": [
        {"code": "family_doctor", "name": "家庭医生", "name_en": "Family Doctor"},
        {"code": "clinic", "name": "诊所", "name_en": "Clinic"},
    ],
    "clinic_visit": [
        {"code": "walk_in_clinic", "name": "Walk-in诊所", "name_en": "Walk-in Clinic"},
        {"code": "emergency", "name": "急诊", "name_en": "Emergency"},
    ],
    "pharmacy": [
        {"code": "pharmacy", "name": "药房", "name_en": "Pharmacy"},
        {"code": "prescription", "name": "处方", "name_en": "Prescription"},
    ],
    "mental_health": [
        {"code": "mental_health", "name": "心理健康", "name_en": "Mental Health"},
        {"code": "counseling", "name": "心理咨询", "name_en": "Counseling"},
    ],
    "childcare": [
        {"code": "childcare", "name": "儿童保健", "name_en": "Childcare"},
        {"code": "daycare", "name": "托儿所", "name_en": "Daycare"},
        {"code": "vaccination", "name": "疫苗", "name_en": "Vaccination"},
    ],
    
    # 交通出行
    "driving_license": [
        {"code": "driving_license", "name": "驾照", "name_en": "Driving License"},
        {"code": "g1_test", "name": "G1考试", "name_en": "G1 Test"},
        {"code": "g2_test", "name": "G2考试", "name_en": "G2 Test"},
        {"code": "road_test", "name": "路考", "name_en": "Road Test"},
    ],
    "car_buying": [
        {"code": "car_buying", "name": "买车", "name_en": "Car Buying"},
        {"code": "used_car", "name": "二手车", "name_en": "Used Car"},
        {"code": "car_dealer", "name": "车行", "name_en": "Car Dealer"},
    ],
    "car_insurance": [
        {"code": "car_insurance", "name": "车险", "name_en": "Car Insurance"},
        {"code": "auto_insurance", "name": "汽车保险", "name_en": "Auto Insurance"},
    ],
    "public_transit": [
        {"code": "public_transit", "name": "公共交通", "name_en": "Public Transit"},
        {"code": "ttc", "name": "TTC", "name_en": "TTC"},
        {"code": "presto", "name": "Presto", "name_en": "Presto"},
    ],
    "flight": [
        {"code": "flight", "name": "机票", "name_en": "Flight"},
        {"code": "airline", "name": "航空公司", "name_en": "Airline"},
    ],
})


# ============================================================
# 兼容旧代码 - 生成扁平化的 TAGS 列表
# ============================================================
def _build_flat_tags() -> List[Dict[str, Any]]:
    """将 MATCH_TAGS 转换为扁平的 TAGS 列表（兼容旧代码）"""
    tags = []
    for domain_code, tag_list in MATCH_TAGS.items():
        for tag in tag_list:
            tags.append({
                "code": tag["code"],
                "name": tag["name"],
                "name_en": tag["name_en"],
                "domain_code": domain_code,
            })
    return tags


TAGS: List[Dict[str, Any]] = _build_flat_tags()

# 兼容旧代码
AI_EXTRA_TAGS: List[Dict[str, Any]] = []


# ============================================================
# 辅助函数
# ============================================================
def get_domain_keywords(domain_code: str) -> List[str]:
    """获取领域的搜索关键词"""
    return DOMAIN_KEYWORDS.get(domain_code, [])


def get_domain_match_tags(domain_code: str) -> List[Dict[str, str]]:
    """获取领域的匹配标签"""
    return MATCH_TAGS.get(domain_code, [])
