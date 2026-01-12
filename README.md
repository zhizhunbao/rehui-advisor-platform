# 北美生活决策顾问系统 (North America Advisor System)

智能推荐平台，帮助用户在北美地区的重大生活决策中找到最佳方案。

## 🌟 功能特性

- 🎫 机票搜索与比较
- 🏨 酒店推荐
- 💼 兼职工作搜索
- 🚗 购车信息分析
- 🏠 房产信息推荐
- 🎓 留学规划建议
- 💰 投资分析

## 🏗️ 项目架构

**前后端分离架构**

```
rehui-advisor-platform/
├── frontend/          # React + TypeScript 前端
├── backend/           # Node.js + Express 后端
├── docs/              # 项目文档
└── scripts/           # 初始化脚本
```

详细结构请查看 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

## 🚀 快速开始（2分钟）

### 1. 克隆项目（如果还没有）

```bash
git clone <repository-url>
cd rehui-advisor-platform
```

### 2. 启动后端

```bash
cd backend
npm install
npm run dev
```

后端运行在：**http://localhost:3000**

### 3. 启动前端

打开新终端：

```bash
cd frontend
npm install
npm run dev
```

前端运行在：**http://localhost:5173**

### 4. 访问应用

打开浏览器访问：**http://localhost:5173**

## 📸 预览

- ✨ 精美的主页界面
- 📊 实时系统状态显示
- 🎯 7 大功能模块展示
- 💎 定价方案（免费、Pro、企业版）
- 📱 完全响应式设计

## 🛠️ 技术栈

### 前端

- **React 18** + **TypeScript**
- **Vite** (SWC 编译器)
- **Ant Design** - UI 组件库
- **React Router** - 路由管理
- **Zustand** - 状态管理
- **Axios** - HTTP 请求

### 后端

- **Node.js** + **TypeScript**
- **Express** - Web 框架
- **Prisma** - ORM
- **PostgreSQL** - 数据库
- **bcrypt** - 密码加密
- **JWT** - 认证（待实现）

## 📁 项目结构

```
├── frontend/              # 前端项目
│   ├── src/
│   │   ├── pages/        # 页面组件
│   │   ├── services/     # API 服务
│   │   ├── store/        # 状态管理
│   │   └── types/        # 类型定义
│   └── package.json
│
├── backend/              # 后端项目
│   ├── src/
│   │   ├── config/      # 配置
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数
│   ├── prisma/          # 数据库
│   └── package.json
│
└── docs/                # 文档
```

## 🔧 开发命令

### 前端命令

```bash
cd frontend
npm run dev      # 启动开发服务器
npm run build    # 构建生产版本
npm run lint     # 代码检查
```

### 后端命令

```bash
cd backend
npm run dev              # 启动开发服务器
npm run build            # 构建生产版本
npm run db:generate      # 生成 Prisma Client
npm run db:migrate       # 运行数据库迁移
npm run db:studio        # 打开数据库 GUI
npm run db:seed          # 填充种子数据
```

## 🗄️ 数据库设置（可选）

后端可以在没有数据库的情况下运行（仅查看模式）。

如果需要完整功能：

### Windows

```powershell
cd backend
.\scripts\init-db.ps1
```

### Mac/Linux

```bash
cd backend
chmod +x scripts/init-db.sh
./scripts/init-db.sh
```

详细说明：[docs/DATABASE_QUICK_START.md](./docs/DATABASE_QUICK_START.md)

## 💡 Freemium 商业模式

- **匿名用户**：5 次/天免费搜索
- **注册用户**：50 次/天免费搜索
- **Pro 用户**：$29.99/月，无限搜索
- **企业版**：$99.99/月，高级功能

详细说明：[docs/FREEMIUM_MODEL.md](./docs/FREEMIUM_MODEL.md)

## 📚 文档

### 快速开始

- [START_HERE.md](./START_HERE.md) - 30秒快速开始 ⭐
- [QUICK_START.md](./QUICK_START.md) - 详细快速开始
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - 项目结构说明

### 前端文档

- [frontend/README.md](./frontend/README.md) - 前端开发指南
- [FRONTEND_SETUP_COMPLETE.md](./FRONTEND_SETUP_COMPLETE.md) - 前端设置说明

### 后端文档

- [backend/README.md](./backend/README.md) - 后端开发指南
- [docs/DATABASE.md](./docs/DATABASE.md) - 数据库详细文档
- [docs/DATABASE_QUICK_START.md](./docs/DATABASE_QUICK_START.md) - 数据库快速入门

### 规范文档

- [需求文档](./.kiro/specs/north-america-advisor/requirements.md)
- [设计文档](./.kiro/specs/north-america-advisor/design.md)
- [任务列表](./.kiro/specs/north-america-advisor/tasks.md)

## 🎯 开发状态

### ✅ 已完成

- [x] 前后端项目分离
- [x] React 前端搭建（主页 + 定价页面）
- [x] Express 后端搭建
- [x] 数据库模型设计（7 个领域）
- [x] Freemium 用户系统设计
- [x] 配额管理系统

### 🚧 开发中

- [ ] 用户认证系统（任务 3）
- [ ] 搜索功能 API
- [ ] 数据爬虫
- [ ] 推荐引擎
- [ ] 数据可视化

## 🤝 贡献

欢迎贡献代码！请查看 [任务列表](./.kiro/specs/north-america-advisor/tasks.md) 了解待完成的功能。

## 📄 许可证

MIT

## 🔗 相关链接

- [React 文档](https://react.dev/)
- [Ant Design 文档](https://ant.design/)
- [Prisma 文档](https://www.prisma.io/docs)
- [Express 文档](https://expressjs.com/)

---

**准备好了吗？**

```bash
# 终端 1 - 后端
cd backend && npm install && npm run dev

# 终端 2 - 前端
cd frontend && npm install && npm run dev
```

然后访问 http://localhost:5173 开始探索！🎉
