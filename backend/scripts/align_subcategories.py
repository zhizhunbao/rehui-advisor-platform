"""Align data source subcategories with domain codes"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# 子分类映射: 旧subcategory -> 新subcategory (domain code)
SUBCATEGORY_MAPPING = {
    # career 分类
    "career": {
        "interview": "job",        # 面试 -> 求职
        "job_board": "job",        # 招聘网站 -> 求职
        "remote": "job",           # 远程工作 -> 求职
        "visa_sponsorship": "job", # 签证担保 -> 求职
    },
    # finance 分类
    "finance": {
        "crypto": "investment",        # 加密货币 -> 投资理财
        "general": "investment",       # 通用 -> 投资理财
        "personal_finance": "investment",  # 个人理财 -> 投资理财
        "tools": "investment",         # 工具 -> 投资理财
        "trading": "investment",       # 交易 -> 投资理财
        "health": "insurance",         # 健康 -> 保险
    },
    # travel 分类
    "travel": {
        "api": "travel",           # API -> 旅行规划
        "booking": "hotel",        # 预订 -> 酒店住宿
        "automotive": "car_rental",  # 汽车 -> 租车自驾
        "data": "car_rental",      # 数据 -> 租车自驾
        "security": "car_rental",  # 安全 -> 租车自驾
    },
    # identity 分类
    "identity": {
        "h1b": "visa",             # H1B -> 签证身份
        "visa": "visa",            # 签证 -> 签证身份
    },
    # home_services 分类
    "home_services": {
        "general": "repair",       # 通用 -> 家电维修
        "rental": "repair",        # 租房 -> 家电维修 (或者应该是 housing?)
    },
    # education 分类
    "education": {
        "books": "school",         # 书籍 -> 学校申请
        "coding": "tutoring",      # 编程 -> 课外辅导
        "cs": "school",            # 计算机科学 -> 学校申请
        "online_course": "tutoring",  # 在线课程 -> 课外辅导
        "resources": "school",     # 资源 -> 学校申请
        "roadmap": "school",       # 路线图 -> 学校申请
    },
    # dev/llm 保持不变
    "dev": {},
    "llm": {},
}


def show_mapping():
    """Show the proposed subcategory mapping"""
    print("=" * 70)
    print("数据源子分类 → 领域代码 映射方案")
    print("=" * 70)
    
    response = client.table("data_sources").select("id, name, category, subcategory").execute()
    
    updates = []
    unchanged = []
    
    for ds in response.data:
        cat = ds["category"]
        old_sub = ds["subcategory"]
        
        if cat in SUBCATEGORY_MAPPING and old_sub in SUBCATEGORY_MAPPING[cat]:
            new_sub = SUBCATEGORY_MAPPING[cat][old_sub]
            if new_sub != old_sub:
                updates.append({
                    "id": ds["id"],
                    "name": ds["name"],
                    "category": cat,
                    "old": old_sub,
                    "new": new_sub
                })
            else:
                unchanged.append(ds)
        else:
            unchanged.append(ds)
    
    # Group by category
    by_cat = {}
    for u in updates:
        cat = u["category"]
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(u)
    
    for cat, items in sorted(by_cat.items()):
        print(f"\n{cat}:")
        for item in items:
            print(f"  {item['name'][:35]:35} {item['old']:20} → {item['new']}")
    
    return updates


def apply_mapping(dry_run: bool = True):
    """Apply the subcategory mapping"""
    updates = show_mapping()
    
    print(f"\n需要更新: {len(updates)} 个")
    
    if dry_run:
        print("\n[DRY RUN] 运行 apply_mapping(dry_run=False) 来实际执行更新")
    else:
        for u in updates:
            client.table("data_sources").update({"subcategory": u["new"]}).eq("id", u["id"]).execute()
            print(f"  ✅ {u['name'][:40]} → {u['new']}")
        print(f"\n已更新 {len(updates)} 个数据源子分类")


if __name__ == "__main__":
    apply_mapping(dry_run=True)
