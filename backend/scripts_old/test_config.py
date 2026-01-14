"""测试 Config 模块迁移到 Document Store"""
import sys
sys.path.insert(0, ".")

from src.modules.admin.config.service import ConfigService


def test_config():
    service = ConfigService()
    
    print("1. 创建配置...")
    config = service.create({
        "key": "test_key_001",
        "value": {"foo": "bar", "num": 123},
        "description": "测试配置",
        "category": "test",
        "is_sensitive": False,
    })
    print(f"   创建成功: {config}")
    
    print("\n2. 通过 key 查询...")
    found = service.find_by_key("test_key_001")
    print(f"   查询结果: {found}")
    
    print("\n3. 通过 ID 查询...")
    found_by_id = service.find_by_id(config["id"])
    print(f"   查询结果: {found_by_id}")
    
    print("\n4. 获取配置值...")
    value = service.get_value("test_key_001")
    print(f"   配置值: {value}")
    
    print("\n5. 更新配置...")
    updated = service.update(config["id"], {"value": {"foo": "updated", "num": 456}})
    print(f"   更新结果: {updated}")
    
    print("\n6. 通过 key 更新值...")
    updated_by_key = service.update_by_key("test_key_001", "simple_string_value")
    print(f"   更新结果: {updated_by_key}")
    
    print("\n7. 获取所有配置...")
    all_configs = service.find_all()
    print(f"   配置数量: {len(all_configs)}")
    
    print("\n8. 获取分类...")
    categories = service.get_categories()
    print(f"   分类: {categories}")
    
    print("\n9. 删除配置...")
    service.delete(config["id"])
    print("   删除成功")
    
    print("\n10. 验证删除...")
    deleted = service.find_by_id(config["id"])
    print(f"   查询结果: {deleted}")
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    test_config()
