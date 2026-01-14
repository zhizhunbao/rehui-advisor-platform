# 出行旅游相关 GitHub 数据源
from typing import Any, Dict, List

# travel_flight - 机票预订
TRAVEL_FLIGHT_SOURCES: List[Dict[str, Any]] = []

# hotel - 酒店住宿
HOTEL_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/TravelXML/Free-Hotel-Booking-Engine", "name": "Free Hotel Booking Engine", "description": "开源酒店预订引擎", "source_type": "github", "domain_code": "hotel", "tags": ["hotel", "booking", "travel"]},
]

# car_rental - 租车自驾
CAR_RENTAL_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/Marcin214/awesome-automotive", "name": "Awesome Automotive", "description": "汽车工程资源精选", "source_type": "github", "domain_code": "car_rental", "tags": ["automotive", "car", "vehicle"]},
    {"url": "https://github.com/jaredthecoder/awesome-vehicle-security", "name": "Awesome Vehicle Security", "description": "汽车安全和黑客技术学习资源", "source_type": "github", "domain_code": "car_rental", "tags": ["vehicle", "security", "car-hacking"]},
]

# travel_planning - 旅行规划
TRAVEL_PLANNING_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/Nedal-Esrar/Travel-and-Accommodation-Booking-Platform", "name": "Travel Booking Platform", "description": "旅行住宿预订平台 API", "source_type": "github", "domain_code": "travel_planning", "tags": ["hotel", "travel", "API"]},
]

# 汇总导出
TRAVEL_GITHUB_SOURCES: List[Dict[str, Any]] = []
TRAVEL_GITHUB_SOURCES.extend(TRAVEL_FLIGHT_SOURCES)
TRAVEL_GITHUB_SOURCES.extend(HOTEL_SOURCES)
TRAVEL_GITHUB_SOURCES.extend(CAR_RENTAL_SOURCES)
TRAVEL_GITHUB_SOURCES.extend(TRAVEL_PLANNING_SOURCES)
