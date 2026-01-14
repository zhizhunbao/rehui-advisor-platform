"""Seed initial product lines, domain categories and domains - 使用 Supabase API"""
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from src.common.supabase import get_supabase_admin
from postgrest.exceptions import APIError
from seed_domain_prompts import DOMAIN_PROMPTS


def clean_all_data():
    """清理所有历史数据"""
    client = get_supabase_admin()
    types_to_clean = ["product_line", "domain_category", "domain", "domain_question", "admin_domain_category", "admin_domain", "admin_question"]
    
    for doc_type in types_to_clean:
        try:
            result = client.table("documents").delete().eq("type", doc_type).execute()
            count = len(result.data) if result.data else 0
            print(f"Deleted {count} records of type: {doc_type}")
        except APIError as e:
            print(f"Error cleaning {doc_type}: {e}")


def seed_product_lines():
    """Seed product lines"""
    client = get_supabase_admin()
    
    product_lines = [
        {
            "code": "life_service",
            "name": "生活服务",
            "name_en": "Life Services",
            "description": "北美新移民生活咨询服务",
            "description_en": "Life consulting services for North America newcomers",
            "icon": "Compass",
            "color": "bg-blue-500",
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "learning",
            "name": "技能学习",
            "name_en": "Skill Learning",
            "description": "在线课程、实验练习、AI 学习助手",
            "description_en": "Online courses, labs, and AI learning assistant",
            "icon": "BookOpen",
            "color": "bg-emerald-500",
            "sort_order": 2,
            "is_active": True,
        },
    ]
    
    product_line_ids = {}
    
    for pl in product_lines:
        try:
            new_id = str(uuid4())
            client.table("documents").insert({
                "id": new_id,
                "type": "product_line",
                "data": pl,
                "status": "active",
            }).execute()
            product_line_ids[pl["code"]] = new_id
            print(f"Created product line: {pl['name']} ({pl['code']})")
        except APIError as e:
            print(f"Error with product line {pl['code']}: {e}")
    
    return product_line_ids


def seed_domain_categories(product_line_ids: dict):
    """Seed domain categories"""
    client = get_supabase_admin()
    
    categories = [
        # 生活服务
        {
            "code": "travel",
            "name": "出行旅游",
            "name_en": "Travel & Tourism",
            "description": "机票、酒店、租车等出行相关服务",
            "description_en": "Flight, hotel, car rental and other travel services",
            "icon": "Plane",
            "color": "bg-blue-500",
            "product_line_id": product_line_ids.get("life_service"),
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "living",
            "name": "生活服务",
            "name_en": "Living Services",
            "description": "租房、搬家、日常生活相关服务",
            "description_en": "Housing, moving, and daily life services",
            "icon": "Home",
            "color": "bg-green-500",
            "product_line_id": product_line_ids.get("life_service"),
            "sort_order": 2,
            "is_active": True,
        },
        {
            "code": "career",
            "name": "职业发展",
            "name_en": "Career Development",
            "description": "求职、职业规划、技能提升",
            "description_en": "Job search, career planning, skill development",
            "icon": "Briefcase",
            "color": "bg-purple-500",
            "product_line_id": product_line_ids.get("life_service"),
            "sort_order": 3,
            "is_active": True,
        },
        {
            "code": "finance",
            "name": "金融理财",
            "name_en": "Finance & Investment",
            "description": "投资、保险、税务规划",
            "description_en": "Investment, insurance, tax planning",
            "icon": "TrendingUp",
            "color": "bg-amber-500",
            "product_line_id": product_line_ids.get("life_service"),
            "sort_order": 4,
            "is_active": True,
        },
        {
            "code": "education",
            "name": "教育培训",
            "name_en": "Education & Training",
            "description": "学校选择、语言学习、技能培训",
            "description_en": "School selection, language learning, skill training",
            "icon": "GraduationCap",
            "color": "bg-cyan-500",
            "product_line_id": product_line_ids.get("life_service"),
            "sort_order": 5,
            "is_active": True,
        },
        # 技能学习
        {
            "code": "courses",
            "name": "课程学习",
            "name_en": "Courses",
            "description": "在线视频课程和学习资料",
            "description_en": "Online video courses and learning materials",
            "icon": "PlayCircle",
            "color": "bg-emerald-500",
            "product_line_id": product_line_ids.get("learning"),
            "sort_order": 1,
            "is_active": True,
        },
        {
            "code": "labs",
            "name": "实验练习",
            "name_en": "Labs",
            "description": "动手实践和项目练习",
            "description_en": "Hands-on practice and project exercises",
            "icon": "FlaskConical",
            "color": "bg-violet-500",
            "product_line_id": product_line_ids.get("learning"),
            "sort_order": 2,
            "is_active": True,
        },
        {
            "code": "ai_tutor",
            "name": "AI 助手",
            "name_en": "AI Tutor",
            "description": "AI 学习助手和答疑服务",
            "description_en": "AI learning assistant and Q&A service",
            "icon": "Bot",
            "color": "bg-pink-500",
            "product_line_id": product_line_ids.get("learning"),
            "sort_order": 3,
            "is_active": True,
        },
    ]
    
    category_ids = {}
    
    for cat in categories:
        try:
            new_id = str(uuid4())
            client.table("documents").insert({
                "id": new_id,
                "type": "domain_category",
                "data": cat,
                "status": "active",
            }).execute()
            category_ids[cat["code"]] = new_id
            print(f"Created category: {cat['name']} ({cat['code']})")
        except APIError as e:
            print(f"Error with category {cat['code']}: {e}")
    
    return category_ids


