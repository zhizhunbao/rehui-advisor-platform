# 教育培训相关 GitHub 数据源
from typing import Any, Dict, List

# school_selection - 学校选择
SCHOOL_SELECTION_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/ossu/computer-science", "name": "OSSU Computer Science", "description": "开源社会大学计算机科学自学课程", "source_type": "github", "domain_code": "school_selection", "tags": ["education", "computer-science", "self-study"]},
    {"url": "https://github.com/EbookFoundation/free-programming-books", "name": "Free Programming Books", "description": "免费编程书籍资源", "source_type": "github", "domain_code": "school_selection", "tags": ["education", "books", "programming"]},
    {"url": "https://github.com/sindresorhus/awesome", "name": "Awesome Lists", "description": "Awesome 列表的列表", "source_type": "github", "domain_code": "school_selection", "tags": ["awesome", "resources", "curated"]},
]

# language_learning - 语言学习
LANGUAGE_LEARNING_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/prakhar1989/awesome-courses", "name": "Awesome Courses", "description": "精选在线课程列表", "source_type": "github", "domain_code": "language_learning", "tags": ["education", "course", "MOOC"]},
]

# skill_training - 技能培训
SKILL_TRAINING_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/freeCodeCamp/freeCodeCamp", "name": "freeCodeCamp", "description": "免费学习编程的开源社区", "source_type": "github", "domain_code": "skill_training", "tags": ["education", "coding", "web-development"]},
    {"url": "https://github.com/kamranahmedse/developer-roadmap", "name": "Developer Roadmap", "description": "开发者学习路线图", "source_type": "github", "domain_code": "skill_training", "tags": ["education", "roadmap", "career"]},
]

# credential_evaluation - 学历认证
CREDENTIAL_EVALUATION_SOURCES: List[Dict[str, Any]] = []

# child_education - 子女教育
CHILD_EDUCATION_SOURCES: List[Dict[str, Any]] = []

# tutoring - 课外辅导
TUTORING_SOURCES: List[Dict[str, Any]] = []

# 汇总导出
EDUCATION_GITHUB_SOURCES: List[Dict[str, Any]] = []
EDUCATION_GITHUB_SOURCES.extend(SCHOOL_SELECTION_SOURCES)
EDUCATION_GITHUB_SOURCES.extend(LANGUAGE_LEARNING_SOURCES)
EDUCATION_GITHUB_SOURCES.extend(SKILL_TRAINING_SOURCES)
EDUCATION_GITHUB_SOURCES.extend(CREDENTIAL_EVALUATION_SOURCES)
EDUCATION_GITHUB_SOURCES.extend(CHILD_EDUCATION_SOURCES)
EDUCATION_GITHUB_SOURCES.extend(TUTORING_SOURCES)
