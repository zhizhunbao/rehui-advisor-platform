"""检查 RLS 策略"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# 尝试直接用 SQL 查询
try:
    result = client.rpc("", {}).execute()
except Exception as e:
    print(f"RPC error: {e}")

# 尝试查询 llm_models
try:
    result = client.table("llm_models").select("*").execute()
    print(f"llm_models query success: {len(result.data)} rows")
except Exception as e:
    print(f"llm_models query error: {e}")

# 尝试查询 domain_categories（已知可以工作的表）
try:
    result = client.table("domain_categories").select("*").execute()
    print(f"domain_categories query success: {len(result.data)} rows")
except Exception as e:
    print(f"domain_categories query error: {e}")
