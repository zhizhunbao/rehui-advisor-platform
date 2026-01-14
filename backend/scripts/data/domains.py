# 领域数据定义 - 完整的领域列表（使用 Lucide 图标名称）
from typing import Any, Dict, List

DOMAINS: List[Dict[str, Any]] = [
    # immigration - 移民签证
    {"code": "work_permit", "icon": "FileCheck", "name": "工签申请", "color": "bg-red-500", "name_en": "Work Permit", "is_active": True, "sort_order": 1, "category_code": "immigration", "description": "帮助您了解和申请加拿大工作签证", "description_en": "Help you understand and apply for Canadian work permit", "tags": ["工签", "LMIA", "工作许可", "work permit", "employment"]},
    {"code": "pr_application", "icon": "Award", "name": "PR申请", "color": "bg-red-500", "name_en": "PR Application", "is_active": True, "sort_order": 2, "category_code": "immigration", "description": "帮助您了解永久居民申请流程和要求", "description_en": "Help you understand PR application process and requirements", "tags": ["PR", "永久居民", "绿卡", "EE", "Express Entry", "PNP", "省提名"]},
    {"code": "citizenship", "icon": "Flag", "name": "入籍考试", "color": "bg-red-500", "name_en": "Citizenship Test", "is_active": True, "sort_order": 3, "category_code": "immigration", "description": "帮助您准备加拿大入籍考试", "description_en": "Help you prepare for Canadian citizenship test", "tags": ["入籍", "公民", "citizenship", "考试", "宣誓"]},
    {"code": "visa_renewal", "icon": "RefreshCw", "name": "签证续签", "color": "bg-red-500", "name_en": "Visa Renewal", "is_active": True, "sort_order": 4, "category_code": "immigration", "description": "帮助您了解签证续签流程和材料", "description_en": "Help you understand visa renewal process and documents", "tags": ["续签", "延期", "renewal", "extension", "visitor visa"]},
    {"code": "family_sponsorship", "icon": "Heart", "name": "家庭团聚", "color": "bg-red-500", "name_en": "Family Sponsorship", "is_active": True, "sort_order": 5, "category_code": "immigration", "description": "帮助您了解家庭团聚移民项目", "description_en": "Help you understand family sponsorship immigration", "tags": ["团聚", "担保", "配偶", "父母", "sponsorship", "family class"]},

    # housing - 住房安居
    {"code": "rental", "icon": "Key", "name": "租房", "color": "bg-green-500", "name_en": "Rental", "is_active": True, "sort_order": 1, "category_code": "housing", "description": "帮助您找到合适的租房并了解租房流程", "description_en": "Help you find rental and understand rental process", "tags": ["租房", "公寓", "apartment", "lease", "房东", "押金"]},
    {"code": "home_buying", "icon": "Home", "name": "买房", "color": "bg-green-500", "name_en": "Home Buying", "is_active": True, "sort_order": 2, "category_code": "housing", "description": "帮助您了解加拿大买房流程和注意事项", "description_en": "Help you understand home buying process in Canada", "tags": ["买房", "房贷", "mortgage", "首付", "验房", "过户"]},
    {"code": "moving", "icon": "Truck", "name": "搬家", "color": "bg-green-500", "name_en": "Moving", "is_active": True, "sort_order": 3, "category_code": "housing", "description": "帮助您规划和安排搬家事宜", "description_en": "Help you plan and arrange moving services", "tags": ["搬家", "搬运", "moving", "movers", "打包"]},
    {"code": "furniture", "icon": "Sofa", "name": "家具家电", "color": "bg-green-500", "name_en": "Furniture & Appliances", "is_active": True, "sort_order": 4, "category_code": "housing", "description": "帮助您选购家具家电和了解购买渠道", "description_en": "Help you buy furniture and appliances", "tags": ["家具", "家电", "IKEA", "furniture", "appliances", "二手"]},
    {"code": "utilities", "icon": "Zap", "name": "水电网络", "color": "bg-green-500", "name_en": "Utilities", "is_active": True, "sort_order": 5, "category_code": "housing", "description": "帮助您开通水电气网络等生活服务", "description_en": "Help you set up utilities and internet services", "tags": ["水电", "煤气", "网络", "utilities", "hydro", "internet"]},

    # career - 职业发展
    {"code": "job_search", "icon": "Search", "name": "求职就业", "color": "bg-purple-500", "name_en": "Job Search", "is_active": True, "sort_order": 1, "category_code": "career", "description": "帮助您找到理想的工作机会", "description_en": "Help you find your ideal job opportunities", "tags": ["求职", "找工作", "job", "career", "LinkedIn", "Indeed"]},
    {"code": "resume", "icon": "FileText", "name": "简历优化", "color": "bg-purple-500", "name_en": "Resume", "is_active": True, "sort_order": 2, "category_code": "career", "description": "帮助您优化简历，提升求职竞争力", "description_en": "Help you optimize your resume", "tags": ["简历", "CV", "resume", "cover letter", "求职信"]},
    {"code": "interview", "icon": "MessageSquare", "name": "面试技巧", "color": "bg-purple-500", "name_en": "Interview Skills", "is_active": True, "sort_order": 3, "category_code": "career", "description": "帮助您准备面试和提升面试技巧", "description_en": "Help you prepare for interviews", "tags": ["面试", "interview", "behavioral", "technical", "STAR"]},
    {"code": "certification", "icon": "BadgeCheck", "name": "职业认证", "color": "bg-purple-500", "name_en": "Professional Certification", "is_active": True, "sort_order": 4, "category_code": "career", "description": "帮助您了解加拿大职业认证要求", "description_en": "Help you understand professional certification requirements", "tags": ["认证", "执照", "license", "certification", "资格"]},
    {"code": "entrepreneurship", "icon": "Store", "name": "创业开店", "color": "bg-purple-500", "name_en": "Entrepreneurship", "is_active": True, "sort_order": 5, "category_code": "career", "description": "帮助您了解加拿大创业和开店流程", "description_en": "Help you understand entrepreneurship in Canada", "tags": ["创业", "开店", "business", "startup", "注册公司"]},

    # finance - 金融理财
    {"code": "banking", "icon": "Building", "name": "银行开户", "color": "bg-amber-500", "name_en": "Banking", "is_active": True, "sort_order": 1, "category_code": "finance", "description": "帮助您了解加拿大银行和开户流程", "description_en": "Help you understand Canadian banks and account opening", "tags": ["银行", "开户", "bank", "account", "TD", "RBC", "BMO"]},
    {"code": "credit_card", "icon": "CreditCard", "name": "信用卡", "color": "bg-amber-500", "name_en": "Credit Card", "is_active": True, "sort_order": 2, "category_code": "finance", "description": "帮助您选择合适的信用卡和建立信用", "description_en": "Help you choose credit cards and build credit", "tags": ["信用卡", "credit card", "信用分", "credit score", "返现"]},
    {"code": "investment", "icon": "TrendingUp", "name": "投资理财", "color": "bg-amber-500", "name_en": "Investment", "is_active": True, "sort_order": 3, "category_code": "finance", "description": "帮助您了解投资选择和理财规划", "description_en": "Help you understand investment options", "tags": ["投资", "理财", "TFSA", "RRSP", "股票", "ETF", "基金"]},
    {"code": "insurance", "icon": "Shield", "name": "保险规划", "color": "bg-amber-500", "name_en": "Insurance", "is_active": True, "sort_order": 4, "category_code": "finance", "description": "帮助您选择合适的保险方案", "description_en": "Help you choose the right insurance plan", "tags": ["保险", "insurance", "人寿", "life", "意外", "理赔"]},
    {"code": "tax", "icon": "Receipt", "name": "税务报税", "color": "bg-amber-500", "name_en": "Tax Filing", "is_active": True, "sort_order": 5, "category_code": "finance", "description": "帮助您了解税务知识和报税流程", "description_en": "Help you understand tax knowledge and filing", "tags": ["报税", "税务", "tax", "CRA", "退税", "T4"]},
    {"code": "remittance", "icon": "ArrowLeftRight", "name": "汇款转账", "color": "bg-amber-500", "name_en": "Remittance", "is_active": True, "sort_order": 6, "category_code": "finance", "description": "帮助您了解国际汇款和转账服务", "description_en": "Help you understand international remittance services", "tags": ["汇款", "转账", "remittance", "Wise", "换汇", "外汇"]},
]


