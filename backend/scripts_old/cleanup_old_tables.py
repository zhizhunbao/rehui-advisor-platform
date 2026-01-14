"""
清理旧表脚本 - 删除已迁移到 documents 表的旧表

运行方式: uv run python scripts/cleanup_old_tables.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common.supabase import get_supabase_admin


# 已迁移的旧表（数据已在 documents 表中）
OLD_TABLES = [
    # Admin 模块
    "system_configs",
    "skills",
    "skill_categories",
    "prompt_templates",
    "prompt_categories",
    "domains",
    "domain_categories",
    "questions",
    "llm_models",
    "data_sources",
    "subscription_plans",
    "admin_users",
    "scheduled_jobs",
    "job_executions",
    "chat_sessions",
    "chat_messages",
    "crawl_sources",
    "crawl_tasks",
    "recommendations",
    "retrieval_engines",
    "retrieval_domain_configs",
    # Member 模块
    "users",
    "cars",
    "houses",
    "jobs",
    "education",
    "investments",
    "flights",
    "hotels",
    "insurance_quotes",
    # 其他可能存在的表
    "system_logs",
]


def check_table_exists(client, table_name: str) -> tuple[bool, int]:
    """检查表是否存在并返回记录数"""
    try:
        response = client.table(table_name).select("id", count="exact").limit(0).execute()
        return True, response.count or 0
    except Exception:
        return False, 0


def drop_table(client, table_name: str) -> bool:
    """删除表（通过 RPC 调用）"""
    try:
        # Supabase 不直接支持 DROP TABLE，需要通过 SQL
        # 这里我们只是清空数据，实际删除表需要在 Supabase Dashboard 操作
        client.table(table_name).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        return True
    except Exception as e:
        print(f"  ❌ 清空失败: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="清理旧表")
    parser.add_argument("--dry-run", action="store_true", help="只检查，不执行删除")
    parser.add_argument("--delete-data", action="store_true", help="删除旧表中的数据")
    args = parser.parse_args()
    
    print("=" * 60)
    print("旧表清理脚本")
    print("=" * 60)
    
    if args.dry_run:
        print("🔍 DRY RUN 模式 - 只检查不删除")
    
    client = get_supabase_admin()
    
    # 先检查 documents 表
    try:
        doc_response = client.table("documents").select("id", count="exact").execute()
        doc_count = doc_response.count or 0
        print(f"\n✓ documents 表: {doc_count} 条记录")
    except Exception as e:
        print(f"\n❌ documents 表不存在: {e}")
        return
    
    print("\n检查旧表状态:")
    print("-" * 60)
    
    tables_with_data = []
    tables_empty = []
    tables_not_found = []
    
    for table in OLD_TABLES:
        exists, count = check_table_exists(client, table)
        if exists:
            if count > 0:
                tables_with_data.append((table, count))
                print(f"  {table}: {count} 条记录 ⚠️")
            else:
                tables_empty.append(table)
                print(f"  {table}: 空表")
        else:
            tables_not_found.append(table)
            print(f"  {table}: 不存在")
    
    print("\n" + "=" * 60)
    print("汇总:")
    print(f"  有数据的表: {len(tables_with_data)}")
    print(f"  空表: {len(tables_empty)}")
    print(f"  不存在: {len(tables_not_found)}")
    
    if tables_with_data:
        print("\n⚠️  以下表仍有数据:")
        for table, count in tables_with_data:
            print(f"    - {table}: {count} 条")
    
    if args.delete_data and not args.dry_run:
        print("\n" + "=" * 60)
        print("清空旧表数据...")
        
        for table, count in tables_with_data:
            print(f"\n清空 {table} ({count} 条)...")
            if drop_table(client, table):
                print(f"  ✓ 已清空")
        
        for table in tables_empty:
            # 空表不需要清空
            pass
        
        print("\n✓ 数据清空完成")
        print("\n提示: 要完全删除表结构，请在 Supabase Dashboard 中操作")
    else:
        print("\n提示:")
        print("  - 使用 --delete-data 清空旧表数据")
        print("  - 要删除表结构，请在 Supabase Dashboard 中操作")


if __name__ == "__main__":
    main()
