# 职业发展相关 GitHub 数据源
from typing import Any, Dict, List

# job_search - 求职就业
JOB_SEARCH_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/Lamiiine/Awesome-daily-list-of-visa-sponsored-jobs", "name": "Awesome Visa Sponsored Jobs", "description": "每日更新的签证担保工作机会列表", "source_type": "github", "domain_code": "job_search", "tags": ["visa", "job", "sponsorship"]},
    {"url": "https://github.com/emredurukn/awesome-job-boards", "name": "Awesome Job Boards", "description": "精选求职网站列表", "source_type": "github", "domain_code": "job_search", "tags": ["job", "career", "job-board"]},
    {"url": "https://github.com/remoteintech/remote-jobs", "name": "Remote Jobs", "description": "提供远程工作的科技公司列表", "source_type": "github", "domain_code": "job_search", "tags": ["remote", "job", "work-from-home"]},
]

# resume - 简历优化
RESUME_SOURCES: List[Dict[str, Any]] = []

# interview - 面试技巧
INTERVIEW_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/poteto/hiring-without-whiteboards", "name": "Hiring Without Whiteboards", "description": "不使用白板面试的公司列表", "source_type": "github", "domain_code": "interview", "tags": ["interview", "hiring", "job"]},
    {"url": "https://github.com/jwasham/coding-interview-university", "name": "Coding Interview University", "description": "完整的计算机科学学习计划", "source_type": "github", "domain_code": "interview", "tags": ["interview", "coding", "study"]},
    {"url": "https://github.com/yangshun/tech-interview-handbook", "name": "Tech Interview Handbook", "description": "技术面试手册", "source_type": "github", "domain_code": "interview", "tags": ["interview", "algorithm", "system-design"]},
    {"url": "https://github.com/donnemartin/system-design-primer", "name": "System Design Primer", "description": "系统设计面试准备资源", "source_type": "github", "domain_code": "interview", "tags": ["system-design", "interview", "architecture"]},
    {"url": "https://github.com/kdn251/interviews", "name": "Interviews", "description": "软件工程技术面试必备知识", "source_type": "github", "domain_code": "interview", "tags": ["interview", "algorithm", "data-structure"]},
]

# certification - 职业认证
CERTIFICATION_SOURCES: List[Dict[str, Any]] = []

# entrepreneurship - 创业开店
ENTREPRENEURSHIP_SOURCES: List[Dict[str, Any]] = []

# 汇总导出
CAREER_GITHUB_SOURCES: List[Dict[str, Any]] = []
CAREER_GITHUB_SOURCES.extend(JOB_SEARCH_SOURCES)
CAREER_GITHUB_SOURCES.extend(RESUME_SOURCES)
CAREER_GITHUB_SOURCES.extend(INTERVIEW_SOURCES)
CAREER_GITHUB_SOURCES.extend(CERTIFICATION_SOURCES)
CAREER_GITHUB_SOURCES.extend(ENTREPRENEURSHIP_SOURCES)
