# LLM API Key 申请助手
import asyncio
from pathlib import Path
from typing import Any
from playwright.async_api import async_playwright, Browser, Page

PROVIDER_CONFIGS: dict[str, dict[str, Any]] = {
    "github": {"name": "GitHub Models", "url": "https://github.com/settings/tokens", "env_key": "GITHUB_TOKEN", "free_tier": "免费GPT-4o/Claude"},
    "groq": {"name": "Groq", "url": "https://console.groq.com/keys", "env_key": "GROQ_API_KEY", "free_tier": "完全免费"},
    "gemini": {"name": "Gemini", "url": "https://aistudio.google.com/apikey", "env_key": "GEMINI_API_KEY", "free_tier": "1M tokens/day"},
    "cerebras": {"name": "Cerebras", "url": "https://cloud.cerebras.ai/", "env_key": "CEREBRAS_API_KEY", "free_tier": "完全免费"},
    "sambanova": {"name": "SambaNova", "url": "https://cloud.sambanova.ai/apis", "env_key": "SAMBANOVA_API_KEY", "free_tier": "完全免费"},
    "together": {"name": "Together", "url": "https://api.together.xyz/settings/api-keys", "env_key": "TOGETHER_API_KEY", "free_tier": "$5额度"},
    "cohere": {"name": "Cohere", "url": "https://dashboard.cohere.com/api-keys", "env_key": "COHERE_API_KEY", "free_tier": "Trial免费"},
    "openrouter": {"name": "OpenRouter", "url": "https://openrouter.ai/settings/keys", "env_key": "OPENROUTER_API_KEY", "free_tier": "部分免费"},
    "fireworks": {"name": "Fireworks", "url": "https://fireworks.ai/api-keys", "env_key": "FIREWORKS_API_KEY", "free_tier": "$1额度"},
    "deepseek": {"name": "DeepSeek", "url": "https://platform.deepseek.com/api_keys", "env_key": "DEEPSEEK_API_KEY", "free_tier": "新用户赠送"},
    "zhipu": {"name": "智谱AI", "url": "https://open.bigmodel.cn/usercenter/apikeys", "env_key": "ZHIPU_API_KEY", "free_tier": "新用户赠送"},
    "qwen": {"name": "通义千问", "url": "https://dashscope.console.aliyun.com/apiKey", "env_key": "DASHSCOPE_API_KEY", "free_tier": "新用户赠送"},
    "moonshot": {"name": "月之暗面", "url": "https://platform.moonshot.cn/console/api-keys", "env_key": "MOONSHOT_API_KEY", "free_tier": "新用户赠送"},
    "doubao": {"name": "字节豆包", "url": "https://console.volcengine.com/ark", "env_key": "ARK_API_KEY", "free_tier": "新用户赠送"},
    "hunyuan": {"name": "腾讯混元", "url": "https://console.cloud.tencent.com/hunyuan", "env_key": "HUNYUAN_API_KEY", "free_tier": "新用户赠送"},
    "ernie": {"name": "百度文心", "url": "https://console.bce.baidu.com/qianfan", "env_key": "QIANFAN_API_KEY", "free_tier": "新用户赠送"},
    "chatjd": {"name": "京东言犀", "url": "https://neuhub.jd.com/", "env_key": "JD_API_KEY", "free_tier": "有免费额度"},
}

class LLMKeyHelper:
    def __init__(self):
        self.pw = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def start(self):
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(headless=False)
        self.page = await (await self.browser.new_context()).new_page()

    async def stop(self):
        if self.browser: await self.browser.close()
        if self.pw: await self.pw.stop()

    async def open(self, provider: str):
        if provider not in PROVIDER_CONFIGS:
            print(f"未知: {provider}, 可用: {', '.join(PROVIDER_CONFIGS.keys())}")
            return
        cfg = PROVIDER_CONFIGS[provider]
        print(f"\n【{cfg['name']}】{cfg['free_tier']}\n环境变量: {cfg['env_key']}\nURL: {cfg['url']}")
        await self.start()
        await self.page.goto(cfg["url"])
        key = input("\n>>> 粘贴 API Key (Enter跳过): ").strip()
        if key:
            self._save(cfg["env_key"], key)
            print(f"[OK] {cfg['env_key']} 已保存")
        await self.stop()

    def _save(self, k, v):
        p = Path(__file__).parents[3] / ".env"
        if not p.exists(): p.write_text("")
        lines = p.read_text().split("\n")
        for i, l in enumerate(lines):
            if l.startswith(f"{k}="):
                lines[i] = f"{k}={v}"
                p.write_text("\n".join(lines))
                return
        lines.append(f"{k}={v}")
        p.write_text("\n".join(lines))

def print_list():
    print(f"\n{'Provider':<12}{'名称':<12}{'免费额度':<15}{'环境变量'}")
    print("-" * 55)
    for k, v in PROVIDER_CONFIGS.items():
        print(f"{k:<12}{v['name']:<12}{v['free_tier']:<15}{v['env_key']}")

async def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--list", "-l", action="store_true")
    p.add_argument("--open", "-o", metavar="P")
    a = p.parse_args()
    if a.list: print_list()
    elif a.open:
        h = LLMKeyHelper()
        try: await h.open(a.open)
        except KeyboardInterrupt: await h.stop()
    else: p.print_help()

if __name__ == "__main__":
    asyncio.run(main())
