"""初始化 LLM 模型和 Prompt 数据"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from src.common.supabase import get_supabase_admin

from postgrest.exceptions import APIError

client = get_supabase_admin()


# ========== LLM Models ==========
MODELS = [
    {
        "name": "gpt-4o",
        "display_name": "GPT-4o",
        "provider": "openai",
        "api_endpoint": "https://api.openai.com/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "gpt-4o-mini",
        "display_name": "GPT-4o Mini",
        "provider": "openai",
        "api_endpoint": "https://api.openai.com/v1",
        "is_active": True,
        "is_default": True,  # 默认模型
        "config": {},
    },
    {
        "name": "claude-3-5-sonnet-20241022",
        "display_name": "Claude 3.5 Sonnet",
        "provider": "anthropic",
        "api_endpoint": "https://api.anthropic.com/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "deepseek-chat",
        "display_name": "DeepSeek Chat",
        "provider": "deepseek",
        "api_endpoint": "https://api.deepseek.com/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "gemini-2.0-flash",
        "display_name": "Gemini 2.0 Flash",
        "provider": "google",
        "api_endpoint": "https://generativelanguage.googleapis.com/v1beta",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
    {
        "name": "llama-3.3-70b-versatile",
        "display_name": "Llama 3.3 70B (Groq)",
        "provider": "groq",
        "api_endpoint": "https://api.groq.com/openai/v1",
        "is_active": True,
        "is_default": False,
        "config": {},
    },
]


# ========== LLM Prompts ==========
PROMPTS = [
    # 求职领域
    {
        "name": "resume_analysis",
        "display_name": "简历分析",
        "description": "分析简历并给出优化建议",
        "category": "job",
        "system_prompt": """你是一位专业的北美职场简历顾问，精通 ATS 系统和北美招聘流程。

请分析用户提供的简历，从以下维度给出评价：
1. 整体结构（是否符合北美简历规范）
2. 内容质量（成就描述是否量化、动词使用是否有力）
3. ATS 兼容性（格式、关键词）
4. 针对性建议

请以 JSON 格式返回分析结果：
{
  "score": 1-100,
  "summary": "整体评价",
  "strengths": ["优点1", "优点2"],
  "weaknesses": ["不足1", "不足2"],
  "suggestions": ["建议1", "建议2"],
  "ats_score": 1-100,
  "keyword_suggestions": ["关键词1", "关键词2"]
}""",
        "user_prompt_template": "请分析以下简历：\n\n{resume_content}",
        "temperature": 0.3,
        "max_tokens": 2000,
        "is_active": True,
    },
    {
        "name": "interview_feedback",
        "display_name": "面试答案评估",
        "description": "评估面试回答并给出改进建议",
        "category": "job",
        "system_prompt": """你是一位资深的北美职场面试官，请评估用户的面试回答。

评估维度：
1. 结构性（是否使用 STAR 方法）
2. 具体性（是否有具体例子和数据）
3. 相关性（是否切题）
4. 表达清晰度

请以 JSON 格式返回：
{
  "score": 1-100,
  "overall": "整体评价",
  "strengths": ["优点"],
  "improvements": ["改进建议"],
  "sample_answer": "参考答案"
}""",
        "user_prompt_template": "问题：{question}\n\n用户回答：{answer}",
        "temperature": 0.5,
        "max_tokens": 1500,
        "is_active": True,
    },
    {
        "name": "job_advisor",
        "display_name": "求职顾问",
        "description": "求职相关问题的智能顾问",
        "category": "job",
        "system_prompt": """你是一位专业的北美求职顾问，帮助用户解答求职相关问题。

你的专长包括：
- 北美求职策略和流程
- 简历和求职信优化
- 面试准备和技巧
- 薪资谈判
- 职业规划
- H1B/OPT 等签证相关求职建议

请用专业但友好的语气回答，给出具体可行的建议。如果涉及法律或签证问题，提醒用户咨询专业律师。""",
        "user_prompt_template": "{message}",
        "temperature": 0.7,
        "max_tokens": 2000,
        "is_active": True,
    },
    # 通用顾问
    {
        "name": "general_advisor",
        "display_name": "通用顾问",
        "description": "北美生活通用问题顾问",
        "category": "advisor",
        "system_prompt": """你是北美生活决策顾问，帮助用户解答北美生活相关问题。

你的专长包括：
- 住房（租房、买房）
- 交通（买车、租车、公共交通）
- 教育（学校选择、申请）
- 金融（银行、信用卡、投资）
- 保险（医疗、汽车、房屋）
- 日常生活（购物、餐饮、娱乐）

请用专业但友好的语气回答，给出具体可行的建议。""",
        "user_prompt_template": "{message}",
        "temperature": 0.7,
        "max_tokens": 2000,
        "is_active": True,
    },
    # 分析类
    {
        "name": "content_summary",
        "display_name": "内容摘要",
        "description": "生成内容摘要",
        "category": "analysis",
        "system_prompt": "你是一个专业的内容分析助手。请对用户提供的内容生成简洁准确的摘要。",
        "user_prompt_template": "请为以下内容生成摘要：\n\n{content}",
        "temperature": 0.3,
        "max_tokens": 500,
        "is_active": True,
    },
    {
        "name": "text_translation",
        "display_name": "文本翻译",
        "description": "中英文互译",
        "category": "general",
        "system_prompt": """你是一个专业的翻译助手。
- 如果输入是中文，翻译成英文
- 如果输入是英文，翻译成中文
- 保持原文的语气和风格
- 专业术语使用准确""",
        "user_prompt_template": "{text}",
        "temperature": 0.3,
        "max_tokens": 2000,
        "is_active": True,
    },
]


def seed_models():
    """初始化模型数据"""
    print("Seeding LLM models...")
    
    for model in MODELS:
        # 检查是否已存在
        try:
            existing = (
                client.table("llm_models")
                .select("id")
                .eq("name", model["name"])
                .execute()
            )
            
            if existing.data and len(existing.data) > 0:
                print(f"  Model '{model['name']}' already exists, skipping")
                continue
        except APIError as e:
            print(f"  Query error for '{model['name']}': {e}")
        
        try:
            client.table("llm_models").insert(model).execute()
            print(f"  Created model: {model['display_name']}")
        except APIError as e:
            print(f"  Error creating model '{model['name']}': {e}")
    
    print(f"Done!")


def seed_prompts():
    """初始化 Prompt 数据"""
    print("\nSeeding LLM prompts...")
    
    for prompt in PROMPTS:
        # 检查是否已存在
        try:
            existing = (
                client.table("llm_prompts")
                .select("id")
                .eq("name", prompt["name"])
                .execute()
            )
            
            if existing.data and len(existing.data) > 0:
                print(f"  Prompt '{prompt['name']}' already exists, skipping")
                continue
        except APIError as e:
            print(f"  Query error for '{prompt['name']}': {e}")
        
        try:
            client.table("llm_prompts").insert(prompt).execute()
            print(f"  Created prompt: {prompt['display_name']}")
        except APIError as e:
            print(f"  Error creating prompt '{prompt['name']}': {e}")
    
    print(f"Done!")


if __name__ == "__main__":
    seed_models()
    seed_prompts()
    print("\n✅ LLM seed data initialized!")