# healthcare - 医疗健康
DOMAINS.extend([
    {"code": "health_insurance", "icon": "HeartPulse", "name": "医保申请", "color": "bg-pink-500", "name_en": "Health Insurance", "is_active": True, "sort_order": 1, "category_code": "healthcare", "description": "帮助您申请省级医疗保险", "description_en": "Help you apply for provincial health insurance", "tags": ["医保", "OHIP", "MSP", "health card", "健康卡"]},
    {"code": "family_doctor", "icon": "Stethoscope", "name": "家庭医生", "color": "bg-pink-500", "name_en": "Family Doctor", "is_active": True, "sort_order": 2, "category_code": "healthcare", "description": "帮助您找到和注册家庭医生", "description_en": "Help you find and register with a family doctor", "tags": ["家庭医生", "family doctor", "GP", "诊所", "clinic"]},
    {"code": "clinic_visit", "icon": "Hospital", "name": "看病就医", "color": "bg-pink-500", "name_en": "Clinic Visit", "is_active": True, "sort_order": 3, "category_code": "healthcare", "description": "帮助您了解加拿大就医流程", "description_en": "Help you understand healthcare system in Canada", "tags": ["看病", "就医", "急诊", "ER", "walk-in", "预约"]},
    {"code": "pharmacy", "icon": "Pill", "name": "药房买药", "color": "bg-pink-500", "name_en": "Pharmacy", "is_active": True, "sort_order": 4, "category_code": "healthcare", "description": "帮助您了解药房和购药流程", "description_en": "Help you understand pharmacy and medication", "tags": ["药房", "pharmacy", "处方", "prescription", "Shoppers"]},
    {"code": "mental_health", "icon": "Brain", "name": "心理健康", "color": "bg-pink-500", "name_en": "Mental Health", "is_active": True, "sort_order": 5, "category_code": "healthcare", "description": "帮助您了解心理健康资源和服务", "description_en": "Help you find mental health resources", "tags": ["心理", "mental health", "咨询", "counseling", "抑郁", "焦虑"]},
    {"code": "childcare", "icon": "Baby", "name": "儿童保健", "color": "bg-pink-500", "name_en": "Childcare", "is_active": True, "sort_order": 6, "category_code": "healthcare", "description": "帮助您了解儿童保健和托儿服务", "description_en": "Help you understand childcare services", "tags": ["儿童", "托儿", "daycare", "疫苗", "儿科"]},
])

