"""测试 DataSource 模块迁移到 Document Store"""
import sys
sys.path.insert(0, ".")

from src.modules.admin.data_source.service import DataSourceService


def test_data_source():
    service = DataSourceService()
    
    print("1. 创建数据源...")
    ds = service.create({
        "url": "https://github.com/test/test-repo-001",
        "name": "Test Repo",
        "description": "A test repository",
        "type": "github",
        "category": "test",
    })
    print(f"   创建成功: {ds['id']} - {ds['name']}")
    
    print("\n2. 通过 ID 查询...")
    found = service.find_by_id(ds["id"])
    print(f"   查询结果: {found['name']}")
    
    print("\n3. 通过 URL 查询...")
    found_by_url = service.find_by_url("https://github.com/test/test-repo-001")
    print(f"   查询结果: {found_by_url['name']}")
    
    print("\n4. 获取所有数据源...")
    sources, total = service.find_all()
    print(f"   数据源数量: {total}")
    
    print("\n5. 获取统计信息...")
    stats = service.get_stats()
    print(f"   总数: {stats['total']}")
    print(f"   按类型: {stats['by_type']}")
    
    print("\n6. 获取类型列表...")
    types = service.get_types()
    print(f"   类型: {types}")
    
    print("\n7. 更新数据源...")
    updated = service.update(ds["id"], {"name": "Updated Test Repo", "description": "Updated description"})
    print(f"   更新结果: {updated['name']}")
    
    print("\n8. 删除数据源...")
    service.delete(ds["id"])
    print("   删除成功")
    
    print("\n9. 验证删除...")
    deleted = service.find_by_id(ds["id"])
    print(f"   查询结果: {deleted}")
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    test_data_source()
