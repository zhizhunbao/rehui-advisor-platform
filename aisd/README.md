# AISD - AI & Software Development Learning

AI 和软件开发学习环境，包含多个课程的代码、笔记和实验。

## 项目结构

```
aisd/
├── courses/          # 课程内容
│   ├── dl/          # Deep Learning (深度学习)
│   ├── llm/         # Large Language Models (大语言模型)
│   ├── ml/          # Machine Learning (机器学习)
│   ├── mv/          # Machine Vision (机器视觉)
│   ├── nlp/         # Natural Language Processing (自然语言处理)
│   └── rl/          # Reinforcement Learning (强化学习)
└── scripts/         # 辅助脚本
    ├── scrapers/    # 数据抓取
    ├── organizers/  # 数据整理
    └── utils/       # 工具函数
```

## 课程目录结构

每个课程遵循统一的目录结构：

```
course/
├── slides/          # 课件 PPT/PDF
├── labs/            # 实验材料和代码
├── assignments/     # 作业要求和提交
├── notes/           # 个人学习笔记
├── code/            # 代码练习和项目
├── resources/       # 补充学习资源
├── quizzes/         # 测验题目
├── schedule/        # 课程安排表
├── links.md         # 外部链接汇总
└── README.md        # 课程说明
```

## 环境设置

使用 uv 管理依赖（推荐）：

```bash
# 安装依赖
cd aisd
uv sync

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 或直接运行脚本（无需激活）
uv run python courses/mv/main.py
uv run python scripts/scrapers/fetch_links.py courses/rl/links.md
```

## 课程说明

### Machine Vision (mv)

- 依赖: opencv-python, matplotlib
- 主要内容: 图像处理、计算机视觉基础

### NLP

- 依赖: nltk
- 主要内容: 自然语言处理基础

### Reinforcement Learning (rl)

- 依赖: numpy, gymnasium
- 主要内容: Q-Learning, 策略梯度等

## 脚本工具

### scrapers/fetch_links.py

抓取 links.md 中的文章链接，生成中英对照文档。

```bash
cd scripts
uv run scrapers/fetch_links.py ../courses/rl/links.md
```

### organizers/organize_courses.py

标准化课程目录结构。

```bash
cd scripts
uv run organizers/organize_courses.py --course rl --execute
```

## 迁移说明

如果你之前在 `courses/mv/` 下有 `.venv`，现在可以：

1. **删除旧的虚拟环境**（推荐）

   ```bash
   rm -rf courses/mv/.venv
   ```

2. **在 aisd 根目录创建新环境**

   ```bash
   cd aisd
   uv sync
   ```

3. **更新 VS Code 设置**（如果使用）
   - Python 解释器路径改为: `${workspaceFolder}/aisd/.venv/bin/python`
