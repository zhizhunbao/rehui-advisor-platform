"""Seed initial domain categories and domains - 使用 Supabase API"""
import sys
from pathlib import Path

# Add backend to path for src.* imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from src.common.supabase import get_supabase_admin
from postgrest.exceptions import APIError


def seed_domain_categories():
    """Seed initial domain categories"""
    client = get_supabase_admin()
    
    categories = [
        {
            "code": "travel",
            "name": "出行旅游",
            "name_en": "Travel & Tourism",
            "description": "机票、酒店、租车等出行相关服务",
            "description_en": "Flight, hotel, car rental and other travel services",
            "icon": "✈️",
            "color": "bg-blue-500",
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "living",
            "name": "生活服务",
            "name_en": "Living Services",
            "description": "租房、搬家、日常生活相关服务",
            "description_en": "Housing, moving, and daily life services",
            "icon": "🏠",
            "color": "bg-green-500",
            "sort_order": 2,
            "is_active": True,
        },
        {
            "code": "career",
            "name": "职业发展",
            "name_en": "Career Development",
            "description": "求职、职业规划、技能提升",
            "description_en": "Job search, career planning, skill development",
            "icon": "💼",
            "color": "bg-purple-500",
            "sort_order": 3,
            "is_active": True,
        },
        {
            "code": "finance",
            "name": "金融理财",
            "name_en": "Finance & Investment",
            "description": "投资、保险、税务规划",
            "description_en": "Investment, insurance, tax planning",
            "icon": "💰",
            "color": "bg-amber-500",
            "sort_order": 4,
            "is_active": True,
        },
        {
            "code": "education",
            "name": "教育培训",
            "name_en": "Education & Training",
            "description": "学校选择、语言学习、技能培训",
            "description_en": "School selection, language learning, skill training",
            "icon": "🎓",
            "color": "bg-cyan-500",
            "sort_order": 5,
            "is_active": True,
        },
    ]
    
    category_ids = {}
    
    for cat in categories:
        try:
            # Check if category exists
            response = (
                client.table("domain_categories")
                .select("id")
                .eq("code", cat["code"])
                .execute()
            )
            
            if response.data:
                category_ids[cat["code"]] = response.data[0]["id"]
                print(f"Category '{cat['code']}' already exists, skipping")
                continue
            
            # Create category
            result = client.table("domain_categories").insert(cat).execute()
            category_ids[cat["code"]] = result.data[0]["id"]
            print(f"Created category: {cat['name']} ({cat['code']})")
            
        except APIError as e:
            print(f"Error creating category {cat['code']}: {e}")
    
    return category_ids