# transportation - 交通出行
DOMAINS.extend([
    {"code": "driving_license", "icon": "IdCard", "name": "驾照考试", "color": "bg-blue-500", "name_en": "Driving License", "is_active": True, "sort_order": 1, "category_code": "transportation", "description": "帮助您了解驾照考试流程和要求", "description_en": "Help you understand driving license test process", "tags": ["驾照", "G1", "G2", "G牌", "路考", "笔试"]},
    {"code": "car_buying", "icon": "Car", "name": "买车卖车", "color": "bg-blue-500", "name_en": "Car Buying", "is_active": True, "sort_order": 2, "category_code": "transportation", "description": "帮助您了解买车卖车流程和注意事项", "description_en": "Help you understand car buying and selling", "tags": ["买车", "卖车", "二手车", "新车", "dealer", "私卖"]},
    {"code": "car_insurance", "icon": "ShieldCheck", "name": "汽车保险", "color": "bg-blue-500", "name_en": "Car Insurance", "is_active": True, "sort_order": 3, "category_code": "transportation", "description": "帮助您选择合适的汽车保险", "description_en": "Help you choose the right car insurance", "tags": ["车险", "car insurance", "保费", "理赔", "全险"]},
    {"code": "public_transit", "icon": "Bus", "name": "公共交通", "color": "bg-blue-500", "name_en": "Public Transit", "is_active": True, "sort_order": 4, "category_code": "transportation", "description": "帮助您了解公共交通系统和票价", "description_en": "Help you understand public transit system", "tags": ["公交", "地铁", "TTC", "Presto", "月票", "transit"]},
    {"code": "flight", "icon": "Plane", "name": "机票预订", "color": "bg-blue-500", "name_en": "Flight Booking", "is_active": True, "sort_order": 5, "category_code": "transportation", "description": "帮助您比较和预订最优惠的机票", "description_en": "Help you compare and book the best flight deals", "tags": ["机票", "flight", "航班", "特价", "里程", "积分"]},
])

