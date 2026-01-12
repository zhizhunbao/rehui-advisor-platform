# 设计文档

## 概述

管理员模块基于现有的代码基础设施进行补全和完善。后端使用 Python/FastAPI，前端使用 React/TypeScript。设计遵循现有的分层架构和命名规范。

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                      前端 (React)                            │
├─────────────────────────────────────────────────────────────┤
│  views/admin/          │  modules/admin/                    │
│  ├── LoginView         │  ├── hooks/                        │
│  ├── DashboardView     │  ├── services/                     │
│  ├── UsersView (新)    │  ├── types/                        │
│  ├── ConversationsView │  └── locales/                      │
│  ├── SubscriptionsView │                                    │
│  └── ConfigView (新)   │                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      后端 (FastAPI)                          │
├─────────────────────────────────────────────────────────────┤
│  modules/admin/                                              │
│  ├── auth_router.py (已有)  - 管理员认证                     │
│  ├── router.py (已有)       - 领域/Prompt/问题管理           │
│  ├── user_router.py (新)    - 用户管理                       │
│  ├── conversation_router.py - 对话记录管理                   │
│  ├── subscription_router.py - 订阅方案管理                   │
│  ├── recommendation_router.py - 推荐方案管理                 │
│  ├── crawler_router.py (新) - 抓取源管理                     │
│  └── config_router.py (新)  - 系统配置管理                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据库 (PostgreSQL)                     │
├─────────────────────────────────────────────────────────────┤
│  已有表: admin_users, domains, prompt_templates, questions,  │
│         crawl_sources, crawl_tasks, recommendations          │
│  新增表: subscription_plans, system_configs, conversations   │
└─────────────────────────────────────────────────────────────┘
```

## 组件和接口

### 后端 API 接口

#### 1. 管理员认证 (已有，需补全前端)

```
POST /api/admin/auth/login      - 管理员登录
POST /api/admin/auth/refresh    - 刷新令牌
GET  /api/admin/auth/me         - 获取当前管理员信息
PUT  /api/admin/auth/password   - 修改密码
POST /api/admin/auth/create     - 创建管理员 (仅超级管理员)
```

#### 2. 用户管理 (新增)

```
GET    /api/admin/users              - 获取用户列表
GET    /api/admin/users/:id          - 获取用户详情
PUT    /api/admin/users/:id/status   - 启用/禁用用户
GET    /api/admin/users/:id/quota    - 获取用户配额信息
```

#### 3. 对话记录管理 (新增)

```
GET    /api/admin/conversations           - 获取对话列表
GET    /api/admin/conversations/:id       - 获取对话详情
DELETE /api/admin/conversations/:id       - 删除对话
```

#### 4. 订阅方案管理 (新增)

```
GET    /api/admin/subscriptions           - 获取订阅方案列表
GET    /api/admin/subscriptions/:id       - 获取方案详情
POST   /api/admin/subscriptions           - 创建订阅方案
PUT    /api/admin/subscriptions/:id       - 更新订阅方案
DELETE /api/admin/subscriptions/:id       - 删除订阅方案
GET    /api/admin/subscriptions/:id/users - 获取方案订阅用户
```

#### 5. 推荐方案管理 (新增)

```
GET    /api/admin/recommendations         - 获取推荐方案列表
GET    /api/admin/recommendations/:id     - 获取方案详情
PUT    /api/admin/recommendations/:id     - 更新推荐方案
DELETE /api/admin/recommendations/:id     - 删除推荐方案
```

#### 6. 抓取源管理 (补全)

```
GET    /api/admin/crawlers/sources        - 获取抓取源列表
POST   /api/admin/crawlers/sources        - 创建抓取源
PUT    /api/admin/crawlers/sources/:id    - 更新抓取源
DELETE /api/admin/crawlers/sources/:id    - 删除抓取源
POST   /api/admin/crawlers/sources/:id/run - 手动触发抓取
GET    /api/admin/crawlers/tasks          - 获取任务列表
```

#### 7. 系统配置管理 (新增)

```
GET    /api/admin/configs                 - 获取配置列表
GET    /api/admin/configs/:key            - 获取配置值
PUT    /api/admin/configs/:key            - 更新配置值
```

### 前端组件

#### 1. 管理员登录页面 (新增)

- `views/admin/LoginView.tsx` - 登录表单
- 使用 localStorage 存储 admin_token

#### 2. 管理员布局组件 (新增)

- `modules/admin/components/AdminLayout.tsx` - 管理后台布局
- `modules/admin/components/AdminSidebar.tsx` - 侧边导航
- `modules/admin/components/AdminHeader.tsx` - 顶部栏

#### 3. 用户管理页面 (新增)

- `views/admin/UsersView.tsx` - 用户列表和管理

#### 4. 对话记录页面 (新增)

- `views/admin/ConversationsView.tsx` - 对话记录列表

#### 5. 订阅方案页面 (新增)

- `views/admin/SubscriptionsView.tsx` - 订阅方案管理

#### 6. 推荐方案页面 (新增)

- `views/admin/RecommendationsView.tsx` - 推荐方案管理

#### 7. 系统配置页面 (新增)

- `views/admin/ConfigView.tsx` - 系统配置管理

## 数据模型

### SubscriptionPlan (新增)

```python
class SubscriptionPlan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "subscription_plans"

    name: str                    # 方案名称
    name_en: str                 # 英文名称
    description: str | None      # 描述
    description_en: str | None   # 英文描述
    price: float                 # 价格
    currency: str = "USD"        # 货币
    billing_period: str          # monthly, yearly
    daily_quota: int             # 每日配额
    features: list[str]          # 功能列表
    is_active: bool = True       # 是否启用
    sort_order: int = 0          # 排序
