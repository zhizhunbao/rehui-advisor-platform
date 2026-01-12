# 开发指南

## 端口配置

- **前端**: http://localhost:3000 (React + Vite)
- **后端**: http://localhost:8000 (Python + FastAPI)

## VSCode 任务使用

### 快速启动

1. **启动全栈开发环境** (`Ctrl+Shift+P` → `Tasks: Run Task` → `🌟 启动全栈开发环境`)
   - 同时启动前端和后端服务
   - 前端: http://localhost:3000
   - 后端: http://localhost:8000

### 单独启动服务

- **启动后端服务**: `🚀 启动后端服务 (端口8000)`
- **启动前端服务**: `🎨 启动前端服务 (端口3000)`

### 代码质量

- **后端代码检查**: `🔍 后端代码检查 (Python)`
- **前端代码检查**: `🔎 前端代码检查`
- **后端自动修复**: `🔧 后端自动修复代码 (Python)`
- **后端格式化**: `✨ 后端格式化代码 (Python)`

### 测试

- **后端运行测试**: `🧪 后端运行测试 (Python)`
- **后端监听测试**: `🔄 后端监听测试 (Python)`

### 数据库管理

- **数据库迁移**: `🔄 数据库迁移 (Alembic)`
- **生成迁移文件**: `📝 生成数据库迁移 (Alembic)`

### 依赖管理

- **安装所有依赖**: `📦 安装所有依赖`
- **清理依赖**: `🧹 清理依赖`

## 调试配置

### 后端调试

1. 在 VSCode 中按 `F5` 或使用调试面板
2. 选择 `🚀 调试后端服务 (Python)`
3. 设置断点并开始调试

### 测试调试

1. 选择 `🧪 调试后端测试 (Python)`
2. 可以调试特定的测试文件

## 快捷键

- `Ctrl+Shift+P` → `Tasks: Run Task` - 运行任务
- `F5` - 开始调试
- `Ctrl+F5` - 运行而不调试

## 开发流程

1. **首次设置**:

   ```bash
   # 安装依赖
   运行任务: 📦 安装所有依赖

   # 运行数据库迁移
   运行任务: 🔄 数据库迁移 (Alembic)
   ```

2. **日常开发**:

   ```bash
   # 启动开发环境
   运行任务: 🌟 启动全栈开发环境
   ```

3. **代码提交前**:

   ```bash
   # 检查代码质量
   运行任务: 🔍 后端代码检查 (Python)
   运行任务: 🔎 前端代码检查

   # 运行测试
   运行任务: 🧪 后端运行测试 (Python)
   ```

## 环境变量

确保 `backend/.env` 文件配置正确:

```env
# 后端端口
PORT=8000

# 数据库连接
DATABASE_URL=postgresql://postgres:password@localhost:5432/rehui_advisor

# JWT 配置
JWT_SECRET=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

## API 端点

- 健康检查: http://localhost:8000/health
- API 文档: http://localhost:8000/docs (Swagger UI)
- ReDoc 文档: http://localhost:8000/redoc
- 认证接口: http://localhost:8000/api/auth/\*
- 顾问接口: http://localhost:8000/api/advisor/\*

## 故障排除

### 端口冲突

如果端口被占用，可以：

1. 修改 `backend/.env` 中的 `PORT`
2. 修改 `frontend/vite.config.ts` 中的端口配置
3. 更新代理配置指向新的后端端口

### 依赖问题

```bash
# 后端 (Python)
cd backend
uv sync

# 前端
cd frontend
npm install
```

### 数据库问题

```bash
# 运行迁移
cd backend
uv run alembic upgrade head

# 生成新迁移
uv run alembic revision --autogenerate -m "description"
```
