# 检查领域和分类数据
from typing import Dict, List

from scripts.base import CheckScript


class CheckDomainsScript(CheckScript):
    """检查领域和分类数据"""

    NAME = "领域检查"
    DESCRIPTION = "检查数据库中的领域和分类数据"

    def check(self) -> bool:
        """执行检查"""
        client = self.get_supabase_client()

        cat_response = client.table("domain_categories").select("*").order("sort_order").execute()
        self.info(f"=== 领域分类 ({len(cat_response.data)}) ===")
        for c in cat_response.data:
            self.info(f"  - {c['id'][:8]}... : {c['name']} ({c.get('name_en', '')})")

        dom_response = client.table("domains").select("code, name, category_id").order("code").execute()
        self.info(f"\n=== 领域 ({len(dom_response.data)}) ===")

        by_cat: Dict[str, List[str]] = {}
        for d in dom_response.data:
            cat_id = d.get("category_id") or "uncategorized"
            if cat_id not in by_cat:
                by_cat[cat_id] = []
            by_cat[cat_id].append(d["code"])

        for cat_id, domains in by_cat.items():
            cat_name = next((c["name"] for c in cat_response.data if c["id"] == cat_id), "未分类")
            self.info(f"\n{cat_name} ({len(domains)}):")
            self.info(f"  {', '.join(domains)}")

        return len(cat_response.data) > 0 and len(dom_response.data) > 0


if __name__ == "__main__":
    script = CheckDomainsScript()
    result = script.run()
    exit(0 if result.success else 1)
