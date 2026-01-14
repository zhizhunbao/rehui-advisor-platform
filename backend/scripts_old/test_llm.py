"""测试 LLM 模块迁移到 Document Store"""
import sys
sys.path.insert(0, ".")

from src.modules.admin.llm.service import LLMService


def test_llm():
    service = LLMService()
    
    print("1. 创建模型...")
    model = service.create_model({
        "name": "test-model-001",
        "display_name": "Test Model",
        "provider": "test",
        "api_endpoint": "https://api.test.com/v1",
        "category": "chat",
        "deployment_type": "api",
        "input_price": 1.0,
        "output_price": 2.0,
        "is_free": False,
        "context_window": 8192,
        "max_output_tokens": 4096,
        "is_active": True,
        "is_default": False,
    })
    print(f"   创建成功: {model['id']} - {model['name']}")
    
    print("\n2. 通过 ID 查询...")
    found = service.find_model_by_id(model["id"])
    print(f"   查询结果: {found['name']}")
    
    print("\n3. 通过名称查询...")
    found_by_name = service.find_model_by_name("test-model-001")
    print(f"   查询结果: {found_by_name['name']}")
    
    print("\n4. 获取所有模型...")
    models, total = service.find_all_models()
    print(f"   模型数量: {total}")
    
    print("\n5. 获取活跃模型...")
    active = service.find_active_models()
    print(f"   活跃模型数量: {len(active)}")
    
    print("\n6. 获取筛选选项...")
    filters = service.get_model_filters()
    print(f"   Providers: {len(filters['providers'])}")
    print(f"   Categories: {len(filters['categories'])}")
    
    print("\n7. 更新模型...")
    updated = service.update_model(model["id"], {"display_name": "Updated Test Model"})
    print(f"   更新结果: {updated['display_name']}")
    
    print("\n8. 设为默认模型...")
    default = service.update_model(model["id"], {"is_default": True})
    print(f"   是否默认: {default['is_default']}")
    
    print("\n9. 获取默认模型...")
    default_model = service.get_default_model()
    print(f"   默认模型: {default_model['name'] if default_model else 'None'}")
    
    print("\n10. 删除模型...")
    service.delete_model(model["id"])
    print("   删除成功")
    
    print("\n11. 验证删除...")
    deleted = service.find_model_by_id(model["id"])
    print(f"   查询结果: {deleted}")
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    test_llm()
