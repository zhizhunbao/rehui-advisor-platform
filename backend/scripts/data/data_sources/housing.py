# 住房安居相关数据源
from typing import Any, Dict, List

HOUSING_SOURCES: List[Dict[str, Any]] = [
    {
        "url": "https://github.com/etewiah/awesome-real-estate",
        "name": "Awesome Real Estate",
        "description": "房地产相关资源和项目精选",
        "source_type": "github",
        "domain_code": "home_buying",
        "tags": ["real-estate", "housing", "property"],
    },
    {
        "url": "https://github.com/ual/rental-listings",
        "name": "Rental Listings Analysis",
        "description": "租房数据分析和可视化",
        "source_type": "github",
        "domain_code": "rental",
        "tags": ["rental", "data-analysis", "housing"],
    },
]