# education - 教育培训
DOMAINS.extend([
    {"code": "school_selection", "icon": "School", "name": "学校选择", "color": "bg-cyan-500", "name_en": "School Selection", "is_active": True, "sort_order": 1, "category_code": "education", "description": "帮助您选择合适的学校", "description_en": "Help you choose the right school", "tags": ["学校", "school", "排名", "ranking", "申请", "录取"]},
    {"code": "language_learning", "icon": "Languages", "name": "语言学习", "color": "bg-cyan-500", "name_en": "Language Learning", "is_active": True, "sort_order": 2, "category_code": "education", "description": "帮助您规划语言学习路径", "description_en": "Help you plan your language learning path", "tags": ["英语", "ESL", "LINC", "雅思", "IELTS", "法语"]},
    {"code": "skill_training", "icon": "Wrench", "name": "技能培训", "color": "bg-cyan-500", "name_en": "Skill Training", "is_active": True, "sort_order": 3, "category_code": "education", "description": "帮助您找到合适的技能培训课程", "description_en": "Help you find skill training courses", "tags": ["培训", "技能", "training", "bootcamp", "证书", "课程"]},
    {"code": "credential_evaluation", "icon": "FileCheck2", "name": "学历认证", "color": "bg-cyan-500", "name_en": "Credential Evaluation", "is_active": True, "sort_order": 4, "category_code": "education", "description": "帮助您了解学历认证流程", "description_en": "Help you understand credential evaluation process", "tags": ["学历认证", "WES", "credential", "evaluation", "学位"]},
    {"code": "child_education", "icon": "Baby", "name": "子女教育", "color": "bg-cyan-500", "name_en": "Child Education", "is_active": True, "sort_order": 5, "category_code": "education", "description": "帮助您了解子女教育选择和资源", "description_en": "Help you understand child education options", "tags": ["子女", "教育", "小学", "中学", "私校", "公校"]},
    {"code": "tutoring", "icon": "BookOpen", "name": "课外辅导", "color": "bg-cyan-500", "name_en": "Tutoring", "is_active": True, "sort_order": 6, "category_code": "education", "description": "帮助您找到课外辅导资源", "description_en": "Help you find tutoring resources", "tags": ["辅导", "补习", "tutoring", "家教", "网课"]},
])


# daily_life - 日常生活
DOMAINS.extend([
    {"code": "mobile_telecom", "icon": "Smartphone", "name": "手机通讯", "color": "bg-orange-500", "name_en": "Mobile & Telecom", "is_active": True, "sort_order": 1, "category_code": "daily_life", "description": "帮助您选择手机套餐和通讯服务", "description_en": "Help you choose mobile plans and telecom services", "tags": ["手机", "套餐", "Rogers", "Bell", "Telus", "Fido"]},
    {"code": "shopping", "icon": "ShoppingCart", "name": "购物省钱", "color": "bg-orange-500", "name_en": "Shopping & Deals", "is_active": True, "sort_order": 2, "category_code": "daily_life", "description": "帮助您了解购物渠道和省钱技巧", "description_en": "Help you find shopping deals and save money", "tags": ["购物", "省钱", "折扣", "deal", "Costco", "Amazon"]},
    {"code": "dining", "icon": "UtensilsCrossed", "name": "餐饮美食", "color": "bg-orange-500", "name_en": "Dining", "is_active": True, "sort_order": 3, "category_code": "daily_life", "description": "帮助您发现美食和餐厅推荐", "description_en": "Help you discover restaurants and food", "tags": ["餐厅", "美食", "restaurant", "外卖", "Uber Eats", "DoorDash"]},
    {"code": "pets", "icon": "PawPrint", "name": "宠物养护", "color": "bg-orange-500", "name_en": "Pets", "is_active": True, "sort_order": 4, "category_code": "daily_life", "description": "帮助您了解宠物养护和相关服务", "description_en": "Help you understand pet care and services", "tags": ["宠物", "猫", "狗", "pet", "兽医", "宠物店"]},
    {"code": "delivery", "icon": "Package", "name": "快递物流", "color": "bg-orange-500", "name_en": "Delivery & Logistics", "is_active": True, "sort_order": 5, "category_code": "daily_life", "description": "帮助您了解快递物流和国际邮寄", "description_en": "Help you understand delivery and shipping", "tags": ["快递", "物流", "邮寄", "Canada Post", "UPS", "海运"]},
    {"code": "internet", "icon": "Wifi", "name": "网络服务", "color": "bg-orange-500", "name_en": "Internet", "is_active": True, "sort_order": 6, "category_code": "daily_life", "description": "帮助您选择网络服务提供商", "description_en": "Help you choose internet service providers", "tags": ["网络", "宽带", "internet", "WiFi", "光纤", "ISP"]},
    {"code": "secondhand", "icon": "Recycle", "name": "二手交易", "color": "bg-orange-500", "name_en": "Secondhand", "is_active": True, "sort_order": 7, "category_code": "daily_life", "description": "帮助您买卖二手物品", "description_en": "Help you buy and sell secondhand items", "tags": ["二手", "闲置", "Kijiji", "Facebook", "Marketplace"]},
    {"code": "storage", "icon": "Archive", "name": "仓储服务", "color": "bg-orange-500", "name_en": "Storage", "is_active": True, "sort_order": 8, "category_code": "daily_life", "description": "帮助您找到仓储服务", "description_en": "Help you find storage services", "tags": ["仓储", "storage", "存储", "self-storage", "迷你仓"]},
])

