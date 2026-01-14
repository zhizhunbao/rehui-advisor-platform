"""删除 llm_models 表的 region 列"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from src.common.supabase import get_supabase_admin

def main():
    client = get_supabase_admin()
    
    # 使用 RPC 执行 SQL
    # 注意：需要在 Supabase Dashboard 中执行此 SQL
    sql = "ALTER TABLE llm_models DROP COLUMN IF EXISTS region;"
    
    print("请在 Supabase Dashboard 的 SQL Editor 中执行以下 SQL:")
    print()
    print(sql)
    print()
    print("或者使用 Supabase CLI: supabase db execute --sql \"" + sql + "\"")

if __name__ == "__main__":
    main()
