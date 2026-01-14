"""Align data source categories with domain categories"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Mapping from old data source categories to new domain categories
CATEGORY_MAPPING = {
    # 直接对应
    "education": "education",      # 教育学习
    
    # 需要映射
    "job": "career",               # 职业发展
    "investment": "finance",       # 金融理财
    "immigration": "identity",     # 身份证件
    "insurance": "finance",        # 金融理财 (保险属于金融)
    
    # 出行相关
    "car_rental": "travel",        # 出行旅游
    "hotel": "travel",             # 出行旅游
    
    # 住房
    "house": "home_services",      # 家政服务 (或者 life_events?)
    
    # 开发相关 - 可能不需要保留，或归类到其他
    "dev": None,                   # 开发工具 - 与北美生活无关
    "llm": None,                   # LLM模型 - 与北美生活无关
}

def show_mapping():
    """Show the proposed category mapping"""
    print("=" * 70)
    print("数据源分类 → 领域分类 映射方案")
    print("=" * 70)
    
    # Get current data sources
    response = client.table("data_sources").select("id, name, category, subcategory").execute()
    
    # Group by category
    by_category = {}
    for ds in response.data:
        cat = ds["category"] or "uncategorized"
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(ds)
    
    for old_cat, sources in sorted(by_category.items()):
        new_cat = CATEGORY_MAPPING.get(old_cat, "unknown")
        status = "✅" if new_cat else "❌ (建议删除或重新分类)"
        print(f"\n{old_cat} ({len(sources)}个) → {new_cat or 'N/A'} {status}")
        for s in sources[:5]:  # Show first 5
            print(f"  - {s['name'][:50]}")
        if len(sources) > 5:
            print(f"  ... 还有 {len(sources) - 5} 个")


def apply_mapping(dry_run: bool = True):
    """Apply the category mapping to data sources"""
    response = client.table("data_sources").select("id, name, category").execute()
    
    updates = []
    skipped = []
    
    for ds in response.data:
        old_cat = ds["category"]
        new_cat = CATEGORY_MAPPING.get(old_cat)
        
        if new_cat and new_cat != old_cat:
            updates.append({
                "id": ds["id"],
                "name": ds["name"],
                "old": old_cat,
                "new": new_cat
            })
        elif new_cat is None:
            skipped.append({
                "id": ds["id"],
                "name": ds["name"],
                "category": old_cat
            })
    
    print(f"\n需要更新: {len(updates)} 个")
    print(f"跳过 (dev/llm): {len(skipped)} 个")
    
    if dry_run:
        print("\n[DRY RUN] 以下数据源将被更新:")
        for u in updates:
            print(f"  {u['name'][:40]:40} {u['old']:15} → {u['new']}")
        print("\n运行 apply_mapping(dry_run=False) 来实际执行更新")
    else:
        for u in updates:
            client.table("data_sources").update({"category": u["new"]}).eq("id", u["id"]).execute()
            print(f"  ✅ {u['name'][:40]} → {u['new']}")
        print(f"\n已更新 {len(updates)} 个数据源")


if __name__ == "__main__":
    show_mapping()
    print("\n" + "=" * 70)
    apply_mapping(dry_run=False)  # 执行更新
