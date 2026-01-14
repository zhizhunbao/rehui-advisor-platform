# 医疗健康相关 GitHub 数据源
from typing import Any, Dict, List

# health_insurance - 医保申请
HEALTH_INSURANCE_SOURCES: List[Dict[str, Any]] = [
    {"url": "https://github.com/kakoni/awesome-healthcare", "name": "Awesome Healthcare", "description": "开源医疗健康软件、库和资源", "source_type": "github", "domain_code": "health_insurance", "tags": ["healthcare", "health", "medical"]},
    {"url": "https://github.com/medtorch/awesome-healthcare-ai", "name": "Awesome Healthcare AI", "description": "医疗健康 AI 工具、算法和数据集", "source_type": "github", "domain_code": "health_insurance", "tags": ["healthcare", "AI", "medical"]},
]

# family_doctor - 家庭医生
FAMILY_DOCTOR_SOURCES: List[Dict[str, Any]] = []

# clinic_visit - 看病就医
CLINIC_VISIT_SOURCES: List[Dict[str, Any]] = []

# pharmacy - 药房买药
PHARMACY_SOURCES: List[Dict[str, Any]] = []

# mental_health - 心理健康
MENTAL_HEALTH_SOURCES: List[Dict[str, Any]] = []

# childcare - 儿童保健
CHILDCARE_SOURCES: List[Dict[str, Any]] = []

# 汇总导出
HEALTHCARE_GITHUB_SOURCES: List[Dict[str, Any]] = []
HEALTHCARE_GITHUB_SOURCES.extend(HEALTH_INSURANCE_SOURCES)
HEALTHCARE_GITHUB_SOURCES.extend(FAMILY_DOCTOR_SOURCES)
HEALTHCARE_GITHUB_SOURCES.extend(CLINIC_VISIT_SOURCES)
HEALTHCARE_GITHUB_SOURCES.extend(PHARMACY_SOURCES)
HEALTHCARE_GITHUB_SOURCES.extend(MENTAL_HEALTH_SOURCES)
HEALTHCARE_GITHUB_SOURCES.extend(CHILDCARE_SOURCES)
