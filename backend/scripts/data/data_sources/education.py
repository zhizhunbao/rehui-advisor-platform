# 教育培训相关数据源
from typing import Any, Dict, List

EDUCATION_SOURCES: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/ossu/computer-science",
        "name": "OSSU Computer Science",
        "description": "开源社会大学计算机科学自学课程",
        "source_type": "github",
        "domain_code": "school_selection",
        "tags": ["education", "computer-science", "self-study"],
    },
    {
        "url": "https://github.com/prakhar1989/awesome-courses",
        "name": "Awesome Courses",
        "description": "精选在线课程列表，涵盖CS各领域",
        "source_type": "github",
        "domain_code": "language_learning",
        "tags": ["education", "course", "MOOC"],
    },
    {
        "url": "https://github.com/EbookFoundation/free-programming-books",
        "name": "Free Programming Books",
        "description": "免费编程书籍资源，多语言支持",
        "source_type": "github",
        "domain_code": "school_selection",
        "tags": ["education", "books", "programming", "free"],
    },
    {
        "url": "https://github.com/freeCodeCamp/freeCodeCamp",
        "name": "freeCodeCamp",
        "description": "免费学习编程的开源社区",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["education", "coding", "web-development"],
    },
    {
        "url": "https://github.com/kamranahmedse/developer-roadmap",
        "name": "Developer Roadmap",
        "description": "开发者学习路线图，前端/后端/DevOps等",
        "source_type": "github",
        "domain_code": "skill_training",
        "tags": ["education", "roadmap", "career"],
    },
    {
        "url": "https://github.com/sindresorhus/awesome",
        "name": "Awesome Lists",
        "description": "Awesome 列表的列表，各领域精选资源汇总",
        "source_type": "github",
        "domain_code": "school_selection",
        "tags": ["awesome", "resources", "curated"],
    },
]
