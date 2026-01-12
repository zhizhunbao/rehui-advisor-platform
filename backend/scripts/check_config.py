"""检查配置"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.common.config import get_settings

s = get_settings()
print(f"URL: {s.supabase_url[:30] if s.supabase_url else 'NOT SET'}...")
print(f"Key: {s.supabase_key[:20] if s.supabase_key else 'NOT SET'}...")
print(f"Service Key: {s.supabase_service_key[:20] if s.supabase_service_key else 'NOT SET'}...")
