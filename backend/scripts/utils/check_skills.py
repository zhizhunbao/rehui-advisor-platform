# 检查 Skills 数据
from typing import Dict

from scripts.base import CheckScript


class CheckSkillsScript(CheckScript):
    """检查 Skills 数据"""

    NAME = "Skills 检查"
    DESCRIPTION = "检查数据库中的 Skills 数据"

    def check(self) -> bool:
        """执行检查"""
        client = self.get_supabase_client()

        response = client.table("skills").select("id, name, category, source", count="exact").limit(10).execute()

        self.info(f"总共 {response.count} 个 Skills")
        self.info("\n示例 Skills:")
        self.info("-" * 80)

        for s in response.data:
            name = s["name"][:40] if s["name"] else ""
            category = s["category"] or ""
            source = s["source"] or ""
            self.info(f"  {name:40} | {category:15} | {source}")

        cat_response = client.table("skills").select("category").execute()
        categories: Dict[str, int] = {}
        for s in cat_response.data:
            cat = s["category"] or "uncategorized"
            categories[cat] = categories.get(cat, 0) + 1

        self.info("\n分类分布:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            self.info(f"  {cat}: {count}")

        return response.count > 0


if __name__ == "__main__":
    script = CheckSkillsScript()
    result = script.run()
    exit(0 if result.success else 1)
