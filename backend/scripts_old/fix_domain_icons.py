"""Fix domain icons to use emoji instead of text"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from src.common.supabase import get_supabase_admin


def fix_icons():
    client = get_supabase_admin()
    
    # Domain category icons
    category_icons = {
        "travel": "✈️",
        "living": "🏠",
        "career": "💼",
        "finance": "💰",
        "education": "🎓",
    }
    
    # Domain icons
    domain_icons = {
        "flight": "✈️",
        "hotel": "🏨",
        "car_rental": "🚗",
        "housing": "🏠",
        "moving": "📦",
        "job": "💼",
        "resume": "📄",
        "investment": "📈",
        "insurance": "🛡️",
        "tax": "🧾",
        "school": "🎓",
        "language": "🗣️",
    }
    
    # Update domain categories
    print("Updating domain category icons...")
    for code, icon in category_icons.items():
        client.table("domain_categories").update({"icon": icon}).eq("code", code).execute()
        print(f"  {code}: {icon}")
    
    # Update domains
    print("\nUpdating domain icons...")
    for code, icon in domain_icons.items():
        client.table("domains").update({"icon": icon}).eq("code", code).execute()
        print(f"  {code}: {icon}")
    
    print("\nDone!")


if __name__ == "__main__":
    fix_icons()
