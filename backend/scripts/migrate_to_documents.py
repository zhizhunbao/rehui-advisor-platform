"""
数据迁移脚本 - 将旧表数据迁移到 documents 表

运行方式: uv run python scripts/migrate_to_documents.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from uuid import uuid4

from src.common.supabase import get_supabase_admin


# 迁移映射配置
MIGRATIONS = [
    {
        "name": "system_configs",
        "source_table": "system_configs",
        "doc_type": "admin_config",
        "field_mapping": {
            "key": "key",
            "value": "value",
            "description": "description",
            "category": "category",
            "is_sensitive": "is_sensitive",
        },
    },
    {
        "name": "skills",
        "source_table": "skills",
        "doc_type": "admin_skill",
        "field_mapping": {
            "name": "name",
            "description": "description",
            "category": "category",
            "source": "source",
            "url": "url",
            "icon": "icon",
            "metadata": "metadata",
            "is_active": "is_active",
        },
    },
    {
        "name": "skill_categories",
        "source_table": "skill_categories",
        "doc_type": "admin_skill_label",
        "field_mapping": {
            "type": "type",
            "code": "code",
            "name_zh": "name_zh",
            "name_en": "name_en",
            "description": "description",
            "icon": "icon",
            "sort_order": "sort_order",
        },
    },
    {
        "name": "prompts",
        "source_table": "prompt_templates",
        "doc_type": "admin_prompt",
        "field_mapping": {
            "name": "name",
            "description": "description",
            "content": "content",
            "category": "category",
            "source": "source",
            "url": "url",
            "variables": "variables",
            "metadata": "metadata",
            "is_active": "is_active",
        },
    },
    {
        "name": "prompt_categories",
        "source_table": "prompt_categories",
        "doc_type": "admin_prompt_label",
        "field_mapping": {
            "type": "type",
            "code": "code",
            "name_zh": "name_zh",
            "name_en": "name_en",
            "description": "description",
            "icon": "icon",
            "sort_order": "sort_order",
        },
    },
    {
        "name": "domains",
        "source_table": "domains",
        "doc_type": "admin_domain",
        "field_mapping": {
            "code": "code",
            "name_zh": "name_zh",
            "name_en": "name_en",
            "description": "description",
            "icon": "icon",
            "category_id": "category_id",
            "config": "config",
            "is_active": "is_active",
            "sort_order": "sort_order",
        },
    },
    {
        "name": "domain_categories",
        "source_table": "domain_categories",
        "doc_type": "admin_domain_category",
        "field_mapping": {
            "code": "code",
            "name": "name",
            "name_en": "name_en",
            "description": "description",
            "description_en": "description_en",
            "icon": "icon",
            "color": "color",
            "sort_order": "sort_order",
            "is_active": "is_active",
        },
    },
    {
        "name": "questions",
        "source_table": "questions",
        "doc_type": "admin_question",
        "field_mapping": {
            "domain_id": "domain_id",
            "text": "text",
            "text_en": "text_en",
            "type": "type",
            "options": "options",
            "sort_order": "sort_order",
            "is_active": "is_active",
        },
    },
    {
        "name": "llm_models",
        "source_table": "llm_models",
        "doc_type": "admin_llm_model",
        "field_mapping": {
            "provider": "provider",
            "model_id": "model_id",
            "name": "name",
            "description": "description",
            "config": "config",
            "is_active": "is_active",
            "is_default": "is_default",
        },
    },
    {
        "name": "data_sources",
        "source_table": "data_sources",
        "doc_type": "admin_data_source",
        "field_mapping": {
            "url": "url",
            "name": "name",
            "description": "description",
            "category_id": "category_id",
            "domain_id": "domain_id",
            "source_type": "source_type",
            "metadata": "metadata",
            "crawl_config": "crawl_config",
            "last_crawled_at": "last_crawled_at",
            "crawl_status": "crawl_status",
            "is_active": "is_active",
        },
    },
    {
        "name": "subscription_plans",
        "source_table": "subscription_plans",
        "doc_type": "admin_subscription",
        "field_mapping": {
            "name": "name",
            "description": "description",
            "price": "price",
            "currency": "currency",
            "interval": "interval",
            "features": "features",
            "limits": "limits",
            "is_active": "is_active",
            "sort_order": "sort_order",
        },
    },
    {
        "name": "admin_users",
        "source_table": "admin_users",
        "doc_type": "admin_user",
        "field_mapping": {
            "username": "username",
            "email": "email",
            "password_hash": "password_hash",
            "name": "name",
            "role": "role",
            "is_active": "is_active",
            "last_login_at": "last_login_at",
        },
    },
    {
        "name": "scheduled_jobs",
        "source_table": "scheduled_jobs",
        "doc_type": "admin_scheduled_job",
        "field_mapping": {
            "name": "name",
            "description": "description",
            "job_type": "job_type",
            "cron_expression": "cron_expression",
            "parameters": "parameters",
            "is_active": "is_active",
            "last_run_at": "last_run_at",
            "last_status": "last_status",
        },
    },
    {
        "name": "job_executions",
        "source_table": "job_executions",
        "doc_type": "admin_job_execution",
        "field_mapping": {
            "job_id": "job_id",
            "started_at": "started_at",
            "finished_at": "finished_at",
            "status": "status",
            "result": "result",
            "error_message": "error_message",
        },
    },
    {
        "name": "chat_sessions",
        "source_table": "chat_sessions",
        "doc_type": "admin_chat_session",
        "field_mapping": {
            "user_id": "user_id",
            "domain": "domain",
            "title": "title",
            "metadata": "metadata",
        },
        "owner_id_field": "user_id",
    },
    {
        "name": "chat_messages",
        "source_table": "chat_messages",
        "doc_type": "admin_chat_message",
        "field_mapping": {
            "session_id": "session_id",
            "role": "role",
            "content": "content",
            "metadata": "metadata",
        },
    },
    {
        "name": "crawl_sources",
        "source_table": "crawl_sources",
        "doc_type": "admin_crawl_source",
        "field_mapping": {
            "name": "name",
            "url": "url",
            "domain_id": "domain_id",
            "crawl_type": "crawl_type",
            "config": "config",
            "is_active": "is_active",
            "last_run_at": "last_run_at",
            "last_status": "last_status",
        },
    },
    {
        "name": "crawl_tasks",
        "source_table": "crawl_tasks",
        "doc_type": "admin_crawl_task",
        "field_mapping": {
            "source_id": "source_id",
            "status": "status",
            "started_at": "started_at",
            "finished_at": "finished_at",
            "records_count": "records_count",
            "error_message": "error_message",
        },
    },
    {
        "name": "recommendations",
        "source_table": "recommendations",
        "doc_type": "admin_recommendation",
        "field_mapping": {
            "user_id": "user_id",
            "domain": "domain",
            "title": "title",
            "content": "content",
            "ranking": "ranking",
            "score": "score",
            "metadata": "metadata",
        },
        "owner_id_field": "user_id",
    },
    {
        "name": "retrieval_engines",
        "source_table": "retrieval_engines",
        "doc_type": "admin_retrieval_engine",
        "field_mapping": {
            "name": "name",
            "display_name": "display_name",
            "type": "type",
            "description": "description",
            "config": "config",
            "is_active": "is_active",
            "is_default": "is_default",
        },
    },
    {
        "name": "retrieval_domain_configs",
        "source_table": "retrieval_domain_configs",
        "doc_type": "admin_retrieval_domain_config",
        "field_mapping": {
            "domain": "domain",
            "engine_id": "engine_id",
        },
    },
    # ========== Member 模块 ==========
    {
        "name": "users",
        "source_table": "users",
        "doc_type": "member_user",
        "field_mapping": {
            "email": "email",
            "password_hash": "password_hash",
            "name": "name",
            "user_type": "user_type",
            "is_anonymous": "is_anonymous",
            "session_token": "session_token",
            "ip_address": "ip_address",
            "search_limit": "search_limit",
            "search_count": "search_count",
            "last_search_at": "last_search_at",
            "quota_reset_at": "quota_reset_at",
        },
    },
    {
        "name": "cars",
        "source_table": "cars",
        "doc_type": "member_car",
        "field_mapping": {
            "make": "make",
            "model": "model",
            "year": "year",
            "condition": "condition",
            "mileage": "mileage",
            "price": "price",
            "currency": "currency",
            "color": "color",
            "transmission": "transmission",
            "fuel_type": "fuel_type",
            "features": "features",
        },
    },
    {
        "name": "houses",
        "source_table": "houses",
        "doc_type": "member_house",
        "field_mapping": {
            "listing_type": "listing_type",
            "property_type": "property_type",
            "city": "city",
            "state": "state",
            "price": "price",
            "currency": "currency",
            "bedrooms": "bedrooms",
            "bathrooms": "bathrooms",
            "square_feet": "square_feet",
            "year_built": "year_built",
            "features": "features",
        },
    },
    {
        "name": "jobs",
        "source_table": "jobs",
        "doc_type": "member_job",
        "field_mapping": {
            "title": "title",
            "company": "company",
            "city": "city",
            "state": "state",
            "job_type": "job_type",
            "salary_min": "salary_min",
            "salary_max": "salary_max",
            "currency": "currency",
            "description": "description",
            "requirements": "requirements",
            "benefits": "benefits",
        },
    },
    {
        "name": "educations",
        "source_table": "educations",
        "doc_type": "member_education",
        "field_mapping": {
            "institution": "institution",
            "program": "program",
            "degree": "degree",
            "major": "major",
            "city": "city",
            "state": "state",
            "country": "country",
            "tuition": "tuition",
            "currency": "currency",
            "duration": "duration",
            "overall_ranking": "overall_ranking",
            "program_ranking": "program_ranking",
            "admission_rate": "admission_rate",
            "employment_rate": "employment_rate",
        },
    },
    {
        "name": "investments",
        "source_table": "investments",
        "doc_type": "member_investment",
        "field_mapping": {
            "product_name": "product_name",
            "type": "type",
            "ticker": "ticker",
            "current_price": "current_price",
            "currency": "currency",
            "risk_level": "risk_level",
            "minimum_investment": "minimum_investment",
            "provider": "provider",
            "description": "description",
            "sector": "sector",
            "dividend_yield": "dividend_yield",
        },
    },
    {
        "name": "flights",
        "source_table": "flights",
        "doc_type": "member_flight",
        "field_mapping": {
            "airline": "airline",
            "flight_number": "flight_number",
            "departure_code": "departure_code",
            "departure_name": "departure_name",
            "departure_city": "departure_city",
            "departure_time": "departure_time",
            "arrival_code": "arrival_code",
            "arrival_name": "arrival_name",
            "arrival_city": "arrival_city",
            "arrival_time": "arrival_time",
            "duration": "duration",
            "stops": "stops",
            "price": "price",
            "currency": "currency",
            "cabin_class": "cabin_class",
            "available_seats": "available_seats",
        },
    },
    {
        "name": "hotels",
        "source_table": "hotels",
        "doc_type": "member_hotel",
        "field_mapping": {
            "name": "name",
            "city": "city",
            "state": "state",
            "country": "country",
            "rating": "rating",
            "review_score": "review_score",
            "price_per_night": "price_per_night",
            "currency": "currency",
            "amenities": "amenities",
        },
    },
    {
        "name": "insurance_quotes",
        "source_table": "insurance_quotes",
        "doc_type": "member_insurance_quote",
        "field_mapping": {
            "user_id": "user_id",
            "session_token": "session_token",
            "insurance_type": "insurance_type",
            "request_data": "request_data",
            "zip_code": "zip_code",
            "quotes": "quotes",
            "status": "status",
            "expires_at": "expires_at",
        },
        "owner_id_field": "user_id",
    },
    {
        "name": "member_recommendations",
        "source_table": "member_recommendations",
        "doc_type": "member_recommendation",
        "field_mapping": {
            "user_id": "user_id",
            "domain": "domain",
            "item_id": "item_id",
            "match_score": "match_score",
            "ranking": "ranking",
            "pros": "pros",
            "cons": "cons",
            "reasoning": "reasoning",
        },
        "owner_id_field": "user_id",
    },
]


def migrate_table(client, migration: dict, dry_run: bool = False, force: bool = False) -> dict:
    """迁移单个表"""
    name = migration["name"]
    source_table = migration["source_table"]
    doc_type = migration["doc_type"]
    field_mapping = migration["field_mapping"]
    owner_id_field = migration.get("owner_id_field")
    
    print(f"\n{'='*50}")
    print(f"迁移: {name}")
    print(f"源表: {source_table} -> 文档类型: {doc_type}")
    
    # 检查源表是否存在
    try:
        response = client.table(source_table).select("*", count="exact").limit(0).execute()
        total_count = response.count or 0
        print(f"源表记录数: {total_count}")
    except Exception as e:
        print(f"⚠️  源表 {source_table} 不存在或无法访问: {e}")
        return {"name": name, "status": "skipped", "reason": "table not found"}
    
    if total_count == 0:
        print(f"✓ 源表为空，跳过")
        return {"name": name, "status": "skipped", "reason": "empty table"}
    
    # 检查是否已迁移
    existing = client.table("documents").select("id", count="exact").eq("type", doc_type).execute()
    existing_count = existing.count or 0
    if existing_count > 0:
        if force:
            print(f"⚠️  目标已有 {existing_count} 条记录，强制清除...")
            if not dry_run:
                client.table("documents").delete().eq("type", doc_type).execute()
                print(f"✓ 已清除 {existing_count} 条记录")
        else:
            print(f"⚠️  目标已有 {existing_count} 条记录，跳过（使用 --force 强制迁移）")
            return {"name": name, "status": "skipped", "reason": f"already has {existing_count} records"}
    
    # 读取源数据（分页读取所有数据）
    all_source_data = []
    page_size = 1000
    offset = 0
    
    while True:
        response = client.table(source_table).select("*").range(offset, offset + page_size - 1).execute()
        batch = response.data or []
        if not batch:
            break
        all_source_data.extend(batch)
        if len(batch) < page_size:
            break
        offset += page_size
    
    source_data = all_source_data
    
    # 转换数据
    documents = []
    for row in source_data:
        # 构建 data 字段
        data = {}
        for source_field, target_field in field_mapping.items():
            if source_field in row:
                data[target_field] = row[source_field]
        
        # 构建文档
        doc = {
            "id": row.get("id") or str(uuid4()),
            "type": doc_type,
            "data": data,
            "owner_id": row.get(owner_id_field) if owner_id_field else None,
            "status": "active",
            "tags": [],
            "created_at": row.get("created_at") or datetime.now(timezone.utc).isoformat(),
            "updated_at": row.get("updated_at") or datetime.now(timezone.utc).isoformat(),
        }
        documents.append(doc)
    
    print(f"准备迁移 {len(documents)} 条记录")
    
    if dry_run:
        print("🔍 DRY RUN - 不执行实际迁移")
        if documents:
            print(f"示例文档: {documents[0]}")
        return {"name": name, "status": "dry_run", "count": len(documents)}
    
    # 批量插入
    if documents:
        # 分批插入，每批 100 条
        batch_size = 100
        inserted = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            try:
                client.table("documents").insert(batch).execute()
                inserted += len(batch)
                print(f"  已插入: {inserted}/{len(documents)}")
            except Exception as e:
                print(f"❌ 插入失败: {e}")
                return {"name": name, "status": "error", "error": str(e), "inserted": inserted}
    
    print(f"✓ 迁移完成: {len(documents)} 条记录")
    return {"name": name, "status": "success", "count": len(documents)}


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="迁移数据到 documents 表")
    parser.add_argument("--dry-run", action="store_true", help="只检查，不执行迁移")
    parser.add_argument("--table", type=str, help="只迁移指定的表")
    parser.add_argument("--force", action="store_true", help="强制迁移（清除已有数据）")
    args = parser.parse_args()
    
    print("=" * 60)
    print("数据迁移脚本 - 旧表 -> documents 表")
    print("=" * 60)
    
    client = get_supabase_admin()
    
    # 检查 documents 表
    try:
        client.table("documents").select("id").limit(1).execute()
        print("✓ documents 表已就绪")
    except Exception as e:
        print(f"❌ documents 表不存在: {e}")
        print("请先运行 alembic 迁移创建 documents 表")
        return
    
    results = []
    migrations_to_run = MIGRATIONS
    
    if args.table:
        migrations_to_run = [m for m in MIGRATIONS if m["name"] == args.table]
        if not migrations_to_run:
            print(f"❌ 未找到表: {args.table}")
            print(f"可用的表: {[m['name'] for m in MIGRATIONS]}")
            return
    
    for migration in migrations_to_run:
        result = migrate_table(client, migration, dry_run=args.dry_run, force=args.force)
        results.append(result)
    
    # 汇总
    print("\n" + "=" * 60)
    print("迁移汇总")
    print("=" * 60)
    
    success = [r for r in results if r["status"] == "success"]
    skipped = [r for r in results if r["status"] == "skipped"]
    errors = [r for r in results if r["status"] == "error"]
    
    print(f"成功: {len(success)}")
    for r in success:
        print(f"  - {r['name']}: {r.get('count', 0)} 条")
    
    print(f"跳过: {len(skipped)}")
    for r in skipped:
        print(f"  - {r['name']}: {r.get('reason', '')}")
    
    if errors:
        print(f"失败: {len(errors)}")
        for r in errors:
            print(f"  - {r['name']}: {r.get('error', '')}")


if __name__ == "__main__":
    main()
