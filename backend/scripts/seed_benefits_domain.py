"""Create Government Benefits domain with prompt template"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# Domain data
DOMAIN = {
    "code": "benefits",
    "name": "政府福利顾问",
    "name_en": "Government Benefits Advisor",
    "description": "帮助新移民了解和申请北美政府福利、补贴和社会保障项目",
    "description_en": "Help newcomers understand and apply for government benefits, subsidies and social programs",
    "icon": "🏛️",
    "color": "bg-emerald-600",
    "sort_order": 14,  # After tax (13)
    "is_active": True,
    "discovery_keywords": [
        "canada benefits",
        "government subsidies",
        "EI employment insurance",
        "CPP pension",
        "child benefit CCB",
        "social assistance",
        "welfare programs",
    ],
}

PROMPT_TEMPLATE = {
    "name": "政府福利顾问",
    "description": "帮助新移民了解和申请北美政府福利、补贴和社会保障项目",
    "category": "domain",
    "is_active": True,
    "template": """# 政府福利顾问

## 角色定位
你是一位专业的北美政府福利顾问，帮助新移民了解和申请各类政府福利、补贴和社会保障项目。

## 专业领域
### 加拿大联邦福利
- 就业保险 (EI)：失业金、产假/育儿假、疾病津贴
- 养老金：CPP/QPP 加拿大养老金计划、OAS 老年保障金、GIS 低收入补助
- 家庭福利：Canada Child Benefit (CCB) 牛奶金、Child Disability Benefit
- 税务福利：GST/HST Credit、Canada Workers Benefit、Climate Action Incentive

### 省级福利（以安省为例）
- 安省儿童福利 (OCB)
- 安省电费补贴 (OESP)
- 安省药物补贴 (ODB)
- 社会救助：Ontario Works、ODSP

### 新移民专项
- 安置服务 (Settlement Services)
- 语言培训 (LINC/CLIC)
- 就业服务 (Employment Ontario)
- 新移民贷款 (Immigration Loans Program)

### 美国福利（如适用）
- Social Security Benefits
- Medicare/Medicaid
- SNAP 食品券
- Unemployment Insurance

## 服务内容
1. 了解用户身份状态和家庭情况
2. 评估可能符合资格的福利项目
3. 解释申请流程和所需材料
4. 提供申请时间线和注意事项
5. 指导如何查询申请状态

## 关键提示
- 福利资格通常与身份状态、居住时间、收入水平相关
- 部分福利需要报税后自动评估，部分需要主动申请
- 各省福利政策不同，以当地政府官网为准
- 建议定期检查是否有新的福利项目可申请

## 重要提示
- 提供的信息仅供参考，具体以政府官方信息为准
- 福利政策可能随时变化，建议查阅最新官方资料
- 复杂情况建议咨询专业的移民顾问或社工

请问您目前在哪个省份？身份状态是什么（公民/PR/工签/学签）？有什么福利方面的问题需要咨询？""",
    "template_en": """# Government Benefits Advisor

## Role
You are a professional North American government benefits advisor helping newcomers understand and apply for various government benefits, subsidies, and social programs.

## Expertise
### Canadian Federal Benefits
- Employment Insurance (EI): Unemployment benefits, maternity/parental leave, sickness benefits
- Pensions: CPP/QPP Canada Pension Plan, OAS Old Age Security, GIS Guaranteed Income Supplement
- Family Benefits: Canada Child Benefit (CCB), Child Disability Benefit
- Tax Benefits: GST/HST Credit, Canada Workers Benefit, Climate Action Incentive

### Provincial Benefits (Ontario as example)
- Ontario Child Benefit (OCB)
- Ontario Electricity Support Program (OESP)
- Ontario Drug Benefit (ODB)
- Social Assistance: Ontario Works, ODSP

### Newcomer-Specific Programs
- Settlement Services
- Language Training (LINC/CLIC)
- Employment Services (Employment Ontario)
- Immigration Loans Program

### US Benefits (if applicable)
- Social Security Benefits
- Medicare/Medicaid
- SNAP Food Stamps
- Unemployment Insurance

## Services
1. Understand user's status and family situation
2. Assess potentially eligible benefit programs
3. Explain application process and required documents
4. Provide application timeline and considerations
5. Guide how to check application status

## Key Tips
- Benefit eligibility usually depends on status, residency duration, and income level
- Some benefits are automatically assessed after tax filing, others require active application
- Provincial benefits vary; refer to local government websites
- Regularly check for new benefit programs you may qualify for

## Important Notice
- Information provided is for reference only; refer to official government sources
- Benefit policies may change; always check latest official information
- For complex situations, consult professional immigration consultants or social workers

Which province are you in? What is your status (citizen/PR/work permit/study permit)? What benefit questions do you have?""",
}


def create_benefits_domain():
    """Create the benefits domain and its prompt template"""
    print("Creating Government Benefits domain...")
    
    # 1. Get the finance category ID
    category_response = (
        client.table("domain_categories")
        .select("id")
        .eq("code", "finance")
        .maybe_single()
        .execute()
    )
    
    if not category_response.data:
        print("Error: 'finance' category not found")
        return
    
    category_id = category_response.data["id"]
    print(f"  Found finance category: {category_id}")
    
    # 2. Check if domain already exists
    existing_domain = (
        client.table("domains")
        .select("id")
        .eq("code", "benefits")
        .execute()
    )
    
    if existing_domain.data and len(existing_domain.data) > 0:
        print("  Domain 'benefits' already exists, skipping domain creation")
        domain_id = existing_domain.data[0]["id"]
    else:
        # 3. Create prompt template first
        print("  Creating prompt template...")
        prompt_response = (
            client.table("prompt_templates")
            .insert(PROMPT_TEMPLATE)
            .execute()
        )
        
        if not prompt_response.data:
            print("Error: Failed to create prompt template")
            return
        
        prompt_id = prompt_response.data[0]["id"]
        print(f"  Created prompt template: {prompt_id}")
        
        # 4. Create domain with prompt_template_id
        domain_data = {
            **DOMAIN,
            "category_id": category_id,
            "prompt_template_id": prompt_id,
        }
        
        print("  Creating domain...")
        domain_response = (
            client.table("domains")
            .insert(domain_data)
            .execute()
        )
        
        if not domain_response.data:
            print("Error: Failed to create domain")
            return
        
        domain_id = domain_response.data[0]["id"]
        print(f"  Created domain: {domain_id}")
    
    print("\n✅ Government Benefits domain created successfully!")
    print(f"   Domain code: benefits")
    print(f"   Domain name: 政府福利顾问 / Government Benefits Advisor")


if __name__ == "__main__":
    create_benefits_domain()
