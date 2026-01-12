"""Test data source service"""
from src.modules.data_source.service import DataSourceService

s = DataSourceService()
data, total = s.find_all(limit=2)
print(f"Total: {total}")
if data:
    print(f"Sample: {data[0]['name']}")
    print(f"Category: {data[0].get('domain_categories')}")
    print(f"Domain: {data[0].get('domains')}")