```

### SystemConfig (新增)

```python
class SystemConfig(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "system_configs"

    key: str                     # 配置键 (唯一)
    value: str                   # 配置值 (JSON 字符串)
    description: str | None      # 描述
    category: str                # 分类: ai, quota, feature
    is_sensitive: bool = False   # 是否敏感信息
```

### Conversation (扩展现有)

```python
# 需要确认现有对话模型结构，可能需要添加管理相关字段
```

## 正确性属性

_正确性属性是系统在所有有效执行中应保持为真的特征或行为——本质上是关于系统应该做什么的形式化陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。_

### Property 1: 管理员认证令牌有效期

_For any_ 成功登录的管理员，返回的 Access_Token 解析后的 exp 字段应当为当前时间 + 24 小时（允许 1 分钟误差），Refresh_Token 的 exp 字段应当为当前时间 + 7 天
**Validates: Requirements 1.4, 1.5**

### Property 2: 登录错误信息一致性

_For any_ 错误的登录凭证（无论是用户名不存在还是密码错误），系统返回的错误信息应当相同，不泄露具体错误原因
**Validates: Requirements 1.3**

### Property 3: 领域 CRUD 一致性

_For any_ 有效的领域配置数据，创建后应能通过 ID 查询到相同数据，更新后应反映新值，删除后应查询不到
**Validates: Requirements 3.2, 3.3, 3.4**

### Property 4: 领域数据完整性

_For any_ 领域配置，应当包含 name、name_en（双语）以及 icon、color、sort_order 等必要属性
**Validates: Requirements 3.5, 3.6**

### Property 5: Prompt 模板 CRUD 一致性

_For any_ 有效的 Prompt 模板数据，创建后应能查询到，更新后应反映新值，删除后应查询不到
**Validates: Requirements 4.2, 4.3, 4.4**

### Property 6: 问题库 CRUD 一致性

_For any_ 有效的问题数据，创建后应能查询到，删除后应查询不到，且按领域筛选应只返回该领域的问题
**Validates: Requirements 5.2, 5.3, 5.4**

### Property 7: 管理员权限控制

_For any_ 普通管理员（role != super_admin），调用创建管理员 API 应返回 403 Forbidden
**Validates: Requirements 7.2**

### Property 8: 密码安全存储

_For any_ 创建或更新的管理员密码，数据库中存储的 password_hash 应当不等于原始密码，且应以 bcrypt 格式存储（以 $2b$ 开头）
**Validates: Requirements 7.4**

### Property 9: 订阅方案 CRUD 一致性

_For any_ 有效的订阅方案数据，创建后应能查询到，更新后应反映新值，删除后应查询不到
**Validates: Requirements 9.2, 9.3, 9.4**

### Property 10: 用户状态管理

_For any_ 用户，禁用后 is_active 应为 false，启用后 is_active 应为 true
**Validates: Requirements 10.4, 10.5**

### Property 11: 系统配置权限控制

_For any_ 普通管理员（role != super_admin），访问系统配置 API 应返回 403 Forbidden
**Validates: Requirements 13.2**

## 错误处理

### 认证错误

- 401 Unauthorized: 未提供令牌或令牌无效
- 403 Forbidden: 权限不足（普通管理员访问超级管理员功能）

### 业务错误

- 404 Not Found: 资源不存在
- 409 Conflict: 资源冲突（如用户名/邮箱已存在）
- 400 Bad Request: 请求参数验证失败

### 错误响应格式

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": null
  }
}
```

## 测试策略

### 单元测试

- 测试各 Service 层的业务逻辑
- 测试 DTO 验证规则
- 测试权限检查逻辑

### 属性测试

- 使用 hypothesis (Python) 进行属性测试
- 每个属性测试至少运行 100 次迭代
- 测试标签格式: **Feature: admin-module, Property {number}: {property_text}**

### 集成测试

- 测试完整的 API 请求/响应流程
- 测试数据库事务和回滚
- 测试认证中间件

### 测试框架

- 后端: pytest + pytest-asyncio + hypothesis
- 前端: vitest + @testing-library/react
