# North America Advisor - Python Backend

北美生活决策顾问系统 - FastAPI + Supabase + Alembic

## 技术栈

- **FastAPI** - 现代异步 Web 框架
- **Supabase** - PostgreSQL 数据库 + 认证
- **SQLAlchemy** - ORM
- **Alembic** - 数据库迁移
- **Pydantic** - 数据验证

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install -e ".[dev]"
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入 Supabase 配置
```

### 3. 数据库迁移

```bash
# 生成迁移
alembic revision --autogenerate -m "initial"

# 执行迁移
alembic upgrade head
```

### 4. 启动服务

```bash
# 开发模式
uvicorn src.main:app --reload --port 8000

# 或
python -m src.main
```

## 项目结构

```
backend-python/
├── alembic/              # 数据库迁移
│   ├── versions/         # 迁移文件
│   └── env.py
├── src/
│   ├── common/           # 公共模块
│   │   ├── database.py   # 数据库连接
│   │   ├── errors.py     # 异常定义
│   │   ├── logger.py     # 日志
│   │   ├── middleware.py # 中间件
│   │   └── response.py   # 响应格式
│   ├── models/           # SQLAlchemy 模型
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── domain.py     # 领域模型
│   │   └── ...
│   ├── modules/          # 业务模块
│   │   ├── auth/         # 认证模块
│   │   └── advisor/      # 顾问模块
│   ├── config.py         # 配置
│   └── main.py           # 入口
├── tests/                # 测试
├── alembic.ini
├── pyproject.toml
└── README.md
```

## API 文档

启动服务后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发命令

```bash
# 代码检查
ruff check .

# 代码格式化
ruff format .

# 类型检查
mypy src

# 运行测试
pytest

# 测试覆盖率
pytest --cov=src
```
