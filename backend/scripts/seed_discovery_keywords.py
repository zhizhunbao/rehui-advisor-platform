"""Seed discovery keywords for all domains"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Domain code to discovery keywords mapping
DOMAIN_KEYWORDS = {
    # 身份证件
    "visa": [
        "awesome-immigration",
        "h1b stars:>50",
        "green-card stars:>30",
        "visa-tracker stars:>20",
        "immigration-usa stars:>30",
        "topic:immigration",
        "topic:visa",
    ],
    "ssn": [
        "ssn stars:>10",
        "itin stars:>10",
        "social-security stars:>20",
        "tax-id stars:>10",
        "topic:ssn",
    ],
    "driving": [
        "dmv stars:>20",
        "driving-test stars:>30",
        "driver-license stars:>20",
        "road-test stars:>10",
        "topic:driving",
        "topic:dmv",
    ],
    
    # 日常生活
    "housing": [
        "awesome-real-estate",
        "apartment-finder stars:>30",
        "rental-platform stars:>30",
        "zillow stars:>20",
        "topic:real-estate",
        "topic:housing",
        "topic:rental",
    ],
    "moving": [
        "moving-checklist stars:>20",
        "relocation-guide stars:>10",
        "moving-tips stars:>10",
        "topic:moving",
        "topic:relocation",
    ],
    "utilities": [
        "utility-api stars:>10",
        "energy-comparison stars:>10",
        "electricity-bill stars:>10",
        "topic:utilities",
        "topic:energy",
    ],
    "storage": [
        "self-storage stars:>10",
        "storage-unit stars:>10",
        "topic:storage",
    ],
    
    # 金融理财
    "banking": [
        "awesome-fintech",
        "banking-api stars:>50",
        "plaid stars:>100",
        "bank-account stars:>20",
        "topic:banking",
        "topic:fintech",
    ],
    "credit": [
        "awesome-credit",
        "credit-score stars:>50",
        "credit-builder stars:>30",
        "fico stars:>20",
        "credit-card stars:>50",
        "topic:credit",
        "topic:credit-score",
    ],
    "investment": [
        "awesome-quant",
        "awesome-trading",
        "stock-trading stars:>100",
        "investment-portfolio stars:>30",
        "topic:trading",
        "topic:investment",
    ],
    "insurance": [
        "awesome-insurance",
        "insurance-api stars:>20",
        "health-insurance stars:>20",
        "topic:insurance",
        "topic:insurtech",
    ],
    "tax": [
        "tax-calculator stars:>30",
        "tax-software stars:>20",
        "irs stars:>10",
        "tax-filing stars:>20",
        "topic:tax",
        "topic:accounting",
    ],
    "remittance": [
        "remittance stars:>20",
        "money-transfer stars:>30",
        "currency-exchange stars:>30",
        "wise-api stars:>10",
        "topic:remittance",
    ],
    
    # 职业发展
    "job": [
        "awesome-interview",
        "awesome-job",
        "job-board stars:>50",
        "linkedin stars:>30",
        "resume-parser stars:>30",
        "topic:job-search",
        "topic:career",
        "topic:interview",
    ],
    "resume": [
        "awesome-resume",
        "resume-builder stars:>100",
        "cv-builder stars:>50",
        "resume-template stars:>50",
        "topic:resume",
        "topic:cv",
    ],
    
    # 出行旅游
    "flight": [
        "awesome-flights",
        "awesome-aviation",
        "flight-api stars:>50",
        "flight-tracker stars:>50",
        "airfare stars:>20",
        "topic:flight",
        "topic:aviation",
    ],
    "hotel": [
        "awesome-travel",
        "hotel-api stars:>30",
        "hotel-booking stars:>50",
        "airbnb stars:>30",
        "topic:hotel",
        "topic:travel",
    ],
    "car_rental": [
        "car-rental-api stars:>20",
        "vehicle-rental stars:>20",
        "rental-car stars:>10",
        "topic:car-rental",
    ],
    "travel": [
        "awesome-travel",
        "travel-api stars:>50",
        "trip-planner stars:>30",
        "itinerary stars:>20",
        "topic:travel",
        "topic:tourism",
    ],
    
    # 通讯网络
    "phone": [
        "phone-plan stars:>10",
        "carrier-comparison stars:>10",
        "mobile-plan stars:>20",
        "mvno stars:>10",
        "topic:telecom",
        "topic:mobile",
    ],
    "internet": [
        "isp-comparison stars:>10",
        "internet-speed stars:>20",
        "broadband stars:>20",
        "speedtest stars:>30",
        "topic:internet",
        "topic:isp",
    ],
    "shipping": [
        "shipping-api stars:>30",
        "package-tracking stars:>20",
        "international-shipping stars:>10",
        "usps stars:>10",
        "topic:shipping",
        "topic:logistics",
    ],
    
    # 医疗法律
    "healthcare": [
        "awesome-healthcare",
        "awesome-health",
        "healthcare-api stars:>50",
        "medical-api stars:>30",
        "health-insurance stars:>20",
        "topic:healthcare",
        "topic:health",
    ],
    "legal": [
        "awesome-legal",
        "legal-api stars:>20",
        "contract-analysis stars:>20",
        "lawyer-finder stars:>10",
        "topic:legal",
        "topic:legaltech",
    ],
    "childcare": [
        "awesome-parenting",
        "daycare stars:>10",
        "childcare stars:>20",
        "babysitter stars:>10",
        "topic:parenting",
        "topic:childcare",
    ],
    
    # 教育学习
    "school": [
        "awesome-education",
        "school-ranking stars:>20",
        "university-api stars:>20",
        "college-finder stars:>10",
        "topic:education",
        "topic:university",
    ],
    "language": [
        "awesome-language-learning",
        "language-learning stars:>100",
        "flashcard stars:>50",
        "duolingo stars:>20",
        "anki stars:>50",
        "topic:language-learning",
    ],
    "tutoring": [
        "awesome-tutoring",
        "tutoring-platform stars:>30",
        "online-tutoring stars:>30",
        "homework-help stars:>20",
        "topic:tutoring",
        "topic:education",
    ],
    
    # 餐饮购物
    "shopping": [
        "awesome-deals",
        "price-comparison stars:>50",
        "cashback stars:>30",
        "coupon stars:>50",
        "deal-finder stars:>20",
        "topic:shopping",
        "topic:deals",
    ],
    "dining": [
        "awesome-food",
        "restaurant-api stars:>30",
        "yelp-api stars:>20",
        "food-delivery stars:>30",
        "restaurant-finder stars:>20",
        "topic:food",
        "topic:restaurant",
    ],
    "secondhand": [
        "marketplace stars:>50",
        "classifieds stars:>20",
        "craigslist stars:>10",
        "facebook-marketplace stars:>10",
        "topic:marketplace",
    ],
    
    # 休闲娱乐
    "fitness": [
        "awesome-fitness",
        "fitness-api stars:>30",
        "workout stars:>50",
        "gym-finder stars:>10",
        "exercise-tracker stars:>30",
        "topic:fitness",
    ],
    "entertainment": [
        "awesome-entertainment",
        "movie-api stars:>50",
        "event-api stars:>30",
        "concert-finder stars:>10",
        "topic:entertainment",
        "topic:movies",
    ],
    "social": [
        "community-platform stars:>30",
        "event-platform stars:>30",
        "meetup stars:>20",
        "social-network stars:>30",
        "topic:community",
        "topic:social",
    ],
    "pet": [
        "awesome-pets",
        "pet-api stars:>10",
        "vet-finder stars:>10",
        "pet-adoption stars:>10",
        "topic:pets",
        "topic:veterinary",
    ],
    
    # 家政服务
    "cleaning": [
        "cleaning-service stars:>20",
        "home-service stars:>30",
        "house-cleaning stars:>10",
        "topic:cleaning",
        "topic:home-services",
    ],
    "repair": [
        "repair-service stars:>20",
        "home-repair stars:>20",
        "handyman stars:>10",
        "topic:repair",
        "topic:maintenance",
    ],
    
    # 人生大事
    "wedding": [
        "wedding-planner stars:>20",
        "wedding stars:>30",
        "marriage-license stars:>10",
        "topic:wedding",
    ],
    "funeral": [
        "funeral stars:>10",
        "memorial stars:>10",
        "cremation stars:>10",
        "topic:funeral",
    ],
}

# Update each domain
print("Seeding discovery keywords...")
updated = 0
for code, keywords in DOMAIN_KEYWORDS.items():
    result = client.table("domains").update({"discovery_keywords": keywords}).eq("code", code).execute()
    if result.data:
        updated += 1
        print(f"  ✓ {code}: {len(keywords)} keywords")
    else:
        print(f"  ✗ {code}: not found")

print(f"\nUpdated {updated} domains")
