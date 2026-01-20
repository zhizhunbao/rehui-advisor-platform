# RL Course Scripts

强化学习课程的实用脚本工具。

## 脚本列表

### 1. 向量化教科书 (`vectorize_textbook.py`)

将 Sutton RL 教科书转换为向量数据库，支持语义搜索。

**功能**:

- 从 PDF 提取文本
- 分块处理（500 字符/块，50 字符重叠）
- 使用 OpenAI embeddings 生成向量
- 保存为单个 JSON 文件

**使用方法**:

```bash
cd aisd/courses/rl/scripts
python vectorize_textbook.py
```

**输出**:

- `../resources/textbook_vectors.json` (约 50-100 MB)

**依赖**:

```bash
uv pip install pypdf openai numpy
```

**成本估算**:

- 使用 `text-embedding-3-small` 模型
- 约 $0.0001/1K tokens
- 500 页教科书约 $0.5-2

---

### 2. 查询教科书 (`query_textbook.py`)

语义搜索向量化的教科书内容。

**使用方法**:

**交互式模式**:

```bash
python query_textbook.py

# 示例查询
🔍 查询 > What is Cliff Walking problem?
🔍 查询 > Explain Q-Learning algorithm
🔍 查询 > Bellman equation derivation
```

**命令行模式**:

```bash
python query_textbook.py "What is temporal difference learning?"
```

**输出示例**:

```
【结果 1】相似度: 0.8523 | 页码: 132
--------------------------------------------------------------------------------
The cliff-walking task is a standard undiscounted, episodic task, with start
and goal states, and the usual actions causing movement up, down, right, and
left. Reward is -1 on all transitions except those into the region marked
"The Cliff." Stepping into this region incurs a reward of -100 and sends the
agent instantly back to the start...
```

---

### 3. 抓取 Medium 文章 (`scrape_medium_article.py`)

从 Medium 抓取文章内容，包括代码块。

**使用方法**:

```bash
python scrape_medium_article.py
```

**输出**:

- `../resources/article_data.json`

---

### 4. 生成双语 Markdown (`generate_bilingual_md.py`)

将抓取的文章数据转换为双语 Markdown 格式。

**使用方法**:

```bash
python generate_bilingual_md.py
```

**输出**:

- `../resources/math_of_q_learning_python_bilingual.md`

---

## 工作流示例

### 场景 1: 准备 Lab 1 学习材料

```bash
# 1. 抓取 Medium 教程
python scrape_medium_article.py

# 2. 生成双语版本
python generate_bilingual_md.py

# 3. 向量化教科书（可选，用于深度查询）
python vectorize_textbook.py

# 4. 查询 Cliff Walking 相关内容
python query_textbook.py "Cliff Walking example page 132"
```

### 场景 2: 查找特定概念

```bash
# 启动交互式查询
python query_textbook.py

# 输入查询
🔍 查询 > temporal difference learning
🔍 查询 > eligibility traces
🔍 查询 > policy gradient methods
```

---

## 配置

### OpenAI API Key

确保设置了环境变量：

```bash
export OPENAI_API_KEY="your-api-key"
```

或在 `.env` 文件中：

```
OPENAI_API_KEY=your-api-key
```

### 自定义参数

编辑脚本顶部的配置：

**vectorize_textbook.py**:

```python
CHUNK_SIZE = 500        # 每块字符数
CHUNK_OVERLAP = 50      # 重叠字符数
```

**query_textbook.py**:

```python
top_k = 5              # 返回结果数量
```

---

## 故障排除

### 问题 1: PDF 读取失败

**错误**: `PdfReadError: EOF marker not found`

**解决**:

- 检查 PDF 文件是否完整
- 尝试重新下载 PDF
- 使用 `pypdf2` 替代 `pypdf`

### 问题 2: OpenAI API 超时

**错误**: `Timeout error`

**解决**:

- 减小批处理大小（`batch_size = 50`）
- 增加重试次数
- 检查网络连接

### 问题 3: 内存不足

**错误**: `MemoryError`

**解决**:

- 减小 `CHUNK_SIZE`
- 分批处理 PDF（按章节）
- 使用流式处理

---

## 进阶用法

### 只向量化特定章节

```python
# 修改 vectorize_textbook.py
def extract_text_from_pdf(pdf_path: Path, start_page: int = 1, end_page: int = None):
    # ... 只处理指定页面范围
```

### 使用本地 Embedding 模型

```python
# 替换 OpenAI embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)
```

### 导出为其他格式

```python
# 导出为 CSV
import pandas as pd

df = pd.DataFrame(data['chunks'])
df.to_csv('textbook_chunks.csv', index=False)
```

---

## 维护

### 更新向量数据

当教科书更新时：

```bash
# 重新向量化
python vectorize_textbook.py

# 备份旧数据
mv ../resources/textbook_vectors.json ../resources/textbook_vectors.json.bak
```

### 清理缓存

```bash
# 删除向量文件
rm ../resources/textbook_vectors.json

# 重新生成
python vectorize_textbook.py
```

---

## 贡献

添加新脚本时：

1. 遵循现有命名规范
2. 添加文档字符串
3. 更新此 README
4. 测试所有功能

---

**最后更新**: 2025-01-20
