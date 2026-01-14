# 迁移脚本 - 重新排序领域分类
from typing import List, Tuple

from scripts.base import MigrateScript


CATEGORY_ORDER: List[Tuple[str, int]] = [
    ("身份证件", 1),
    ("日常生活", 2),
    ("金融理财", 3),
    ("职业发展", 4),
    ("出行旅游", 5),
    ("通讯网络", 6),
    ("医疗法律", 7),
    ("教育学习", 8),
    ("餐饮购物", 9),
    ("休闲娱乐", 10),
    ("家政服务", 11),
    ("人生大事", 12),
]


class ReorderCategoriesScript(MigrateScript):
    """重新排序领域分类"""

    NAME = "重排分类顺序"
    DESCRIPTION = "按优先级重新排序领域分类"

    def migrate(self) -> int:
        """执行迁移"""
        client = self.get_supabase_client()
        affected = 0

        self.info("更新分类排序...")
        for name, order in CATEGORY_ORDER:
            result = client.table("domain_categories").update({"sort_order": order}).eq("name", name).execute()
            if result.data:
                self.info(f"  {order}. {name}")
                affected += 1

        return affected


if __name__ == "__main__":
    script = ReorderCategoriesScript()
    result = script.run()
    exit(0 if result.success else 1)
