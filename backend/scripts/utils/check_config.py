# 检查脚本 - 检查配置
from scripts.base import CheckScript


class CheckConfigScript(CheckScript):
    """检查配置"""

    NAME = "配置检查"
    DESCRIPTION = "检查环境变量和配置是否正确"

    def check(self) -> bool:
        """执行检查"""
        settings = self.get_settings()

        self.info("检查配置...")

        has_url = bool(settings.supabase_url)
        has_key = bool(settings.supabase_key)
        has_service_key = bool(settings.supabase_service_key)

        if has_url:
            self.info(f"URL: {settings.supabase_url[:30]}...")
        else:
            self.error("URL: NOT SET")

        if has_key:
            self.info(f"Key: {settings.supabase_key[:20]}...")
        else:
            self.error("Key: NOT SET")

        if has_service_key:
            self.info(f"Service Key: {settings.supabase_service_key[:20]}...")
        else:
            self.error("Service Key: NOT SET")

        return has_url and has_key and has_service_key


if __name__ == "__main__":
    script = CheckConfigScript()
    result = script.run()
    exit(0 if result.success else 1)
