# 住房安居相关 GitHub 数据源
from typing import Any, Dict, List

# rental - 租房
RENTAL_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/ual/rental-listings", "name": "Rental Listings Analysis", "description": "租房数据分析和可视化", "source_type": "github", "domain_code": "rental", "tags": ["rental", "data-analysis", "housing"]},
]

# home_buying - 买房
HOME_BUYING_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/etewiah/awesome-real-estate", "name": "Awesome Real Estate", "description": "房地产相关资源和项目精选", "source_type": "github", "domain_code": "home_buying", "tags": ["real-estate", "housing", "property"]},
]

# moving - 搬家
MOVING_SOURCES: List[Dict[str, Any]] = []

# furniture - 家具家电
FURNITURE_SOURCES: List[Dict[str, Any]] = []

# utilities - 水电网络
UTILITIES_SOURCES: List[Dict[str, Any]] = []

# 汇总导出
HOUSING_GITHUB_SOURCES: List[Dict[str, Any]] = []
HOUSING_GITHUB_SOURCES.extend(RENTAL_SOURCES)
HOUSING_GITHUB_SOURCES.extend(HOME_BUYING_SOURCES)
HOUSING_GITHUB_SOURCES.extend(MOVING_SOURCES)
HOUSING_GITHUB_SOURCES.extend(FURNITURE_SOURCES)
HOUSING_GITHUB_SOURCES.extend(UTILITIES_SOURCES)
