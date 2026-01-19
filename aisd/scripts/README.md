# AISD Scripts

课程辅助脚本工具集

## 目录结构

```
scripts/
├── scrapers/           # 数据抓取脚本
│   ├── fetch_links.py  # 链接抓取工具
│   └── brightspace/    # Brightspace 爬虫
├── organizers/         # 数据整理脚本
│   └── organize_courses.py
├── utils/              # 工具函数
│   └── file_helpers.py
└── run.py             # 主入口
```

## scrapers/fetch_links.py

抓取 links.md 文件中的所有链接，生成中英对照文档框架。

### 前置要求

确保已安装 uv：

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 使用方法

**无需手动安装依赖！** uv 会自动管理所有依赖。

```bash
# 基本用法
uv run scrapers/fetch_links.py <links_file_path>

# 示例：抓取 RL 课程链接
cd aisd/scripts
uv run scrapers/fetch_links.py ../courses/rl/links.md

# 示例：抓取 NLP 课程链接
uv run scrapers/fetch_links.py ../courses/nlp/links.md
```

### 功能特性

- ✅ 自动解析 Markdown 链接格式 `[title](url)`
- ✅ 支持 Medium 文章专门优化
- ✅ 通用网页内容提取
- ✅ 生成中英对照文档框架
- ✅ 自动保存到课程目录
- ✅ 使用 uv 自动管理依赖（无需手动安装）

### 输出格式

生成的文档包含：

- 原文链接
- 逐段原文内容
- 翻译占位符（需要手动翻译或使用 AI 翻译）
- 学习建议

### 注意事项

1. **版权合规**: 脚本只提取文本内容框架，翻译时需要改写而非直接复制
2. **网络访问**: 需要能访问目标网站
3. **内容质量**: 不同网站的提取效果可能不同，建议检查后手动调整

### 技术栈

- **uv**: 现代 Python 包管理器，自动处理依赖
- **requests**: HTTP 请求
- **beautifulsoup4**: HTML 解析
- **lxml**: 高性能 XML/HTML 解析器
