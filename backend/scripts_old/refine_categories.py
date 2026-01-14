"""Refine domain categories - split 生活服务 into more specific categories"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Get existing categories
cat_response = client.table("domain_categories").select("id, name").execute()
categories = {c["name"]: c["id"] for c in cat_response.data}
print("Current categories:", list(categories.keys()))

# New categories to create
NEW_CATEGORIES = [
    {"code": "daily_life", "name": "日常生活", "name_en": "Daily Life", "icon": "🏠", "sort_order": 10},
    {"code": "communication", "name": "通讯网络", "name_en": "Communication", "icon": "📱", "sort_order": 11},
    {"code": "food_shopping", "name": "餐饮购物", "name_en": "Food & Shopping", "icon": "🛒", "sort_order": 12},
    {"code": "leisure", "name": "休闲娱乐", "name_en": "Leisure", "icon": "🎬", "sort_order": 13},
    {"code": "home_services", "name": "家政服务", "name_en": "Home Services", "icon": "🔧", "sort_order": 14},
    {"code": "life_events", "name": "人生大事", "name_en": "Life Events", "icon": "💒", "sort_order": 15},
]

# Create new categories
for cat in NEW_CATEGORIES:
    if cat["name"] not in categories:
        result = client.table("domain_categories").insert(cat).execute()
        categories[cat["name"]] = result.data[0]["id"]
        print(f"Created: {cat['name']}")
    else:
        print(f"Exists: {cat['name']}")

# Domain to new category mapping
DOMAIN_CATEGORY_MAP = {
    # 日常生活 - 居住相关
    "housing": "日常生活",
    "moving": "日常生活",
    "utilities": "日常生活",
    "storage": "日常生活",
    
    # 通讯网络
    "phone": "通讯网络",
    "internet": "通讯网络",
    "shipping": "通讯网络",
    
    # 餐饮购物
    "shopping": "餐饮购物",
    "dining": "餐饮购物",
    "secondhand": "餐饮购物",
    
    # 休闲娱乐
    "fitness": "休闲娱乐",
    "entertainment": "休闲娱乐",
    "social": "休闲娱乐",
    "pet": "休闲娱乐",
    
    # 家政服务
    "cleaning": "家政服务",
    "repair": "家政服务",
    
    # 人生大事
    "wedding": "人生大事",
    "funeral": "人生大事",
}

# Update domains
print("\nUpdating domains...")
updated = 0
for code, cat_name in DOMAIN_CATEGORY_MAP.items():
    cat_id = categories.get(cat_name)
    if cat_id:
        client.table("domains").update({"category_id": cat_id}).eq("code", code).execute()
        print(f"  {code} -> {cat_name}")
        updated += 1

print(f"\nUpdated {updated} domains")

# Delete old 生活服务 category if empty
old_cat_id = categories.get("生活服务")
if old_cat_id:
    check = client.table("domains").select("id").eq("category_id", old_cat_id).execute()
    if not check.data:
        client.table("domain_categories").delete().eq("id", old_cat_id).execute()
        print("\nDeleted empty category: 生活服务")
    else:
        print(f"\n生活服务 still has {len(check.data)} domains")
