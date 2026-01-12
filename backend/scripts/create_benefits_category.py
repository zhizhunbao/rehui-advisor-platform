"""Create Government Benefits category and move the benefits domain to it"""
from src.common.supabase import get_supabase_admin

client = get_supabase_admin()

# New category data
CATEGORY = {
    "code": "government",
    "name": "政府福利",
    "name_en": "Government Benefits",
    "description": "政府补贴、社会福利、公共服务等",
    "description_en": "Government subsidies, social benefits, public services",
    "icon": "🏛️",
    "color": "bg-emerald-600",
    "sort_order": 7,  # After healthcare_legal (6)
    "is_active": True,
}


def create_category_and_move_domain():
    """Create the government benefits category and move the domain"""
    print("Creating Government Benefits category...")
    
    # 1. Check if category already exists
    existing = (
        client.table("domain_categories")
        .select("id")
        .eq("code", "government")
        .execute()
    )
    
    if existing.data and len(existing.data) > 0:
        category_id = existing.data[0]["id"]
        print(f"  Category already exists: {category_id}")
    else:
        # Create new category
        response = (
            client.table("domain_categories")
            .insert(CATEGORY)
            .execute()
        )
        
        if not response.data:
            print("Error: Failed to create category")
            return
        
        category_id = response.data[0]["id"]
        print(f"  Created category: {category_id}")
    
    # 2. Move the benefits domain to this category
    domain_response = (
        client.table("domains")
        .select("id, name")
        .eq("code", "benefits")
        .execute()
    )
    
    if domain_response.data and len(domain_response.data) > 0:
        domain_id = domain_response.data[0]["id"]
        domain_name = domain_response.data[0]["name"]
        
        # Update domain's category_id
        client.table("domains").update({
            "category_id": category_id
        }).eq("id", domain_id).execute()
        
        print(f"  Moved domain '{domain_name}' to new category")
    else:
        print("  Note: benefits domain not found, skipping move")
    
    print("\n✅ Government Benefits category created successfully!")
    print(f"   Category code: government")
    print(f"   Category name: 政府福利 / Government Benefits")


if __name__ == "__main__":
    create_category_and_move_domain()
