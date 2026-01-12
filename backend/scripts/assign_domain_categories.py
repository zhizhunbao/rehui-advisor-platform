"""Assign categories to domains"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Get categories
cat_response = client.table("domain_categories").select("id, name").execute()
categories = {c["name"]: c["id"] for c in cat_response.data}
print("Categories:", categories)

# Domain to category mapping
domain_categories = {
    # 出行旅游
    "flight": "出行旅游",
    "hotel": "出行旅游",
    "car_rental": "出行旅游",
    "travel": "出行旅游",
    
    # 生活服务
    "housing": "生活服务",
    "moving": "生活服务",
    "utilities": "生活服务",
    "phone": "生活服务",
    "internet": "生活服务",
    "shopping": "生活服务",
    "dining": "生活服务",
    "pet": "生活服务",
    "cleaning": "生活服务",
    "repair": "生活服务",
    "storage": "生活服务",
    "secondhand": "生活服务",
    "fitness": "生活服务",
    "entertainment": "生活服务",
    "wedding": "生活服务",
    "funeral": "生活服务",
    "shipping": "生活服务",
    "social": "生活服务",
    
    # 职业发展
    "job": "职业发展",
    "resume": "职业发展",
    
    # 金融理财
    "investment": "金融理财",
    "insurance": "金融理财",
    "tax": "金融理财",
    "banking": "金融理财",
    "credit": "金融理财",
    "remittance": "金融理财",
    
    # 教育学习
    "school": "教育学习",
    "language": "教育学习",
    "tutoring": "教育学习",
    
    # 身份证件 - 需要新建分类
    "visa": "身份证件",
    "ssn": "身份证件",
    "driving": "身份证件",
    
    # 医疗法律 - 需要新建分类
    "healthcare": "医疗法律",
    "legal": "医疗法律",
    "childcare": "医疗法律",
}

# Create missing categories
missing_cats = set(domain_categories.values()) - set(categories.keys())
print(f"\nMissing categories: {missing_cats}")

for cat_name in missing_cats:
    cat_info = {
        "身份证件": {"code": "identity", "name_en": "Identity"},
        "医疗法律": {"code": "healthcare_legal", "name_en": "Healthcare & Legal"},
    }.get(cat_name, {"code": cat_name.lower(), "name_en": cat_name})
    
    result = client.table("domain_categories").insert({
        "code": cat_info["code"],
        "name": cat_name,
        "name_en": cat_info["name_en"],
        "sort_order": len(categories) + 1,
    }).execute()
    categories[cat_name] = result.data[0]["id"]
    print(f"Created category: {cat_name} -> {result.data[0]['id']}")

# Update domains
print("\nUpdating domains...")
updated = 0
for code, cat_name in domain_categories.items():
    cat_id = categories.get(cat_name)
    if not cat_id:
        print(f"  Skip {code}: category {cat_name} not found")
        continue
    
    client.table("domains").update({"category_id": cat_id}).eq("code", code).execute()
    updated += 1

print(f"\nUpdated {updated} domains")
