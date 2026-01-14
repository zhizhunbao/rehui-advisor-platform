# 检查 Prompt 模板数据
from scripts.base import CheckScript


class CheckPromptsScript(CheckScript):
    """检查 Prompt 模板数据"""

    NAME = "Prompt 检查"
    DESCRIPTION = "检查数据库中的 Prompt 模板"

    def check(self) -> bool:
        """执行检查"""
        client = self.get_supabase_client()

        response = client.table("prompt_templates").select("name, description, template, category").execute()

        long_prompts = [p for p in response.data if len(p.get("template") or "") > 1000]
        self.info(f"找到 {len(long_prompts)} 个长度超过 1000 字符的 Prompt")

        for p in long_prompts[:3]:
            self.info(f"\n{'='*60}")
            self.info(f"NAME: {p['name']} ({p['category']})")
            self.info(f"DESC: {p['description'][:100]}...")
            self.info(f"\nTEMPLATE ({len(p['template'])} chars):")
            self.info(p['template'][:500] + "...")

        return len(response.data) > 0


if __name__ == "__main__":
    script = CheckPromptsScript()
    result = script.run()
    exit(0 if result.success else 1)
