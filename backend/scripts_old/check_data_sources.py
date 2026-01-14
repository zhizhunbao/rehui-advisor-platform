"""检查数据源相关的数据库数据"""
import sys
sys.path.insert(0, ".")

from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# 1. 检查 domain_categories 表
print("=" * 50)
print("1. domain_categories 表:")
categories = client.table("domain_categories").select("id, code, name, name_en").limit(20).execute()
print(f"   总数: {len(categories.data)}")
for cat in categories.data[:5]:
    print(f"   - {cat['code']}: {cat['name']} ({cat.get('name_en', '')})")
if len(categories.data) > 5:
    print(f"   ... 还有 {len(categories.data) - 5} 条")

# 2. 检查 data_sources 表的 category_id 字段
print("\n" + "=" * 50)
print("2. data_sources 表 category_id 分布:")
ds_with_cat_id = client.table("data_sources").select("category_id").not_.is_("category_id", "null").execute()
print(f"   有 category_id 的数据源: {len(ds_with_cat_id.data)}")

# 统计每个 category_id 的数量
cat_id_counts = {}
for ds in ds_with_cat_id.data:
    cat_id = ds.get("category_id")
    if cat_id:
        cat_id_counts[cat_id] = cat_id_counts.get(cat_id, 0) + 1
print(f"   不同的 category_id 数量: {len(cat_id_counts)}")
for cat_id, count in list(cat_id_counts.items())[:5]:
    print(f"   - {cat_id}: {count}")

# 3. 检查 data_sources 表的 domain_id 字段
print("\n" + "=" * 50)
print("3. data_sources 表 domain_id 分布:")
ds_with_domain_id = client.table("data_sources").select("domain_id").not_.is_("domain_id", "null").execute()
print(f"   有 domain_id 的数据源: {len(ds_with_domain_id.data)}")

# 4. 检查 domains 表
print("\n" + "=" * 50)
print("4. domains 表:")
domains = client.table("domains").select("id, code, name, category_id").limit(20).execute()
print(f"   总数: {len(domains.data)}")
for d in domains.data[:5]:
    print(f"   - {d['code']}: {d['name']} (category_id: {d.get('category_id', 'N/A')})")

# 5. 检查 data_sources 总数
print("\n" + "=" * 50)
print("5. data_sources 表总数:")
total = client.table("data_sources").select("id", count="exact").execute()
print(f"   总数: {total.count}")

# 6. 调用 API 检查返回的 categories
print("\n" + "=" * 50)
print("6. 模拟 get_categories API 返回:")
from src.modules.data_source.service import DataSourceService
service = DataSourceService()
api_categories = service.get_categories()
print(f"   返回的分类数: {len(api_categories)}")
for cat in api_categories[:5]:
    print(f"   - {cat['code']}: {cat['name']} (count: {cat['count']}, id: {cat['id']})")
if len(api_categories) > 5:
    print(f"   ... 还有 {len(api_categories) - 5} 条")
