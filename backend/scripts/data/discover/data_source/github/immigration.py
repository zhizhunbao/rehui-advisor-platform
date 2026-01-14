# 移民签证相关 GitHub 数据源
from typing import Any, Dict, List

# work_permit - 工签申请
WORK_PERMIT_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/nickliqian/h1b-salary-database", "name": "H1B Salary Database", "description": "H1B 签证薪资数据库", "source_type": "github", "domain_code": "work_permit", "tags": ["H1B", "salary", "visa"]},
]

# pr_application - PR申请
PR_APPLICATION_SOURCES: List[Dict[str, Any]] = []

# citizenship - 入籍考试
CITIZENSHIP_SOURCES: List[Dict[str, Any]] = []

# visa_renewal - 签证续签
VISA_RENEWAL_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/AwesomeVisa/awesome-immigration", "name": "Awesome Immigration", "description": "各国移民签证信息汇总", "source_type": "github", "domain_code": "visa_renewal", "tags": ["immigration", "visa", "green-card"]},
]

# family_sponsorship - 家庭团聚
FAMILY_SPONSORSHIP_SOURCES: List[Dict[str, Any]] = []

# 汇总导出
IMMIGRATION_GITHUB_SOURCES: List[Dict[str, Any]] = []
IMMIGRATION_GITHUB_SOURCES.extend(WORK_PERMIT_SOURCES)
IMMIGRATION_GITHUB_SOURCES.extend(PR_APPLICATION_SOURCES)
IMMIGRATION_GITHUB_SOURCES.extend(CITIZENSHIP_SOURCES)
IMMIGRATION_GITHUB_SOURCES.extend(VISA_RENEWAL_SOURCES)
IMMIGRATION_GITHUB_SOURCES.extend(FAMILY_SPONSORSHIP_SOURCES)
