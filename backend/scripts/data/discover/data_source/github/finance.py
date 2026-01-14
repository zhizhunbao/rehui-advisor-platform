# 金融理财相关 GitHub 数据源
from typing import Any, Dict, List

# banking - 银行开户
BANKING_SOURCES: List[Dict[str, Any]] = []

# credit_card - 信用卡
CREDIT_CARD_SOURCES: List[Dict[str, Any]] = []

# investment - 投资理财
INVESTMENT_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/wangzhe3224/awesome-systematic-trading", "name": "Awesome Systematic Trading", "description": "系统化交易资源", "source_type": "github", "domain_code": "investment", "tags": ["trading", "stock", "crypto"]},
    {"url": "https://github.com/mr-karan/awesome-investing", "name": "Awesome Investing", "description": "投资与金融相关资源精选", "source_type": "github", "domain_code": "investment", "tags": ["investing", "finance", "stock"]},
    {"url": "https://github.com/finwiki/awesome-personal-finance", "name": "Awesome Personal Finance", "description": "个人理财在线资源精选", "source_type": "github", "domain_code": "investment", "tags": ["personal-finance", "budgeting"]},
    {"url": "https://github.com/ashishb/personal-finance-awesome", "name": "Personal Finance Awesome", "description": "个人理财相关网站和工具列表", "source_type": "github", "domain_code": "investment", "tags": ["personal-finance", "tools"]},
    {"url": "https://github.com/SpiralDevelopment/Awesome-Crypto-Trading", "name": "Awesome Crypto Trading", "description": "加密货币交易资源", "source_type": "github", "domain_code": "investment", "tags": ["crypto", "trading", "bitcoin"]},
]

# insurance - 保险规划
INSURANCE_SOURCES: List[Dict[str, Any]] = []

# tax - 税务报税
TAX_SOURCES: List[Dict[str, Any]] = []

# remittance - 汇款转账
REMITTANCE_SOURCES: List[Dict[str, Any]] = []

# 汇总导出
FINANCE_GITHUB_SOURCES: List[Dict[str, Any]] = []
FINANCE_GITHUB_SOURCES.extend(BANKING_SOURCES)
FINANCE_GITHUB_SOURCES.extend(CREDIT_CARD_SOURCES)
FINANCE_GITHUB_SOURCES.extend(INVESTMENT_SOURCES)
FINANCE_GITHUB_SOURCES.extend(INSURANCE_SOURCES)
FINANCE_GITHUB_SOURCES.extend(TAX_SOURCES)
FINANCE_GITHUB_SOURCES.extend(REMITTANCE_SOURCES)
