# 迁移脚本 - 修复领域图标为 emoji
from typing import Dict

from scripts.base import MigrateScript


CATEGORY_ICONS: Dict[str, str] = {
    "travel": "✈️",
    "living": "🏠",
    "career": "💼",
    "finance": "💰",
    "education": "🎓",
}

DOMAIN_ICONS: Dict[str, str] = {
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


class FixDomainIconsScript(MigrateScript):
    """修复领域图标为 emoji"""

    NAME = "修复领域图标"
    DESCRIPTION = "将领域图标从文本更新为 emoji"

    def migrate(self) -> int:
        """执行迁移"""
        client = self.get_supabase_client()
        affected = 0

        self.info("更新领域分类图标...")
        for code, icon in CATEGORY_ICONS.items():
            client.table("domain_categories").update({"icon": icon}).eq("code", code).execute()
            self.info(f"  {code}: {icon}")
            affected += 1

        self.info("更新领域图标...")
        for code, icon in DOMAIN_ICONS.items():
            client.table("domains").update({"icon": icon}).eq("code", code).execute()
            self.info(f"  {code}: {icon}")
            affected += 1

        return affected


if __name__ == "__main__":
    script = FixDomainIconsScript()
    result = script.run()
    exit(0 if result.success else 1)