def seed_domains(category_ids: dict):
    """Seed initial domains"""
    client = get_supabase_admin()
    
    domains = [
        # 出行旅游
        {
            "code": "flight",
            "name": "机票预订",
            "name_en": "Flight Booking",
            "description": "帮助您比较和预订最优惠的机票",
            "description_en": "Help you compare and book the best flight deals",
            "icon": "✈️",
            "color": "bg-blue-600",
            "prompt": "你是一位专业的机票预订顾问，帮助用户找到最合适的航班。",
            "prompt_en": "You are a professional flight booking advisor helping users find the best flights.",
            "category_id": category_ids.get("travel"),
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "hotel",
            "name": "酒店预订",
            "name_en": "Hotel Booking",
            "description": "帮助您找到性价比最高的住宿",
            "description_en": "Help you find the best value accommodation",
            "icon": "🏨",
            "color": "bg-blue-500",
            "prompt": "你是一位专业的酒店预订顾问，帮助用户找到最合适的住宿。",
            "prompt_en": "You are a professional hotel booking advisor helping users find the best accommodation.",
            "category_id": category_ids.get("travel"),
            "sort_order": 2,
            "is_active": True,
        },
        {
            "code": "car_rental",
            "name": "租车服务",
            "name_en": "Car Rental",
            "description": "帮助您比较和预订租车服务",
            "description_en": "Help you compare and book car rental services",
            "icon": "🚗",
            "color": "bg-blue-400",
            "prompt": "你是一位专业的租车顾问，帮助用户找到最合适的租车方案。",
            "prompt_en": "You are a professional car rental advisor helping users find the best rental options.",
            "category_id": category_ids.get("travel"),
            "sort_order": 3,
            "is_active": True,
        },
        # 生活服务
        {
            "code": "housing",
            "name": "租房买房",
            "name_en": "Housing",
            "description": "帮助您找到理想的住所",
            "description_en": "Help you find your ideal home",
            "icon": "🏠",
            "color": "bg-green-600",
            "prompt": "你是一位专业的房产顾问，帮助用户找到最合适的住所。",
            "prompt_en": "You are a professional housing advisor helping users find the best home.",
            "category_id": category_ids.get("living"),
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "moving",
            "name": "搬家服务",
            "name_en": "Moving Services",
            "description": "帮助您规划和安排搬家事宜",
            "description_en": "Help you plan and arrange moving services",
            "icon": "📦",
            "color": "bg-green-500",
            "prompt": "你是一位专业的搬家顾问，帮助用户规划搬家事宜。",
            "prompt_en": "You are a professional moving advisor helping users plan their move.",
            "category_id": category_ids.get("living"),
            "sort_order": 2,
            "is_active": True,
        },
        # 职业发展
        {
            "code": "job",
            "name": "求职就业",
            "name_en": "Job Search",
            "description": "帮助您找到理想的工作机会",
            "description_en": "Help you find your ideal job opportunities",
            "icon": "💼",
            "color": "bg-purple-600",
            "prompt": "你是一位专业的职业顾问，帮助用户找到最合适的工作。",
            "prompt_en": "You are a professional career advisor helping users find the best job.",
            "category_id": category_ids.get("career"),
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "resume",
            "name": "简历优化",
            "name_en": "Resume Optimization",
            "description": "帮助您优化简历，提升求职竞争力",
            "description_en": "Help you optimize your resume to improve job competitiveness",
            "icon": "📄",
            "color": "bg-purple-500",
            "prompt": "你是一位专业的简历顾问，帮助用户优化简历。",
            "prompt_en": "You are a professional resume advisor helping users optimize their resume.",
            "category_id": category_ids.get("career"),
            "sort_order": 2,
            "is_active": True,
        },
        # 金融理财
        {
            "code": "investment",
            "name": "投资理财",
            "name_en": "Investment",
            "description": "帮助您了解投资选择和理财规划",
            "description_en": "Help you understand investment options and financial planning",
            "icon": "📈",
            "color": "bg-amber-600",
            "prompt": "你是一位专业的投资顾问，帮助用户了解投资选择。",
            "prompt_en": "You are a professional investment advisor helping users understand investment options.",
            "category_id": category_ids.get("finance"),
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "insurance",
            "name": "保险规划",
            "name_en": "Insurance Planning",
            "description": "帮助您选择合适的保险方案",
            "description_en": "Help you choose the right insurance plan",
            "icon": "🛡️",
            "color": "bg-amber-500",
            "prompt": "你是一位专业的保险顾问，帮助用户选择合适的保险。",
            "prompt_en": "You are a professional insurance advisor helping users choose the right insurance.",
            "category_id": category_ids.get("finance"),
            "sort_order": 2,
            "is_active": True,
        },
        {
            "code": "tax",
            "name": "税务规划",
            "name_en": "Tax Planning",
            "description": "帮助您了解税务知识和规划",
            "description_en": "Help you understand tax knowledge and planning",
            "icon": "🧾",
            "color": "bg-amber-400",
            "prompt": "你是一位专业的税务顾问，帮助用户了解税务规划。",
            "prompt_en": "You are a professional tax advisor helping users understand tax planning.",
            "category_id": category_ids.get("finance"),
            "sort_order": 3,
            "is_active": True,
        },
        # 教育培训
        {
            "code": "school",
            "name": "学校选择",
            "name_en": "School Selection",
            "description": "帮助您选择合适的学校和专业",
            "description_en": "Help you choose the right school and major",
            "icon": "🎓",
            "color": "bg-cyan-600",
            "prompt": "你是一位专业的教育顾问，帮助用户选择合适的学校。",
            "prompt_en": "You are a professional education advisor helping users choose the right school.",
            "category_id": category_ids.get("education"),
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "language",
            "name": "语言学习",
            "name_en": "Language Learning",
            "description": "帮助您规划语言学习路径",
            "description_en": "Help you plan your language learning path",
            "icon": "🗣️",
            "color": "bg-cyan-500",
            "prompt": "你是一位专业的语言学习顾问，帮助用户规划学习路径。",
            "prompt_en": "You are a professional language learning advisor helping users plan their learning path.",
            "category_id": category_ids.get("education"),
            "sort_order": 2,
            "is_active": True,
        },
    ]
    
    for domain in domains:
        try:
            # Check if domain exists
            response = (
                client.table("domains")
                .select("id")
                .eq("code", domain["code"])
                .execute()
            )
            
            if response.data:
                print(f"Domain '{domain['code']}' already exists, skipping")
                continue
            
            # Create domain
            client.table("domains").insert(domain).execute()
            print(f"Created domain: {domain['name']} ({domain['code']})")
            
        except APIError as e:
            print(f"Error creating domain {domain['code']}: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("Seeding domain categories...")
    print("=" * 50)
    category_ids = seed_domain_categories()
    
    print()
    print("=" * 50)
    print("Seeding domains...")
    print("=" * 50)
    seed_domains(category_ids)
    
    print()
    print("Done!")