# legal - 法律权益
DOMAINS.extend([
    {"code": "rental_contract", "icon": "FileSignature", "name": "租房合同", "color": "bg-slate-500", "name_en": "Rental Contract", "is_active": True, "sort_order": 1, "category_code": "legal", "description": "帮助您了解租房合同条款和权益", "description_en": "Help you understand rental contract terms", "tags": ["租房合同", "lease", "租约", "房东", "租客权益"]},
    {"code": "labor_rights", "icon": "Gavel", "name": "劳动权益", "color": "bg-slate-500", "name_en": "Labor Rights", "is_active": True, "sort_order": 2, "category_code": "legal", "description": "帮助您了解劳动法和员工权益", "description_en": "Help you understand labor law and employee rights", "tags": ["劳动法", "员工权益", "labor", "employment", "解雇", "工资"]},
    {"code": "consumer_rights", "icon": "ShieldAlert", "name": "消费维权", "color": "bg-slate-500", "name_en": "Consumer Rights", "is_active": True, "sort_order": 3, "category_code": "legal", "description": "帮助您了解消费者权益和维权途径", "description_en": "Help you understand consumer rights", "tags": ["消费者", "维权", "consumer", "投诉", "退款", "欺诈"]},
    {"code": "traffic_accident", "icon": "AlertTriangle", "name": "交通事故", "color": "bg-slate-500", "name_en": "Traffic Accident", "is_active": True, "sort_order": 4, "category_code": "legal", "description": "帮助您了解交通事故处理流程", "description_en": "Help you understand traffic accident procedures", "tags": ["交通事故", "accident", "理赔", "报警", "保险"]},
    {"code": "legal_consultation", "icon": "Scale", "name": "法律咨询", "color": "bg-slate-500", "name_en": "Legal Consultation", "is_active": True, "sort_order": 5, "category_code": "legal", "description": "帮助您找到法律咨询资源", "description_en": "Help you find legal consultation resources", "tags": ["法律", "律师", "lawyer", "咨询", "法律援助"]},
])

# social - 社交融入
DOMAINS.extend([
    {"code": "chinese_community", "icon": "Users", "name": "华人社区", "color": "bg-indigo-500", "name_en": "Chinese Community", "is_active": True, "sort_order": 1, "category_code": "social", "description": "帮助您融入当地华人社区", "description_en": "Help you connect with Chinese community", "tags": ["华人", "社区", "community", "同乡会", "微信群"]},
    {"code": "cultural_events", "icon": "Calendar", "name": "文化活动", "color": "bg-indigo-500", "name_en": "Cultural Events", "is_active": True, "sort_order": 2, "category_code": "social", "description": "帮助您发现文化活动和节日庆典", "description_en": "Help you discover cultural events and festivals", "tags": ["活动", "节日", "event", "festival", "春节", "中秋"]},
    {"code": "volunteering", "icon": "HandHeart", "name": "志愿服务", "color": "bg-indigo-500", "name_en": "Volunteering", "is_active": True, "sort_order": 3, "category_code": "social", "description": "帮助您找到志愿服务机会", "description_en": "Help you find volunteering opportunities", "tags": ["志愿者", "volunteer", "义工", "公益", "社区服务"]},
    {"code": "religion", "icon": "Church", "name": "宗教信仰", "color": "bg-indigo-500", "name_en": "Religion", "is_active": True, "sort_order": 4, "category_code": "social", "description": "帮助您找到宗教场所和活动", "description_en": "Help you find religious places and activities", "tags": ["宗教", "教会", "church", "寺庙", "清真寺"]},
    {"code": "dating", "icon": "Heart", "name": "交友婚恋", "color": "bg-indigo-500", "name_en": "Dating & Marriage", "is_active": True, "sort_order": 5, "category_code": "social", "description": "帮助您了解交友和婚恋资源", "description_en": "Help you find dating and marriage resources", "tags": ["交友", "婚恋", "dating", "相亲", "单身"]},
])


