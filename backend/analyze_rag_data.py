from scripts.discover.raw_data.raw_rag_frameworks_urls import RAW_RAG_FRAMEWORKS_URLS

categories = {}
quality_ranges = {"90+": 0, "80-90": 0, "60-80": 0}
sources = {}

for item in RAW_RAG_FRAMEWORKS_URLS:
    cat = item['category']
    categories[cat] = categories.get(cat, 0) + 1
    
    score = item['metadata'].get('quality_score', 0)
    if score > 90:
        quality_ranges["90+"] += 1
    elif score >= 80:
        quality_ranges["80-90"] += 1
    else:
        quality_ranges["60-80"] += 1
    
    src = item['source']
    sources[src] = sources.get(src, 0) + 1

print("=" * 50)
print("RAG 框架资源数据分析")
print("=" * 50)
print(f"\n总资源数: {len(RAW_RAG_FRAMEWORKS_URLS)}")

print("\n分类统计:")
for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count}")

print("\n质量评分分布:")
for range_name, count in quality_ranges.items():
    print(f"  {range_name}: {count}")

print("\n数据来源:")
for src, count in sources.items():
    print(f"  {src}: {count}")

print("\n高质量资源示例 (评分 > 90):")
high_quality = [i for i in RAW_RAG_FRAMEWORKS_URLS if i['metadata'].get('quality_score', 0) > 90]
for item in high_quality[:10]:
    score = item['metadata']['quality_score']
    stars = item['metadata'].get('stars', 0)
    print(f"  [{score}分] {item['name']} - {stars} stars")