def seed_domains(category_ids: dict):
    """Seed domains"""
    client = get_supabase_admin()
    
    domains = [
        # 出行旅游
        {"code": "flight", "name": "机票预订", "name_en": "Flight Booking", "description": "帮助您比较和预订最优惠的机票", "description_en": "Help you compare and book the best flight deals", "icon": "Plane", "color": "bg-blue-500", "category_id": category_ids.get("travel"), "sort_order": 1, "is_active": True},
        {"code": "hotel", "name": "酒店预订", "name_en": "Hotel Booking", "description": "帮助您找到性价比最高的住宿", "description_en": "Help you find the best value accommodation", "icon": "Hotel", "color": "bg-blue-500", "category_id": category_ids.get("travel"), "sort_order": 2, "is_active": True},
        {"code": "car_rental", "name": "租车服务", "name_en": "Car Rental", "description": "帮助您比较和预订租车服务", "description_en": "Help you compare and book car rental services", "icon": "Car", "color": "bg-blue-500", "category_id": category_ids.get("travel"), "sort_order": 3, "is_active": True},
        # 生活服务
        {"code": "housing", "name": "租房买房", "name_en": "Housing", "description": "帮助您找到理想的住所", "description_en": "Help you find your ideal home", "icon": "Home", "color": "bg-green-500", "category_id": category_ids.get("living"), "sort_order": 1, "is_active": True},
        {"code": "moving", "name": "搬家服务", "name_en": "Moving Services", "description": "帮助您规划和安排搬家事宜", "description_en": "Help you plan and arrange moving services", "icon": "Package", "color": "bg-green-500", "category_id": category_ids.get("living"), "sort_order": 2, "is_active": True},
        # 职业发展
        {"code": "job", "name": "求职就业", "name_en": "Job Search", "description": "帮助您找到理想的工作机会", "description_en": "Help you find your ideal job opportunities", "icon": "Briefcase", "color": "bg-purple-500", "category_id": category_ids.get("career"), "sort_order": 1, "is_active": True},
        {"code": "resume", "name": "简历优化", "name_en": "Resume Optimization", "description": "帮助您优化简历，提升求职竞争力", "description_en": "Help you optimize your resume to improve job competitiveness", "icon": "FileText", "color": "bg-purple-500", "category_id": category_ids.get("career"), "sort_order": 2, "is_active": True},
        # 金融理财
        {"code": "investment", "name": "投资理财", "name_en": "Investment", "description": "帮助您了解投资选择和理财规划", "description_en": "Help you understand investment options and financial planning", "icon": "TrendingUp", "color": "bg-amber-500", "category_id": category_ids.get("finance"), "sort_order": 1, "is_active": True},
        {"code": "insurance", "name": "保险规划", "name_en": "Insurance Planning", "description": "帮助您选择合适的保险方案", "description_en": "Help you choose the right insurance plan", "icon": "ShieldCheck", "color": "bg-amber-500", "category_id": category_ids.get("finance"), "sort_order": 2, "is_active": True},
        {"code": "tax", "name": "税务规划", "name_en": "Tax Planning", "description": "帮助您了解税务知识和规划", "description_en": "Help you understand tax knowledge and planning", "icon": "Receipt", "color": "bg-amber-500", "category_id": category_ids.get("finance"), "sort_order": 3, "is_active": True},
        # 教育培训
        {"code": "school", "name": "学校选择", "name_en": "School Selection", "description": "帮助您选择合适的学校和专业", "description_en": "Help you choose the right school and major", "icon": "GraduationCap", "color": "bg-cyan-500", "category_id": category_ids.get("education"), "sort_order": 1, "is_active": True},
        {"code": "language", "name": "语言学习", "name_en": "Language Learning", "description": "帮助您规划语言学习路径", "description_en": "Help you plan your language learning path", "icon": "Languages", "color": "bg-cyan-500", "category_id": category_ids.get("education"), "sort_order": 2, "is_active": True},
        # 技能学习 - 课程
        {"code": "course_list", "name": "课程列表", "name_en": "Course List", "description": "浏览和学习在线课程", "description_en": "Browse and learn online courses", "icon": "PlayCircle", "color": "bg-emerald-500", "category_id": category_ids.get("courses"), "sort_order": 1, "is_active": True, "route": "/learning/courses"},
        # 技能学习 - 实验
        {"code": "lab_list", "name": "实验列表", "name_en": "Lab List", "description": "动手实践项目练习", "description_en": "Hands-on project exercises", "icon": "FlaskConical", "color": "bg-violet-500", "category_id": category_ids.get("labs"), "sort_order": 1, "is_active": True, "route": "/learning/labs"},
        # 技能学习 - AI 助手
        {"code": "learning_tutor", "name": "学习助手", "name_en": "Learning Tutor", "description": "AI 辅助学习和答疑", "description_en": "AI-assisted learning and Q&A", "icon": "Bot", "color": "bg-pink-500", "category_id": category_ids.get("ai_tutor"), "sort_order": 1, "is_active": True},
    ]
    
    for domain in domains:
        try:
            code = domain["code"]
            if code in DOMAIN_PROMPTS:
                domain["prompt"] = DOMAIN_PROMPTS[code].get("template", "")
            
            client.table("documents").insert({
                "id": str(uuid4()),
                "type": "domain",
                "data": domain,
                "status": "active",
            }).execute()
            print(f"Created domain: {domain['name']} ({code})")
        except APIError as e:
            print(f"Error with domain {domain['code']}: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("Cleaning all data...")
    print("=" * 50)
    clean_all_data()
    
    print()
    print("=" * 50)
    print("Seeding product lines...")
    print("=" * 50)
    product_line_ids = seed_product_lines()
    
    print()
    print("=" * 50)
    print("Seeding domain categories...")
    print("=" * 50)
    category_ids = seed_domain_categories(product_line_ids)
    
    print()
    print("=" * 50)
    print("Seeding domains...")
    print("=" * 50)
    seed_domains(category_ids)
    
    print()
    print("Done!")