# identity - 身份证件
DOMAINS.extend([
    {"code": "visa", "icon": "Stamp", "name": "签证身份", "color": "bg-teal-500", "name_en": "Visa", "is_active": True, "sort_order": 1, "category_code": "identity", "description": "帮助您了解签证和身份相关事宜", "description_en": "Help you understand visa and identity matters", "tags": ["签证", "visa", "身份", "status", "合法身份"]},
    {"code": "ssn", "icon": "IdCard", "name": "SIN卡申请", "color": "bg-teal-500", "name_en": "SIN Card", "is_active": True, "sort_order": 2, "category_code": "identity", "description": "帮助您申请社会保险号码", "description_en": "Help you apply for Social Insurance Number", "tags": ["SIN", "社保号", "工卡", "social insurance", "税号"]},
    {"code": "driving", "icon": "CarFront", "name": "驾照换领", "color": "bg-teal-500", "name_en": "Driving License", "is_active": True, "sort_order": 3, "category_code": "identity", "description": "帮助您换领加拿大驾照", "description_en": "Help you exchange for Canadian driving license", "tags": ["驾照", "换领", "license", "国际驾照", "翻译"]},
])

# travel - 出行旅游
DOMAINS.extend([
    {"code": "travel_flight", "icon": "Plane", "name": "机票预订", "color": "bg-sky-500", "name_en": "Flight Booking", "is_active": True, "sort_order": 1, "category_code": "travel", "description": "帮助您比较和预订最优惠的机票", "description_en": "Help you compare and book the best flight deals", "tags": ["机票", "flight", "航班", "特价机票", "里程兑换"]},
    {"code": "hotel", "icon": "Hotel", "name": "酒店住宿", "color": "bg-sky-500", "name_en": "Hotel", "is_active": True, "sort_order": 2, "category_code": "travel", "description": "帮助您预订酒店和住宿", "description_en": "Help you book hotels and accommodations", "tags": ["酒店", "hotel", "民宿", "Airbnb", "住宿"]},
    {"code": "car_rental", "icon": "CarTaxiFront", "name": "租车自驾", "color": "bg-sky-500", "name_en": "Car Rental", "is_active": True, "sort_order": 3, "category_code": "travel", "description": "帮助您租车和自驾游", "description_en": "Help you rent cars for road trips", "tags": ["租车", "car rental", "自驾", "Hertz", "Enterprise"]},
    {"code": "travel_planning", "icon": "Map", "name": "旅行规划", "color": "bg-sky-500", "name_en": "Travel Planning", "is_active": True, "sort_order": 4, "category_code": "travel", "description": "帮助您规划旅行行程", "description_en": "Help you plan your travel itinerary", "tags": ["旅行", "行程", "travel", "攻略", "景点", "签证"]},
])

# leisure - 休闲娱乐
DOMAINS.extend([
    {"code": "fitness", "icon": "Dumbbell", "name": "健身运动", "color": "bg-fuchsia-500", "name_en": "Fitness", "is_active": True, "sort_order": 1, "category_code": "leisure", "description": "帮助您找到健身房和运动场所", "description_en": "Help you find gyms and sports facilities", "tags": ["健身", "gym", "运动", "瑜伽", "游泳", "跑步"]},
    {"code": "entertainment", "icon": "Film", "name": "娱乐休闲", "color": "bg-fuchsia-500", "name_en": "Entertainment", "is_active": True, "sort_order": 2, "category_code": "leisure", "description": "帮助您发现娱乐活动和场所", "description_en": "Help you discover entertainment activities", "tags": ["娱乐", "电影", "KTV", "游戏", "演出", "音乐会"]},
])

