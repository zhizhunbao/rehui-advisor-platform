"""Reorder domain categories by priority"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Priority order (most important first)
CATEGORY_ORDER = [
    ("身份证件", 1),      # 新移民首要
    ("日常生活", 2),      # 居住基础
    ("金融理财", 3),      # 银行信用
    ("职业发展", 4),      # 求职
    ("出行旅游", 5),      # 出行
    ("通讯网络", 6),      # 手机网络
    ("医疗法律", 7),      # 医疗法律
    ("教育学习", 8),      # 教育
    ("餐饮购物", 9),      # 日常消费
    ("休闲娱乐", 10),     # 娱乐
    ("家政服务", 11),     # 家政
    ("人生大事", 12),     # 婚丧
]

print("Updating category sort order...")
for name, order in CATEGORY_ORDER:
    result = client.table("domain_categories").update({"sort_order": order}).eq("name", name).execute()
    if result.data:
        print(f"  {order}. {name}")

print("\nDone!")
