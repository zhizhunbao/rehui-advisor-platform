# 移民签证相关数据源
from typing import Any, Dict, List

IMMIGRATION_SOURCES: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/AwesomeVisa/awesome-immigration",
        "name": "Awesome Immigration",
        "description": "各国移民签证信息汇总",
        "source_type": "github",
        "domain_code": "visa",
        "tags": ["immigration", "visa", "green-card"],
    },
    {
        "url": "https://github.com/nickliqian/h1b-salary-database",
        "name": "H1B Salary Database",
        "description": "H1B 签证薪资数据库",
        "source_type": "github",
        "domain_code": "work_permit",
        "tags": ["H1B", "salary", "visa"],
    },
]
