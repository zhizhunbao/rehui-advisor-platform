"""Update all domain icons to emoji"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Domain code to emoji mapping
DOMAIN_ICONS = {
    # 出行旅游
    "flight": "✈️",
    "hotel": "🏨",
    "car_rental": "🚗",
    "travel": "🧳",
    
    # 生活服务
    "housing": "🏠",
    "moving": "📦",
    "utilities": "💡",
    "phone": "📱",
    "internet": "📶",
    "shopping": "🛒",
    "dining": "🍽️",
    "pet": "🐾",
    "cleaning": "🧹",
    "repair": "🔧",
    "storage": "📦",
    "secondhand": "♻️",
    "fitness": "💪",
    "entertainment": "🎬",
    "wedding": "💒",
    "funeral": "🕯️",
    "shipping": "📮",
    "social": "👥",
    
    # 职业发展
    "job": "💼",
    "resume": "📄",
    
    # 金融理财
    "investment": "📈",
    "insurance": "🛡️",
    "tax": "🧾",
    "banking": "🏦",
    "credit": "💳",
    "remittance": "💸",
    
    # 教育学习
    "school": "🎓",
    "language": "🗣️",
    "tutoring": "📚",
    
    # 身份证件
    "visa": "🛂",
    "ssn": "🆔",
    "driving": "🚘",
    
    # 医疗法律
    "healthcare": "🏥",
    "legal": "⚖️",
    "childcare": "👶",
}

# Update each domain
updated = 0
for code, icon in DOMAIN_ICONS.items():
    result = client.table("domains").update({"icon": icon}).eq("code", code).execute()
    if result.data:
        updated += 1
        print(f"  ✓ {code}: {icon}")

print(f"\nUpdated {updated} domains")
