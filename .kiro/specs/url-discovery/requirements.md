# URL 自动探索功能

## 背景

Data Sources 模块目前只支持手动添加 URL，需要增加自动探索功能，帮助管理员快速发现不同领域的高质量数据源，然后交给 Crawlers 模块抓取实际内容。

## 数据流

```
URL 探索 → Data Sources（元数据）→ Crawlers（抓取）→ 检索引擎
```

## 用户故事

### US-1: 基于 GitHub 探索数据源

**作为** 管理员
**我想要** 通过关键词搜索 GitHub 仓库
**以便于** 快速发现某个领域的优质资源

**验收标准：**

- [ ] 输入关键词（如 "machine learning", "react"）搜索仓库
- [ ] 支持按 stars、更新时间排序
- [ ] 显示仓库基本信息（名称、描述、stars、语言）
- [ ] 可批量选择并添加到 Data Sources
- [ ] 自动填充 category/subcategory

### US-2: 解析 Awesome 列表

**作为** 管理员
**我想要** 解析 awesome-xxx 仓库中的链接
**以便于** 批量导入高质量资源列表

**验收标准：**

- [ ] 输入 awesome 仓库 URL
- [ ] 自动解析 README 中的链接
- [ ] 按章节分组显示
- [ ] 可选择性导入到 Data Sources
- [ ] 自动识别链接类型（github/website/api）

### US-3: 基于种子 URL 爬取发现

**作为** 管理员
**我想要** 从一个入口页面发现相关链接
**以便于** 探索某个网站的资源结构

**验收标准：**

- [ ] 输入种子 URL
- [ ] 爬取页面中的链接
- [ ] 支持过滤规则（同域名、路径模式、深度限制）
- [ ] 预览发现的链接
- [ ] 批量添加到 Data Sources

### US-4: 按领域分类探索

**作为** 管理员
**我想要** 按预设领域快速探索资源
**以便于** 系统化地构建各领域数据源

**验收标准：**

- [ ] 预设领域列表（job, education, investment, insurance, house, car, hotel, flight）
- [ ] 每个领域有推荐的搜索关键词
- [ ] 一键探索某个领域的资源
- [ ] 探索结果自动关联领域分类

## 技术设计

### 后端 API

```
POST /data-sources/discover/github     # GitHub 搜索
POST /data-sources/discover/awesome    # 解析 awesome 列表
POST /data-sources/discover/crawl      # 种子 URL 爬取
GET  /data-sources/discover/domains    # 获取领域推荐关键词
```

### 数据结构

```python
class DiscoverResult:
    url: str
    name: str
    description: str
    type: str  # github/website/api
    suggested_category: str
    suggested_subcategory: str
    metadata: dict  # stars, language, etc.
```

### 前端组件

- `DiscoverPanel` - 探索面板（可作为 DataSourcesView 的一部分或独立 Tab）
- `GitHubSearchForm` - GitHub 搜索表单
- `AwesomeParserForm` - Awesome 列表解析
- `UrlCrawlerForm` - 种子 URL 爬取
- `DiscoverResultList` - 探索结果列表（支持批量选择）

## 实现优先级

1. **P0**: GitHub 搜索 - 最实用，API 稳定
2. **P1**: Awesome 列表解析 - 高质量资源聚合
3. **P2**: 种子 URL 爬取 - 通用但复杂度高
4. **P3**: 领域预设 - 锦上添花

## 依赖

- GitHub API（需要 token 提高 rate limit）
- 爬虫库（requests/httpx + beautifulsoup）
- Markdown 解析（解析 awesome 列表）
