# Docker 配置说明

## 目录结构

```
docker/
├── development/           # 开发环境配置
│   ├── docker-compose.yml   # 开发环境服务定义
│   ├── postgres/            # PostgreSQL 配置
│   └── redis/              # Redis 配置
├── production/            # 生产环境配置
│   ├── backend/            # 后端 Docker 配置
│   ├── frontend/           # 前端 Docker 配置
│   └── nginx/              # Nginx 配置
├── scripts/               # Docker 脚本
└── .dockerignore          # Docker 忽略文件
```

## 开发环境

### 快速启动

```bash
# 方式1：使用根目录的 docker-compose.yml
docker-compose up -d

# 方式2：使用脚本
./docker/scripts/dev-up.ps1

# 方式3：使用 VSCode 任务
# Ctrl+Shift+P -> Tasks: Run Task -> 🐳 启动数据库服务
```

### 服务访问

- **PostgreSQL**: `localhost:5432`
  - 数据库: `north_america_advisor`
  - 用户: `postgres`
  - 密码: `password`
- **Redis**: `localhost:6379`
- **pgAdmin**: `http://localhost:5050`
  - 邮箱: `admin@example.com`
  - 密码: `admin`

### 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重建并启动
docker-compose up -d --build

# 停止并删除数据
docker-compose down -v
```

## 生产环境

### 构建镜像

```bash
# 构建后端镜像
docker build -f docker/production/backend/Dockerfile -t na-advisor-backend .

# 构建前端镜像
docker build -f docker/production/frontend/Dockerfile -t na-advisor-frontend .
```

### 部署

```bash
# 使用生产环境配置
docker-compose -f docker/production/docker-compose.yml up -d
```

## 数据持久化

开发环境数据存储在 Docker volumes 中：

- `postgres_dev_data`: PostgreSQL 数据
- `redis_dev_data`: Redis 数据
- `pgadmin_dev_data`: pgAdmin 配置

## 网络配置

所有服务运行在 `na-advisor-network` 网络中，服务间可以通过服务名互相访问。

## 健康检查

所有服务都配置了健康检查，确保服务正常启动后才标记为可用。

## 环境变量

开发环境的环境变量在 `docker-compose.yml` 中定义，生产环境建议使用 `.env` 文件或外部配置管理。
