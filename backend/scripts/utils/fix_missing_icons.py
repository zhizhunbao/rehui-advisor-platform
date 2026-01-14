# 迁移脚本 - 修复缺失的领域图标
from typing import Dict

from scripts.base import MigrateScript


ICONS: Dict[str, str] = {
    "dev_tools": "🛠️",
    "ai_ml": "🤖",
    "llm": "🧠",
    "devops": "☁️",
    "prompts": "💬",
    "benefits": "🏛️",
    "employment_insurance": "💼",
    "pension": "👴",
    "child_benefits": "👶",
    "housing_subsidy": "🏠",
    "healthcare_benefits": "🏥",
    "newcomer_services": "🌟",
    "disability_benefits": "♿",
    "social_assistance": "🤝",
}


class FixMissingIconsScript(MigrateScript):
    """修复缺失的领域图标"""

    NAME = "修复缺失图标"
    DESCRIPTION = "为缺少图标的领域添加 emoji 图标"

    def migrate(self) -> int:
        """执行迁移"""
        client = self.get_supabase_client()
        affected = 0

        response = client.table("domains").select("code, name, icon").execute()
        missing = [d for d in response.data if not d.get("icon")]
        self.info(f"缺少 icon 的 domains ({len(missing)}):")
        for d in missing:
            self.info(f"  {d['code']}: {d['name']}")

        self.info("\n更新 icons:")
        for code, icon in ICONS.items():
            result = client.table("domains").update({"icon": icon}).eq("code", code).execute()
            if result.data:
                self.info(f"  {icon} {code}")
                affected += 1

        return affected


if __name__ == "__main__":
    script = FixMissingIconsScript()
    result = script.run()
    exit(0 if result.success else 1)
