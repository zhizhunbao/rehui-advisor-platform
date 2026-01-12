"""
Migrate data_sources to use domain_categories and domains foreign keys

Steps:
1. Add category_id and domain_id columns to data_sources
2. Migrate existing category/subcategory data to new columns
3. (Optional) Remove old category/subcategory columns

Run this SQL in Supabase Dashboard first:
"""

MIGRATION_SQL = """
-- Step 1: Add new columns
ALTER TABLE data_sources 
ADD COLUMN IF NOT EXISTS category_id UUID REFERENCES domain_categories(id),
ADD COLUMN IF NOT EXISTS domain_id UUID REFERENCES domains(id);

-- Step 2: Create indexes
CREATE INDEX IF NOT EXISTS idx_data_sources_category_id ON data_sources(category_id);
CREATE INDEX IF NOT EXISTS idx_data_sources_domain_id ON data_sources(domain_id);
"""

from src.common.supabase import get_supabase_admin

client = get_supabase_admin()


def get_category_id(code: str) -> str | None:
    """Get category_id by code"""
    response = client.table("domain_categories").select("id").eq("code", code).maybe_single().execute()
    return response.data["id"] if response.data else None


def get_domain_id(code: str) -> str | None:
    """Get domain_id by code"""
    response = client.table("domains").select("id").eq("code", code).maybe_single().execute()
    return response.data["id"] if response.data else None


# Category mapping (old string -> domain_categories.code)
CATEGORY_MAP = {
    "career": "career",
    "finance": "finance",
    "travel": "travel",
    "identity": "identity",
    "home_services": "home_services",
    "education": "education",
    "dev": None,  # 保留，不关联
    "llm": None,  # 保留，不关联
}

# Subcategory mapping (old string -> domains.code)
SUBCATEGORY_MAP = {
    # career
    "interview": "job",
    "job_board": "job",
    "remote": "job",
    "visa_sponsorship": "job",
    # finance
    "crypto": "investment",
    "general": None,  # 太通用，不映射
    "personal_finance": "investment",
    "tools": None,
    "trading": "investment",
    "health": "insurance",
    # travel
    "api": "travel",
    "booking": "hotel",
    "automotive": "car_rental",
    "data": "car_rental",
    "security": "car_rental",
    # identity
    "h1b": "visa",
    "visa": "visa",
    # home_services
    "rental": "housing",  # 租房应该是 daily_life.housing
    # education
    "books": "school",
    "coding": "tutoring",
    "cs": "school",
    "online_course": "tutoring",
    "resources": "school",
    "roadmap": "school",
}


def migrate_data(dry_run: bool = True):
    """Migrate category/subcategory to category_id/domain_id"""
    print("=" * 70)
    print("迁移数据源分类到外键关联")
    print("=" * 70)
    
    # Get all data sources
    response = client.table("data_sources").select("id, name, category, subcategory").execute()
    
    updates = []
    skipped = []
    
    for ds in response.data:
        old_cat = ds["category"]
        old_sub = ds["subcategory"]
        
        # Map category
        new_cat_code = CATEGORY_MAP.get(old_cat)
        category_id = get_category_id(new_cat_code) if new_cat_code else None
        
        # Map subcategory to domain
        new_domain_code = SUBCATEGORY_MAP.get(old_sub)
        domain_id = get_domain_id(new_domain_code) if new_domain_code else None
        
        if category_id or domain_id:
            updates.append({
                "id": ds["id"],
                "name": ds["name"],
                "old_cat": old_cat,
                "old_sub": old_sub,
                "category_id": category_id,
                "domain_id": domain_id,
                "new_cat_code": new_cat_code,
                "new_domain_code": new_domain_code,
            })
        else:
            skipped.append(ds)
    
    print(f"\n需要更新: {len(updates)} 个")
    print(f"跳过 (dev/llm): {len(skipped)} 个")
    
    if dry_run:
        print("\n[DRY RUN] 以下数据源将被更新:")
        for u in updates:
            cat_info = f"category_id={u['new_cat_code']}" if u['category_id'] else ""
            domain_info = f"domain_id={u['new_domain_code']}" if u['domain_id'] else ""
            print(f"  {u['name'][:35]:35} {cat_info:20} {domain_info}")
        print("\n运行 migrate_data(dry_run=False) 来实际执行更新")
    else:
        for u in updates:
            update_data = {}
            if u["category_id"]:
                update_data["category_id"] = u["category_id"]
            if u["domain_id"]:
                update_data["domain_id"] = u["domain_id"]
            
            if update_data:
                client.table("data_sources").update(update_data).eq("id", u["id"]).execute()
                print(f"  ✅ {u['name'][:40]}")
        
        print(f"\n已更新 {len(updates)} 个数据源")


if __name__ == "__main__":
    migrate_data(dry_run=False)