# home_services - 家政服务
DOMAINS.extend([
    {"code": "cleaning", "icon": "Sparkles", "name": "清洁服务", "color": "bg-lime-500", "name_en": "Cleaning", "is_active": True, "sort_order": 1, "category_code": "home_services", "description": "帮助您找到清洁服务", "description_en": "Help you find cleaning services", "tags": ["清洁", "保洁", "cleaning", "家政", "钟点工"]},
    {"code": "repair", "icon": "Wrench", "name": "家电维修", "color": "bg-lime-500", "name_en": "Repair", "is_active": True, "sort_order": 2, "category_code": "home_services", "description": "帮助您找到家电维修服务", "description_en": "Help you find appliance repair services", "tags": ["维修", "repair", "家电", "水管", "电工"]},
])

# life_events - 人生大事
DOMAINS.extend([
    {"code": "wedding", "icon": "Heart", "name": "婚礼筹备", "color": "bg-emerald-500", "name_en": "Wedding", "is_active": True, "sort_order": 1, "category_code": "life_events", "description": "帮助您筹备婚礼", "description_en": "Help you plan your wedding", "tags": ["婚礼", "wedding", "结婚", "婚纱", "婚宴"]},
    {"code": "funeral", "icon": "Flower2", "name": "丧葬服务", "color": "bg-emerald-500", "name_en": "Funeral", "is_active": True, "sort_order": 2, "category_code": "life_events", "description": "帮助您了解丧葬服务", "description_en": "Help you understand funeral services", "tags": ["丧葬", "funeral", "殡仪", "墓地", "追悼"]},
])

# communication - 通讯网络
DOMAINS.extend([
    {"code": "phone_plan", "icon": "Phone", "name": "手机套餐", "color": "bg-violet-500", "name_en": "Phone Plan", "is_active": True, "sort_order": 1, "category_code": "communication", "description": "帮助您选择合适的手机套餐", "description_en": "Help you choose the right phone plan", "tags": ["手机套餐", "phone plan", "流量", "话费", "合约机"]},
    {"code": "internet_service", "icon": "Globe", "name": "网络服务", "color": "bg-violet-500", "name_en": "Internet Service", "is_active": True, "sort_order": 2, "category_code": "communication", "description": "帮助您选择网络服务提供商", "description_en": "Help you choose internet service providers", "tags": ["网络", "internet", "宽带", "光纤", "ISP"]},
    {"code": "shipping", "icon": "Send", "name": "快递物流", "color": "bg-violet-500", "name_en": "Shipping", "is_active": True, "sort_order": 3, "category_code": "communication", "description": "帮助您了解快递物流服务", "description_en": "Help you understand shipping services", "tags": ["快递", "shipping", "物流", "邮寄", "包裹"]},
])

# food_shopping - 餐饮购物
DOMAINS.extend([
    {"code": "restaurants", "icon": "Utensils", "name": "餐厅美食", "color": "bg-rose-500", "name_en": "Restaurants", "is_active": True, "sort_order": 1, "category_code": "food_shopping", "description": "帮助您发现美食和餐厅", "description_en": "Help you discover restaurants and food", "tags": ["餐厅", "美食", "restaurant", "中餐", "西餐", "日料"]},
    {"code": "grocery", "icon": "ShoppingBasket", "name": "超市购物", "color": "bg-rose-500", "name_en": "Grocery", "is_active": True, "sort_order": 2, "category_code": "food_shopping", "description": "帮助您了解超市和购物", "description_en": "Help you find grocery stores", "tags": ["超市", "grocery", "华人超市", "T&T", "Walmart", "No Frills"]},
    {"code": "deals", "icon": "Tag", "name": "优惠折扣", "color": "bg-rose-500", "name_en": "Deals", "is_active": True, "sort_order": 3, "category_code": "food_shopping", "description": "帮助您找到优惠折扣", "description_en": "Help you find deals and discounts", "tags": ["优惠", "折扣", "deal", "coupon", "促销", "黑五"]},
])
